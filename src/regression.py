import csv, shutil, subprocess, tempfile
from pathlib import Path
from .ref_model import predict
from .analyzer import Analyzer
from .coverage import Coverage
from .generator import StimulusGenerator

class RegressionEngine:
    def __init__(self, root): self.root=Path(root)

    def run(self, tests, seed, dut='rtl/alu.s', adaptive=True, keep=False):
        work=Path(tempfile.mkdtemp(prefix='p3reg_')); vec=work/'vectors.txt'; results=work/'rtl_results.txt'; sim=work/'sim.out'
        gen=StimulusGenerator(seed,adaptive=False); txs=gen.generate(tests)
        cov=Coverage()
        for tx in txs: cov.sample(tx)
        if adaptive:
            missing=cov.missing_scenarios()
            if missing:
                txs += StimulusGenerator(seed+1,adaptive=True).generate(max(1,tests//5),len(txs),cov)
                for tx in txs[-max(1,tests//5):]: cov.sample(tx)
        vec.write_text(''.join(t.to_vector() for t in txs))
        # Build a temporary TB that instantiates the requested module name through a stable alias.
        tb=(self.root/'tb/alu_tb.sv').read_text().replace('alu dut(', 'dut_alias dut(')
        wrapper=work/'tb.sv'; wrapper.write_text(tb)
        # Wrapper module exposes a stable dut_alias name while allowing any compatible source module.
        alias=work/'alias.sv'; alias.write_text(f'''module dut_alias(input logic clk,rst_n,valid,ready,input logic [31:0] a,b,input logic [2:0] op,output logic out_valid,output logic [31:0] y);\n  {Path(dut).stem} u(.clk(clk),.rst_n(rst_n),.valid(valid),.ready(ready),.a(a),.b(b),.op(op),.out_valid(out_valid),.y(y));\nendmodule\n''')
        compile_cmd=['iverilog','-g2012','-s','alu_tb','-o',str(work/'simv'),str(self.root/dut),str(alias),str(wrapper)]
        try:
            cp=subprocess.run(compile_cmd,capture_output=True,text=True,timeout=30)
            if cp.returncode!=0:
                return {'functional_failures':0,'assertion_failures':1,'timeouts':0,'compile_error':cp.stderr,'coverage':cov.summary()}
            run=subprocess.run(['vvp',str(work/'simv')],cwd=work,capture_output=True,text=True,timeout=30)
            if run.returncode!=0:
                return {'functional_failures':0,'assertion_failures':0,'timeouts':1,'runtime_error':run.stderr,'coverage':cov.summary()}
            # Results are keyed by transaction id. The simple DUT has one output per accepted transaction.
            actual={}
            if results.exists():
                for row in csv.reader(results.open()):
                    if len(row)>=3: actual[int(row[0])]=(int(row[1]),int(row[2],16))
            analyzer=Analyzer()
            for tx in txs:
                if tx.tid not in actual:
                    analyzer.failures.append(__import__('src.analyzer',fromlist=['Failure']).Failure(tx.tid,-1,tx.op_name,tx.a,tx.b,predict(tx),0,tx.category,'missing_output_or_timeout'))
                else: analyzer.compare(tx,actual[tx.tid][0],actual[tx.tid][1])
            assertion_failures=sum(1 for line in run.stdout.splitlines() if line.startswith('ASSERT_FAIL'))
            return {'functional_failures':len(analyzer.failures),'assertion_failures':assertion_failures,'timeouts':0,'failures':analyzer.as_dict(),'coverage':cov.summary(),'tests_generated':len(txs),'stdout':run.stdout}
        finally:
            if keep:
                dst=self.root/'reports'/'traces'/work.name; dst.mkdir(parents=True,exist_ok=True)
                for p in work.iterdir(): shutil.copy2(p,dst/p.name)
            else: shutil.rmtree(work,ignore_errors=True)
