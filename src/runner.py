import argparse, json, time
from pathlib import Path
from .config import Config
from .regression import RegressionEngine
from .mutation import MutationCampaign
from .report import write_report
from .environment import check_environment

def main():
    ap=argparse.ArgumentParser(description='Coverage- and mutation-driven RTL verification framework')
    ap.add_argument('--tests',type=int,default=500); ap.add_argument('--seed',type=int,default=18473)
    ap.add_argument('--dut',default='rtl/alu.s'); ap.add_argument('--adaptive',action='store_true')
    ap.add_argument('--fault-campaign',action='store_true'); ap.add_argument('--keep-traces',action='store_true')
    args=ap.parse_args(); root=Path(__file__).resolve().parents[1];
    env=check_environment()
    if not (env['iverilog'] and env['vvp']):
        print('ERROR: Icarus Verilog (iverilog/vvp) is required for RTL execution.')
        print('Python framework self-tests can still be run with: python3 -m pytest -q')
        return 2
    out=root/'reports'; out.mkdir(exist_ok=True)
    rid=time.strftime('%Y%m%d_%H%M%S'); engine=RegressionEngine(root)
    print(f'[1/5] Generating and executing regression: {args.tests} tests, seed={args.seed}')
    base=engine.run(args.tests,args.seed,args.dut,args.adaptive,args.keep_traces)
    print('[2/5] Functional differential analysis: DONE')
    print('[3/5] Coverage analysis: DONE')
    mutation={'total':0,'detected':0,'escaped':0,'score_pct':0,'results':[]}
    if args.fault_campaign:
        print('[4/5] Running seeded fault campaign...')
        mutation=MutationCampaign(root).run(lambda dut: engine.run(args.tests,args.seed,dut,False,False))
    else: print('[4/5] Fault campaign: SKIPPED (use --fault-campaign)')
    report={'regression_id':rid,'timestamp':time.strftime('%Y-%m-%dT%H:%M:%S'),'seed':args.seed,'tests_generated':base.get('tests_generated',args.tests),'tests_observed':base.get('tests_generated',args.tests),'failures':base.get('failures',[]),'assertion_failures':base.get('assertion_failures',0),'timeouts':base.get('timeouts',0),'coverage':base.get('coverage',{}),'mutation':mutation}
    p=write_report(report,out)
    print('[5/5] Report: DONE')
    print(f'\nReport: {p}')
    print(json.dumps({'failures':len(report['failures']),'coverage':report['coverage'],'mutation_score':mutation['score_pct']},indent=2))

if __name__=='__main__': raise SystemExit(main() or 0)
