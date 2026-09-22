from dataclasses import dataclass,asdict
from .ref_model import predict

@dataclass
class Failure:
    tid:int; cycle:int; op:str; a:int; b:int; expected:int; actual:int; category:str; reason:str

class Analyzer:
    def __init__(self): self.failures=[]
    def compare(self,tx,cycle,actual):
        expected=predict(tx)
        if expected != actual:
            f=Failure(tx.tid,cycle,tx.op_name,tx.a,tx.b,expected,actual,tx.category,'functional_mismatch')
            self.failures.append(f); return f
        return None
    def as_dict(self): return [asdict(f) for f in self.failures]
