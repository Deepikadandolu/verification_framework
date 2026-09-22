import random
from collections import Counter
from .transaction import Transaction, Op

BOUNDARIES=[0,1,2,0x7fffffff,0x80000000,0xfffffffe,0xffffffff,0xaaaaaaaa,0x55555555]

class StimulusGenerator:
    def __init__(self, seed=18473, adaptive=False):
        self.seed=seed; self.rng=random.Random(seed); self.adaptive=adaptive
        self.weights=Counter()

    def _operand_class(self, x):
        x &= 0xffffffff
        if x==0:return 'zero'
        if x==1:return 'one'
        if x==0xffffffff:return 'all_ones'
        if x==0x7fffffff:return 'max_pos'
        if x==0x80000000:return 'min_neg'
        return 'random'

    def generate(self,n,start_tid=0,coverage=None):
        ops=list(range(6)); out=[]
        missing=set(coverage.missing_scenarios()) if coverage else set()
        for i in range(n):
            tid=start_tid+i
            # Directed seeds: guarantee all operations and boundary classes appear.
            if i < 6:
                op=i; a=BOUNDARIES[i]; b=BOUNDARIES[(i+1)%len(BOUNDARIES)]; cat='directed_op'
            elif i < 6+len(BOUNDARIES):
                op=self.rng.randrange(6); a=BOUNDARIES[i-6]; b=self.rng.choice(BOUNDARIES); cat='corner'
            elif self.adaptive and missing:
                scenario=self.rng.choice(sorted(missing))
                opname,cls=scenario.split(':',1); op=next(o.value for o in Op if o.name==opname)
                a=self.rng.choice(BOUNDARIES) if cls!='random' else self.rng.getrandbits(32)
                b=self.rng.choice(BOUNDARIES) if cls!='random' else self.rng.getrandbits(32)
                cat='coverage_directed'
            else:
                op=self.rng.randrange(6)
                # 35% corner-biased, 65% unconstrained random.
                if self.rng.random()<0.35:
                    a=self.rng.choice(BOUNDARIES); b=self.rng.choice(BOUNDARIES)
                else:
                    a=self.rng.getrandbits(32); b=self.rng.getrandbits(32)
                cat='random'
            out.append(Transaction(tid,op,a,b,self.seed,cat).normalized())
        return out
