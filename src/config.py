from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    tests:int=500
    seed:int=18473
    adaptive:bool=True
    timeout_cycles:int=100000
    workdir:Path=Path('reports')
