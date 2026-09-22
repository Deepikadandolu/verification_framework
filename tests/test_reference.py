from src.ref_model import alu

def test_add_wraparound():
    assert alu(0xFFFFFFFF, 1, 0) == 0

def test_sub_wraparound():
    assert alu(0, 1, 1) == 0xFFFFFFFF

def test_signed_slt():
    assert alu(0xFFFFFFFF, 1, 5) == 1
    assert alu(1, 0xFFFFFFFF, 5) == 0

def test_bitwise():
    assert alu(0xAA, 0x0F, 2) == 0x0A
    assert alu(0xAA, 0x0F, 3) == 0xAF
    assert alu(0xAA, 0x0F, 4) == 0xA5
