import numpy as np
from itertools import product
# ###############################################
from .game_config import GameConfig
# ###############################################


class CodeList(np.ndarray):
    def __new__(cls, cfg: GameConfig):
        symbols = list(range(cfg.symbol_count))
        codes   = product(*[symbols] * cfg.code_length)
        if not cfg.doublons:
            no_doublon = lambda code: len(set(code)) == cfg.code_length
            codes = filter(no_doublon, codes)
        codes = np.array(list(codes)).view(cls)
        return codes
    # ###############################################

    def __init__(self, cfg: GameConfig):
        # __new__ is used, this is just for auto-completion
        pass
    # ###############################################

    def to_id(self, code: np.ndarray) -> int:
        try:
            id = np.where((self == code).sum(1) == self.shape[1])[0][0]
            return int(id)
        except:
            raise Exception('unknown code')
    # ###############################################
