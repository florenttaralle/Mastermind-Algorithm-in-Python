import numpy as np
from typing import Union
# ###############################################
from .game_config import GameConfig
from .code_list import CodeList
from .game_state import GameState
from .step import Step
from .code import Code
from .hash import Hash
# ###############################################

class Game:
    def __init__(self, cfg: GameConfig):
        self.cfg        = cfg
        self.codes      = CodeList(cfg)
        assert len(self.codes), 'No valid codes with this config'
        self.state      = None
        self.new()
    # ###############################################

    def new(self, code_id: int=None):
        if code_id is None:
            code_id = np.random.randint(0, len(self.codes))
        code = Code(code_id, self.codes[code_id])
        self.state = GameState(code)
        return self
    # ###############################################

    def __bool__(self) -> bool:
        return not self.state.over
    # ###############################################

    def __len__(self) -> int:
        return len(self.state.steps)
    # ###############################################
    
    def __iter__(self):
        return iter(self.state.steps)
    # ###############################################

    def __getitem__(self, idx) -> Step:
        return self.state.steps[idx]
    # ###############################################

    def guess(self, guess: Union[int, np.ndarray]) -> Step:
        assert not self.state.over, 'Game already terminated'
        # get the code from the code id or value
        if isinstance(guess, int):
            # guess is a code id
            guess = Code(guess, self.codes[guess])
        elif isinstance(guess, np.ndarray):
            # guess is a code value
            guess_id = ((self.codes == guess).sum(1) == self.cfg.code_length).nonzero()[0]
            assert len(guess_id), 'invalid code value'
            guess_id = guess_id[0]
            guess = Code(guess_id, guess)
        else:
            # invalid type provided
            assert TypeError('Invalid type for guess')

        # compute the hash
        hash = Hash.compute(guess, self.state.solution)
        # is it a win ?
        winner = guess.id == self.state.solution.id
        self.state.over = winner
        # build new step and add it to the history
        step = Step(len(self.state.steps) + 1, guess, hash, winner)
        self.state.steps.append(step)

        return step
    # ###############################################
