from dataclasses import dataclass
# ###############################################
from .code import Code
from .hash import Hash
# ###############################################


@dataclass
class Step:
    id:     int
    guess:  Code
    hash:   Hash
    winner: bool = False
    # ###############################################


