"""Offline behavioral tests; constructed responses are not chain observations."""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import read_batch as tool

ZTO = '0xd782bdea4ef02a0bd391eb9089470c8080f0a68e'
IMD = '0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7'


def abi():
    return [{'type': 'function', 'name': 'totalSupply', 'stateMutability': 'view',
             'inputs': [], 'outputs': [{'name': 'supply', 'type': 'uint256'}]}]


def specification(ids=(3, '3')):
    return {'block': '0x18fd343', 'calls': [
        {'id': identifier, 'to': ZTO, 'function': 'totalSupply()', 'args': []}
        for identifier in ids]}


def response(identifier, value):
    return {'jsonrpc': '2.0', 'id': identifier, 'result': '0x' + value.to_bytes(32, 'big').hex()}


class BatchTests(unittest.TestCase):
    def setUp(self):
        self.entries = abi()
        self.plan = tool.prepare(self.entries, specification())

    def test_prepare_known_selector_and_exact_request(self):
        request = self.plan['requests'][0]
        self.assertEqual(request, {'jsonrpc': '2.0', 'id': 3, 'method': 'eth_call',
                                  'params': [{'to': ZTO, 'data': '0x18160ddd'}, '0x18fd343']})
        for value in ['', {}, None, 1]:
            spec = specification((1,))
            spec['calls'][0]['args'] = value
            with self.subTest(args=value), self.assertRaisesRegex(ValueError, 'JSON array'):
                tool.prepare(self.entries, spec)

    def test_argument_encoding_independent_words(self):
        entries = [{'type': 'function', 'name': 'balanceOf', 'stateMutability': 'view',
                    'inputs': [{'type': 'address'}], 'outputs': [{'type': 'uint256'}]}]
        spec = specification((1,))
        spec['calls'][0].update(function='balanceOf(address)', args=[IMD])
        # A constructed query of IMD's token-contract address on ZTO, not a user's account.
        data = tool.prepare(entries, spec)['requests'][0]['params'][0]['data']
        self.assertEqual(data, '0x70a08231' + '0' * 24 + IMD[2:])

    def test_unordered_responses_and_typed_ids(self):
        report = tool.inspect(self.entries, self.plan, [response('3', 29), response(3, 17)])
        self.assertEqual(report['status'], 'decoded')
        self.assertEqual([r['request_id'] for r in report['results']], [3, '3'])
        self.assertEqual([r['outputs'][0]['value'] for r in report['results']], [17, 29])

    def test_missing_response_is_explicit(self):
        report = tool.inspect(self.entries, self.plan, [response('3', 9)])
        self.assertEqual(report['status'], 'review-required')
        self.assertEqual(report['results'][0]['status'], 'missing-response')
        self.assertEqual(report['results'][1]['outputs'][0]['value'], 9)
        self.assertEqual(tool.inspect(self.entries, self.plan, [])['response_count'], 0)

    def test_extra_duplicate_and_invalid_ids_are_refused(self):
        for responses in ([response(4, 1)], [response(3, 1)] * 2,
                          [response(True, 1)], [response(None, 1)],
                          [response(3.0, 1)], [response('', 1)],
                          [response(2**53, 1)], [response('x' * 129, 1)]):
            with self.subTest(responses=responses), self.assertRaises(ValueError):
                tool.inspect(self.entries, self.plan, responses)
        for ids in ((1, 1), (True,), (None,), (1.0,), ('',)):
            with self.subTest(ids=ids), self.assertRaises(ValueError):
                tool.prepare(self.entries, specification(ids))

    def test_rpc_error_and_good_result_survive_together(self):
        error = {'jsonrpc': '2.0', 'id': 3, 'error': {'code': -32000, 'message': 'execution reverted'}}
        report = tool.inspect(self.entries, self.plan, [response('3', 19), error])
        self.assertEqual(report['status'], 'review-required')
        self.assertEqual(report['results'][0]['status'], 'rpc-error')
        self.assertNotIn('outputs', report['results'][0])
        self.assertEqual(report['results'][1]['outputs'][0]['value'], 19)

    def test_bad_return_and_unknown_selector_are_not_successes(self):
        bad = response(3, 1)
        bad['result'] += '00' * 32
        report = tool.inspect(self.entries, self.plan, [bad, response('3', 2)])
        self.assertEqual(report['results'][0]['status'], 'invalid-return')
        self.assertNotIn('outputs', report['results'][0])
        plan = copy.deepcopy(self.plan)
        plan['requests'][0]['params'][0]['data'] = '0xffffffff'
        report = tool.inspect(self.entries, plan, [response(3, 1)])
        self.assertEqual(report['results'][0]['status'], 'call-unknown-selector')

    def test_response_envelope_refusals_before_report(self):
        for field, value in [('jsonrpc', '1.0'), ('result', None)]:
            bad = response(3, 1)
            bad[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                tool.inspect(self.entries, self.plan, [bad])
        bad = response(3, 1)
        bad['error'] = {'code': -1, 'message': 'bad'}
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            tool.inspect(self.entries, self.plan, [bad])

    def test_no_mutation_methods_or_extra_call_fields(self):
        for method in ['eth_sendTransaction', 'eth_sendRawTransaction', 'eth_estimateGas']:
            plan = copy.deepcopy(self.plan)
            plan['requests'][0]['method'] = method
            with self.subTest(method=method), self.assertRaises(ValueError):
                tool.inspect(self.entries, plan, [])
        for key in ['from', 'value', 'gas', 'nonce']:
            plan = copy.deepcopy(self.plan)
            plan['requests'][0]['params'][0][key] = ZTO
            with self.subTest(key=key), self.assertRaises(ValueError):
                tool.inspect(self.entries, plan, [])

    def test_explicit_read_mutability_and_signature_required(self):
        for mutability in [None, 'payable', 'nonpayable']:
            entries = abi()
            entries[0]['stateMutability'] = mutability
            with self.subTest(mutability=mutability), self.assertRaises(ValueError):
                tool.prepare(entries, specification())
            with self.assertRaises(ValueError):
                tool.inspect(entries, self.plan, [])
        spec = specification()
        spec['calls'][0]['function'] = 'totalSupply'
        with self.assertRaisesRegex(ValueError, 'explicit'):
            tool.prepare(self.entries, spec)

    def test_collision_and_duplicate_signature_refusal(self):
        with self.assertRaises(ValueError):
            tool.prepare(self.entries * 2, specification())
        entries = [{'type': 'function', 'name': name, 'stateMutability': 'view',
                    'inputs': [{'type': typ}], 'outputs': []}
                   for name, typ in [('burn', 'uint256'), ('collate_propagate_storage', 'bytes16')]]
        spec = specification((1,))
        spec['calls'][0].update(function='burn(uint256)', args=[1])
        with self.assertRaisesRegex(ValueError, 'ambiguous-selector'):
            tool.prepare(entries, spec)

    def test_unsupported_outputs_fail_even_with_missing_response(self):
        entries = abi()
        entries[0]['outputs'] = [{'type': 'string[]'}]
        with self.assertRaises(ValueError):
            tool.prepare(entries, specification())
        with self.assertRaises(ValueError):
            tool.inspect(entries, self.plan, [])

    def test_explicit_block_tags_and_quantities(self):
        for block in ['latest', 'safe', 'finalized', 'pending', 'earliest', '0x0', '0x18fd343']:
            spec = specification()
            spec['block'] = block
            self.assertEqual(tool.prepare(self.entries, spec)['requests'][0]['params'][1], block)
        for block in [None, 123, '0x01', '0x', '0x' + 'f' * 65, {}, 'latest ']:
            spec = specification()
            spec['block'] = block
            with self.subTest(block=block), self.assertRaises(ValueError):
                tool.prepare(self.entries, spec)

    def test_item_and_aggregate_byte_limits(self):
        with self.assertRaises(ValueError):
            tool.prepare(self.entries, specification(tuple(range(33))))
        with self.assertRaises(ValueError):
            tool.prepare(self.entries, specification(()))
        with patch.object(tool, 'MAX_BATCH_BYTES', 7), self.assertRaisesRegex(ValueError, 'calldata'):
            tool.validate_plan(self.plan)
        with patch.object(tool, 'MAX_BATCH_BYTES', 40), self.assertRaisesRegex(ValueError, 'return data'):
            tool.inspect(self.entries, self.plan, [response(3, 1), response('3', 2)])

    def test_historical_zto_demo_round_trip(self):
        demo = tool.demo()
        self.assertEqual(demo['review']['status'], 'decoded')
        self.assertEqual(demo['review']['results'][0]['outputs'][0]['value'], 10**27)
        self.assertEqual(demo['plan']['requests'][0]['params'][0]['to'], ZTO)

    def test_cli_exits_and_workspace_reading(self):
        Path('test/scratch').mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir='test/scratch') as folder:
            folder = Path(folder)
            paths = {name: folder / (name + '.json') for name in ['abi', 'spec', 'plan', 'responses']}
            for name, value in [('abi', self.entries), ('spec', specification()),
                                ('plan', self.plan), ('responses', [response(3, 1)])]:
                paths[name].write_text(json.dumps(value))
            for arguments, expected in [(['demo'], 0),
                (['prepare', '--abi', str(paths['abi']), '--spec', str(paths['spec'])], 0),
                (['inspect', '--abi', str(paths['abi']), '--plan', str(paths['plan']),
                  '--responses', str(paths['responses'])], 1)]:
                with patch('sys.argv', ['read_batch.py'] + arguments), contextlib.redirect_stdout(io.StringIO()) as output:
                    self.assertEqual(tool.main(), expected)
                    json.loads(output.getvalue())
            paths['spec'].write_text('{"calls":[],"calls":[]}')
            with patch('sys.argv', ['read_batch.py', 'prepare', '--abi', str(paths['abi']),
                                    '--spec', str(paths['spec'])]), contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(tool.main(), 2)
                self.assertEqual(output.getvalue(), '')
            with self.assertRaisesRegex(ValueError, 'workspace'):
                tool.transcript.read_transcript(Path.cwd().parent / 'not-read.json')


if __name__ == '__main__':
    unittest.main()
