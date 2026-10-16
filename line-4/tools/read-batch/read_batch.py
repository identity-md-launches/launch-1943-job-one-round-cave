#!/usr/bin/env python3
"""Prepare read-only ABI eth_call batches and inspect saved responses offline."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

SOURCE = Path(__file__).resolve().parents[1] / 'transcript-inspector' / 'transcript_inspector.py'
spec = importlib.util.spec_from_file_location('line4_batch_transcript', SOURCE)
transcript = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transcript)
codec = transcript.codec
MAX_BATCH = 32
MAX_BATCH_BYTES = 512 * 1024
SCHEMA = 'read-batch-plan/v1'


def identifier(value):
    # Type is part of identity: JSON-RPC string "3" and integer 3 differ.
    if type(value) is int and abs(value) <= 2**53 - 1:
        return (int, value)
    if isinstance(value, str) and 1 <= len(value) <= 128:
        return (str, value)
    raise ValueError('id must be a safe integer or nonempty string of at most 128 characters')


def bounded_list(value, label, *, empty=False):
    if not isinstance(value, list) or not (0 if empty else 1) <= len(value) <= MAX_BATCH:
        raise ValueError(f'{label} must be a list of {0 if empty else 1}..{MAX_BATCH} items')


def index_by_id(items, label):
    found = {}
    for item in items:
        if not isinstance(item, dict) or 'id' not in item:
            raise ValueError(f'{label} item must be an object with id')
        key = identifier(item['id'])
        if key in found:
            raise ValueError(f'duplicate {label} id: {item["id"]!r}')
        found[key] = item
    return found


def check_block(block):
    if (not isinstance(block, str) or len(block) > 66 or
            not (block in transcript.BLOCK_TAGS or transcript.QUANTITY.fullmatch(block))):
        raise ValueError('block must be a block tag or canonical hex quantity of at most 256 bits')


def validate_plan(plan):
    if not isinstance(plan, dict) or set(plan) != {'schema', 'requests'} or plan['schema'] != SCHEMA:
        raise ValueError('expected read-batch-plan/v1 with only schema and requests')
    requests = plan['requests']
    bounded_list(requests, 'requests')
    index_by_id(requests, 'request')
    total = 0
    for request in requests:
        if (set(request) != {'jsonrpc', 'id', 'method', 'params'} or
                request['jsonrpc'] != '2.0' or request['method'] != 'eth_call'):
            raise ValueError('requests must contain only JSON-RPC 2.0 eth_call fields')
        params = request['params']
        if not isinstance(params, list) or len(params) != 2:
            raise ValueError('eth_call params must be [call, block]')
        call, block = params
        if not isinstance(call, dict) or set(call) != {'to', 'data'}:
            raise ValueError('call must contain only to and data')
        if not isinstance(call['to'], str) or not transcript.ADDRESS.fullmatch(call['to']):
            raise ValueError('to must be a 20-byte hex address')
        check_block(block)
        total += len(codec.parse_data(call['data'], call=True))
        if total > MAX_BATCH_BYTES:
            raise ValueError('aggregate calldata exceeds 512 KiB')
    return requests


def prepare(entries, specification):
    """No RPC client: the resulting requests can be reviewed and sent elsewhere."""
    codec.validate_abi(entries)
    if not isinstance(specification, dict) or set(specification) != {'block', 'calls'}:
        raise ValueError('specification must contain only block and calls')
    check_block(specification['block'])
    bounded_list(specification['calls'], 'calls')
    functions = [fn for fn in entries if fn['type'] == 'function']
    if len(functions) > transcript.calls.MAX_FUNCTIONS:
        raise ValueError('ABI exceeds 256 function entries')
    signatures = [(codec.input_signature(fn), fn) for fn in functions]
    requests = []
    for call in specification['calls']:
        if not isinstance(call, dict) or set(call) != {'id', 'to', 'function', 'args'}:
            raise ValueError('each call must contain only id, to, function and args')
        identifier(call['id'])
        if not isinstance(call['args'], list):
            raise ValueError('args must be a JSON array')
        _, signature = codec.function_reference(call['function'])
        if signature is None:
            raise ValueError('function must be an explicit canonical signature, such as totalSupply()')
        selected = [fn for sig, fn in signatures if sig == signature]
        if len(selected) != 1:
            raise ValueError('expected exactly one matching function: ' + signature)
        fn = selected[0]
        if fn.get('stateMutability') not in ('view', 'pure'):
            raise ValueError('function must explicitly declare view or pure')
        codec.check_type_tree(fn.get('outputs', []))
        for param in fn.get('outputs', []):
            codec.canonical(param)
        data = codec.keccak256(signature.encode('ascii'))[:4] + codec.encode_tuple(fn.get('inputs', []), call['args'])
        inspected = transcript.calls.inspect_call(entries, data)
        if inspected['status'] != 'decoded':
            raise ValueError('prepared calldata is not unambiguous: ' + inspected['status'])
        requests.append({'jsonrpc': '2.0', 'id': call['id'], 'method': 'eth_call',
                         'params': [{'to': call['to'], 'data': '0x' + data.hex()}, specification['block']]})
    plan = {'schema': SCHEMA, 'requests': requests}
    validate_plan(plan)
    return plan


def inspect(entries, plan, responses):
    requests = validate_plan(plan)
    bounded_list(responses, 'responses', empty=True)
    wanted = index_by_id(requests, 'request')
    received = index_by_id(responses, 'response')
    if received.keys() - wanted.keys():
        raise ValueError('response id is absent from the plan')
    # Validate all envelopes before producing any decoded report.
    total = 0
    for key, response in received.items():
        _, _, _, data, _ = transcript.validate_transcript({'request': wanted[key], 'response': response})
        total += len(data) if data is not None else 0
        if total > MAX_BATCH_BYTES:
            raise ValueError('aggregate return data exceeds 512 KiB')
    codec.validate_abi(entries)
    rows = []
    for request in requests:
        call, block = request['params']
        inspected = transcript.calls.inspect_call(entries, codec.parse_data(call['data'], call=True))
        if inspected['status'] == 'decoded':
            fn = entries[inspected['abi_index']]
            if fn.get('stateMutability') not in ('view', 'pure'):
                raise ValueError('planned function must explicitly declare view or pure')
            codec.check_type_tree(fn.get('outputs', []))
            for output in fn.get('outputs', []):
                codec.canonical(output)
        key = identifier(request['id'])
        if key not in received:
            rows.append({'request_id': request['id'], 'to': call['to'].lower(), 'block': block,
                         'status': 'missing-response', 'call': inspected})
        else:
            rows.append(transcript.inspect_transcript(entries, {'request': request, 'response': received[key]}))
    complete = all(row['status'] == 'decoded' for row in rows)
    return {'schema': 'read-batch-review/v1', 'status': 'decoded' if complete else 'review-required',
            'request_count': len(requests), 'response_count': len(responses),
            'block_identifiers': sorted({request['params'][1] for request in requests}),
            'results': rows,
            'limitations': 'Offline supplied ABI and response interpretation; no chain identity, freshness, authenticity or common-state proof. Tags may resolve to different blocks.'}


def demo():
    folder = SOURCE.parent
    entries = transcript.calls.inventory.read_abi(folder / 'zto-total-supply-abi.json')
    saved = transcript.read_transcript(folder / 'zto-total-supply-transcript.json')
    plan = prepare(entries, {'block': saved['request']['params'][1], 'calls': [
        {'id': saved['request']['id'], 'to': saved['request']['params'][0]['to'],
         'function': 'totalSupply()', 'args': []}]})
    if plan['requests'] != [saved['request']]:
        raise ValueError('prepared call does not match the saved ZTO request')
    return {'plan': plan, 'review': inspect(entries, plan, [saved['response']]),
            'evidence': 'Historical ZTO example retained by Transcript Inspector; no fresh RPC request.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('demo')
    build = commands.add_parser('prepare')
    build.add_argument('--abi', required=True)
    build.add_argument('--spec', required=True)
    review = commands.add_parser('inspect')
    review.add_argument('--abi', required=True)
    review.add_argument('--plan', required=True)
    review.add_argument('--responses', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'demo':
            result = demo()
        else:
            entries = transcript.calls.inventory.read_abi(args.abi)
            if args.command == 'prepare':
                result = prepare(entries, transcript.read_transcript(args.spec))
            else:
                result = inspect(entries, transcript.read_transcript(args.plan), transcript.read_transcript(args.responses))
    except (ValueError, TypeError, OSError, UnicodeError) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, allow_nan=False))
    return 1 if result.get('status') == 'review-required' else 0


if __name__ == '__main__':
    raise SystemExit(main())
