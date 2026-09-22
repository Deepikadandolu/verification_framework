import json
from pathlib import Path
from datetime import datetime

def write_report(report, outdir):
    outdir=Path(outdir); outdir.mkdir(parents=True,exist_ok=True)
    rid=report['regression_id']
    (outdir/f'regression_{rid}.json').write_text(json.dumps(report,indent=2))
    c=report['coverage']; f=report['failures']
    lines=[
        '# RTL Verification Regression Report',
        '',f"Regression: `{rid}`",f"Timestamp: `{report['timestamp']}`",f"Seed: `{report['seed']}`",'',
        '## Regression',
        f"- Tests generated: **{report['tests_generated']}**",
        f"- RTL tests observed: **{report['tests_observed']}**",
        f"- Functional failures: **{len(f)}**",
        f"- Assertion/protocol failures: **{report['assertion_failures']}**",
        f"- Timeouts: **{report['timeouts']}**",'',
        '## Coverage',
        f"- Operation coverage: **{c['operation_coverage_pct']}%**",
        f"- Operand-class coverage: **{c['operand_class_coverage_pct']}%**",
        f"- Cross coverage: **{c['cross_coverage_pct']}%**",'',
        '## Fault campaign',
        f"- Mutants injected: **{report['mutation']['total']}**",
        f"- Mutants detected: **{report['mutation']['detected']}**",
        f"- Escaped mutants: **{report['mutation']['escaped']}**",
        f"- Mutation/fault detection score: **{report['mutation']['score_pct']}%**",'',
        '## First failures'
    ]
    for x in f[:10]: lines.append(f"- Test `{x['tid']}`, cycle `{x['cycle']}`: `{x['op']}` expected `0x{x['expected']:08X}`, observed `0x{x['actual']:08X}`")
    if not f: lines.append('- No functional mismatches.')
    (outdir/f'regression_{rid}.md').write_text('\n'.join(lines)+'\n')
    return outdir/f'regression_{rid}.md'
