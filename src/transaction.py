from dataclasses import dataclass
from enum import IntEnum

class Op(IntEnum):
    ADD=0; SUB=1; AND=2; OR=3; XOR=4; SLT=5

OP_NAMES={o.value:o.name for o in Op}

@dataclass(frozen=True)
class Transaction:
    tid:int
    op:int
    a:int
    b:int
    seed:int
    category:str='random'

    def normalized(self):
        return Transaction(self.tid,self.op,self.a & 0xffffffff,self.b & 0xffffffff,self.seed,self.category)

    @property
    def op_name(self): return OP_NAMES.get(self.op, f'OP_{self.op}')

    def to_vector(self):
        t=self.normalized()
        return f"{t.tid} {t.op} {t.a:08x} {t.b:08x}\n"
