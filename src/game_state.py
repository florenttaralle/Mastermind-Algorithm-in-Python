from dataclasses import dataclass, field
from typing import List
# ###############################################
from .code import Code
from .step import Step
# ###############################################


@dataclass
class GameState:
    solution:   Code
    over:       bool = False
    steps:      List[Step] = field(default_factory=list)
    # ###############################################


