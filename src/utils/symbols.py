import numpy as np
from typing import Union
# ###############################################
from ..code import Code
# ###############################################


class Symbols:
    def __init__(self, symbols: str):
        self.symbols    = np.asarray(list(symbols))
    # ###############################################

    def __len__(self) -> int:
        return len(self.symbols)
    # ###############################################

    def __iter__(self):
        return iter(self.symbols)
    # ###############################################
    
    def __getitem__(self, idx) -> str:
        return self.symbols[idx]
    # ###############################################

    def __str__(self) -> str:
        return ''.join(self.symbols)
    # ###############################################
    
    def from_sym(self, sym: str) -> np.ndarray:
        Sm, Sr  = np.meshgrid(self.symbols, list(sym))
        _, code = np.nonzero(Sm == Sr)
        assert len(code) == len(sym), 'Invalid symbol'
        return code
    # ###############################################

    def to_sym(self, code: Union[np.ndarray, Code]) -> str:
        if isinstance(code, Code):
            code = code.value
        return ''.join(self.symbols[code])
    # ###############################################
