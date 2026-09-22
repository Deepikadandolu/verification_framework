from dataclasses import dataclass
from pathlib import Path

@dataclass
class Mutant:
    name:str; rtl:str; expected_detection:str

class MutationCampaign:
    def __init__(self, root):
        r=Path(root)
        self.mutants=[
            Mutant('stuck_at_0','rtl/alu_fault_stuck0.s','functional'),
            Mutant('stuck_at_1','rtl/alu_fault_stuck1.s','functional'),
            Mutant('add_to_sub','rtl/alu_fault_wrong_add.s','functional'),
        ]

    def run(self, regression_fn):
        results=[]
        for m in self.mutants:
            result=regression_fn(m.rtl)
            detected=(result['functional_failures']>0 or result['assertion_failures']>0 or result['timeouts']>0)
            results.append({'name':m.name,'rtl':m.rtl,'detected':detected,'mechanism':m.expected_detection})
        detected=sum(x['detected'] for x in results); total=len(results)
        return {'total':total,'detected':detected,'escaped':total-detected,'score_pct':round(100*detected/total,2) if total else 0,'results':results}
