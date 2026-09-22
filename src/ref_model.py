from .transaction import Transaction, Op
MASK=0xffffffff

def s32(x):
    x &= MASK
    return x - (1<<32) if x & (1<<31) else x

def predict(tx: Transaction):
    a,b=tx.a&MASK,tx.b&MASK
    if tx.op==Op.ADD: y=(a+b)&MASK
    elif tx.op==Op.SUB: y=(a-b)&MASK
    elif tx.op==Op.AND: y=a&b
    elif tx.op==Op.OR: y=a|b
    elif tx.op==Op.XOR: y=a^b
    elif tx.op==Op.SLT: y=1 if s32(a)<s32(b) else 0
    else: y=0xdeadbeef
    return y&MASK


def alu(a,b,op):
    """Compatibility helper for unit tests: raw ALU API."""
    return predict(Transaction(0,op,a,b,0)).__index__()
