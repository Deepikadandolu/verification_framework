from src.transaction import Transaction,Op
from src.ref_model import predict
from src.generator import StimulusGenerator
from src.coverage import Coverage

def test_reference_ops():
    vals=[
      (Op.ADD,1,2,3),(Op.SUB,5,2,3),(Op.AND,0xF0,0x0F,0),
      (Op.OR,0xF0,0x0F,0xFF),(Op.XOR,0xAA,0x55,0xFF),(Op.SLT,0xffffffff,1,1)
    ]
    for op,a,b,e in vals: assert predict(Transaction(0,op,a,b,1))==e

def test_generator_and_coverage():
    txs=StimulusGenerator(7).generate(100)
    c=Coverage()
    for t in txs:c.sample(t)
    assert len(txs)==100
    assert c.summary()['operation_coverage_pct']==100
