from collections import Counter
from .transaction import Op

class Coverage:
    def __init__(self):
        self.ops=Counter(); self.classes=Counter(); self.cross=Counter(); self.total=0
        self.expected_ops={o.name for o in Op}
        self.expected_classes={'zero','one','all_ones','max_pos','min_neg','random'}

    @staticmethod
    def operand_class(x):
        x &= 0xffffffff
        if x==0:return 'zero'
        if x==1:return 'one'
        if x==0xffffffff:return 'all_ones'
        if x==0x7fffffff:return 'max_pos'
        if x==0x80000000:return 'min_neg'
        return 'random'

    def sample(self,tx):
        self.total+=1; self.ops[tx.op_name]+=1
        for x in (tx.a,tx.b):
            c=self.operand_class(x); self.classes[c]+=1; self.cross[(tx.op_name,c)]+=1

    def missing_scenarios(self):
        return [f'{op}:{c}' for op in sorted(self.expected_ops) for c in sorted(self.expected_classes) if self.cross[(op,c)]==0]

    def summary(self):
        op_cov=len([o for o in self.expected_ops if self.ops[o]>0])/len(self.expected_ops)*100
        class_cov=len([c for c in self.expected_classes if self.classes[c]>0])/len(self.expected_classes)*100
        total_cross=len(self.expected_ops)*len(self.expected_classes)
        cross_cov=(total_cross-len(self.missing_scenarios()))/total_cross*100
        return {'tests_observed':self.total,'operation_coverage_pct':round(op_cov,2),'operand_class_coverage_pct':round(class_cov,2),'cross_coverage_pct':round(cross_cov,2),'operations':dict(self.ops),'operand_classes':dict(self.classes),'missing_cross':self.missing_scenarios()}
