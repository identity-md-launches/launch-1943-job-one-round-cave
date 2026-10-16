#!/usr/bin/env python3
"""Try every line tool; retain compact evidence without changing line files.

The four live HTTP/TLS commands are anonymous bounded reads. All other trials
are offline. No shell, credentials, writes to inputs, or chain requests.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

# Explicit, reviewed commands; documentation is never evaluated as shell code.
TRIALS = [
(3,'import-shadow','shadow.py',['line-3/tools/import-shadow/examples','--json'],0),
(1,'accept-lens','accept_lens.py',['https://api.imd.fun/launches','--deadline','8'],0),
(4,'read-batch','read_batch.py',['demo'],0),
(1,'burst-sentry','burst_sentry.py',['https://api.imd.fun/launches','--samples','3','--budget','10','--per-probe','3','--timeout','2','--json','--expect-path','/launches/0/status'],0),
(1,'cache-lens','cache_lens.py',['line-1/tools/cache-lens/observed-live.json','--shared'],0),
(1,'deadline-sentry','deadline_sentry.py',['--deadline','8','https://api.imd.fun/launches','--timeout','5','--max-redirects','0','--max-bytes','262144','--json'],0),
(1,'endpoint-doctor','endpoint_doctor.py',['--report','line-1/tools/endpoint-doctor/observed-live.json'],0),
(1,'endpoint-sentry','sentry.py',['https://api.imd.fun/launches','--timeout','5','--max-redirects','0','--max-bytes','262144','--json'],0),
(1,'failure-map','failure_map.py',['line-1/tools/failure-map/observed-live36.json'],0),
(1,'framing-lens','framing_lens.py',['line-1/tools/framing-lens/observed-live.json'],0),
(1,'freshness-lens','freshness_lens.py',['line-1/tools/endpoint-doctor/observed-live.json','--at','2026-10-16T00:02:23.567439Z','--max-age','300'],1),
(1,'payload-lens','payload_lens.py',['line-1/tools/endpoint-doctor/observed-live.json','--media','application/json','--json-check','--min-bytes','1'],0),
(1,'probe-contract','probe_contract.py',['compare','line-1/tools/probe-contract/observed-before.json','line-1/tools/probe-contract/observed-after.json'],0),
(1,'probe-triage','probe_triage.py',['line-1/tools/probe-triage/observed-404.json'],0),
(1,'redirect-lens','redirect_lens.py',['line-1/tools/redirect-lens/observed-live.json'],0),
(1,'report-delta','report_delta.py',['line-1/tools/report-delta/observed-before.json','line-1/tools/report-delta/observed-after.json','--same-expectations'],0),
(1,'retry-lens','retry_lens.py',['line-1/tools/retry-lens/observed-live.json'],0),
(1,'timing-lens','timing_lens.py',['line-1/tools/timing-lens/observed-live.json','--max-ms','500'],0),
(1,'tls-route','tls_route.py',['https://api.imd.fun'],0),
(2,'csv-align','align.py',['line-2/tools/csv-align/demo-before.csv','line-2/tools/csv-align/demo-after.csv','--key','item','--key','location','--map','item','sku'],1),
(2,'csv-duplicates','duplicates.py',['line-2/tools/csv-duplicates/demo.csv','--key','item','--key','location','--format','text'],1),
(2,'csv-gate','gate.py',['line-2/tools/csv-gate/demo-before.csv','line-2/tools/csv-gate/demo-after.csv','--key','item','--max-added','1','--max-changed','1','--allow-change','quantity'],0),
(2,'csv-key-audit','audit.py',['line-2/tools/csv-key-audit/demo.csv','--key','item','--key','location','--format','text'],0),
(2,'csv-key-scout','scout.py',['line-2/tools/csv-key-scout/demo-before.csv','line-2/tools/csv-key-scout/demo-after.csv','--candidate','["record_id"]','--candidate','["source_code"]','--candidate','["area","record_id"]','--format','text'],0),
(2,'csv-merge','merge.py',[f'line-2/tools/csv-merge/demo-{s}.csv' for s in ('base','left','right')]+['--key','item','--key','place','--format','csv'],0),
(2,'csv-multiplicity','multiplicity.py',['line-2/tools/csv-multiplicity/demo-before.csv','line-2/tools/csv-multiplicity/demo-after.csv','--key','item','--key','location','--format','text'],1),
(2,'csv-patch','patch.py',['plan','line-2/tools/csv-reconcile/demo-before.csv','line-2/tools/csv-reconcile/demo-after.csv','--key','item','--key','location'],0),
(2,'csv-reconcile','reconcile.py',['line-2/tools/csv-reconcile/demo-before.csv','line-2/tools/csv-reconcile/demo-after.csv','--key','item','--key','location','--format','text'],1),
(2,'csv-review','review.py',['line-2/tools/csv-reconcile/demo-before.csv','line-2/tools/csv-reconcile/demo-after.csv','--key','item','--key','location'],1),
(2,'csv-slice','slice.py',['line-2/tools/csv-gate/demo-before.csv','line-2/tools/csv-gate/demo-after.csv','--key','item','--kind','changed','--limit','1'],1),
(2,'csv-summary','summary.py',['line-2/tools/csv-gate/demo-before.csv','line-2/tools/csv-gate/demo-after.csv','--key','item'],1),
(2,'csv-transitions','transitions.py',['line-2/tools/csv-transitions/demo-before.csv','line-2/tools/csv-transitions/demo-after.csv','--key','id','--column','status','--include-records'],1),
(2,'csv-undo','undo.py',['line-2/tools/csv-reconcile/demo-before.csv','line-2/tools/csv-patch/demo-plan.json'],0),
(3,'import-boundaries','boundaries.py',['line-3/tools/import-boundaries/examples','--strict'],0),
(3,'import-budget','budget.py',['line-3/tools/import-map/examples'],0),
(3,'import-context','context.py',['line-3/tools/import-context/examples'],0),
(3,'import-delta','delta.py',['line-3/tools/import-delta/examples/before','line-3/tools/import-delta/examples/after'],0),
(3,'import-dynamic','dynamic.py',['line-3/tools/import-dynamic/examples','--json'],0),
(3,'import-externals','externals.py',['line-3/tools/import-externals/examples'],0),
(3,'import-impact','impact.py',['line-3/tools/import-map/examples','pkg.helper'],0),
(3,'import-initializers','initializers.py',['line-3/tools/import-initializers/examples','--json'],0),
(3,'import-lineage','lineage.py',['line-3/tools/import-lineage/examples','app','service'],0),
(3,'import-map','import_map.py',['line-3/tools/import-map/examples'],0),
(3,'import-order','order.py',['line-3/tools/import-order/examples','--from','cli'],0),
(3,'import-origin-trace','origins.py',['line-3/tools/import-origin-trace/examples'],0),
(3,'import-reach','reach.py',['line-3/tools/import-reach/examples'],0),
(3,'import-route','route.py',['line-3/tools/import-map/examples','main','pkg.helper'],0),
(3,'import-witness','witness.py',['line-3/tools/import-map/examples'],0),
(4,'abi-delta','abi_delta.py',['--demo'],1),
(4,'abi-workbench','abi_workbench.py',['--demo'],0),
(4,'call-inspector','call_inspector.py',['--abi','line-4/tools/selector-audit/erc20.json','--data','0xa9059cbb'+'0'*24+'d782bdea4ef02a0bd391eb9089470c8080f0a68e'+'0'*63+'c'],0),
(4,'calldata-rehearsal','calldata_rehearsal.py',['--selector','0x70a08231','--types','address','--values','0xd782bdea4ef02a0bd391eb9089470c8080f0a68e'],0),
(4,'event-lens','event_lens.py',['--demo'],0),
(4,'revert-lens','revert_lens.py',['--demo'],0),
(4,'selector-audit','selector_audit.py',['--abi','line-4/tools/selector-audit/erc20.json'],0),
(4,'transcript-inspector','transcript_inspector.py',['--abi','line-4/tools/transcript-inspector/zto-total-supply-abi.json','--transcript','line-4/tools/transcript-inspector/zto-total-supply-transcript.json'],0),
]


def main():
    results = []
    for line, name, script, args, expected in TRIALS:
        command = [sys.executable, '-B', f'line-{line}/tools/{name}/{script}', *args]
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=15)
            item = {'line': line, 'tool': name, 'command': command,
                    'exit_code': result.returncode, 'expected_exit_code': expected,
                    'passed': result.returncode == expected,
                    'stdout_bytes': len(result.stdout.encode()),
                    'stdout_sha256': hashlib.sha256(result.stdout.encode()).hexdigest(),
                    'stdout_excerpt': result.stdout[:1000], 'stderr': result.stderr[:500]}
            if name in ('import-shadow','accept-lens','read-batch','import-origin-trace','burst-sentry','deadline-sentry','endpoint-sentry','tls-route','probe-contract',
                        'csv-transitions','import-initializers','import-dynamic','abi-delta','transcript-inspector'):
                Path(f'gathering/trial39-{name}.json').write_text(result.stdout)
        except subprocess.TimeoutExpired:
            item = {'line':line, 'tool':name, 'command':command, 'passed':False, 'error':'15-second trial timeout'}
        results.append(item)
    known = {str(p.parent) for p in Path('.').glob('line-*/tools/*/README.md')}
    covered = {f'line-{i}/tools/{name}' for i,name,*_ in TRIALS}
    assert known == covered
    report = {'round':39,'ok':all(r['passed'] for r in results), 'all_tools_covered':True,'results':results}
    Path('gathering/current-checks39.json').write_text(json.dumps(report,separators=(',',':'))+'\n')
    print(json.dumps({'ok':report['ok'],'trials':len(results),'failed':[r for r in results if not r['passed']]},indent=2))
    return int(not report['ok'])


if __name__ == '__main__':
    raise SystemExit(main())
