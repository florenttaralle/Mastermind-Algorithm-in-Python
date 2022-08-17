import sys
from typing import FrozenSet
# ###############################################
from ..game_config import GameConfig
from .symbols import Symbols
# ###############################################

class CustomInput:
    def __init__(self, config: GameConfig, symbols: Symbols,
        keywords: FrozenSet[str]=set(), exit_keyword='exit'):
        self.config         = config
        self.symbols        = symbols
        self.keywords       = set([*keywords, exit_keyword])
        self.exit_keyword   = exit_keyword
    # ###############################################

    def __call__(self) -> str:
        guess = None
        while guess is None:
            try:
                guess = input('Next guess: ')
                # erase 'input' line
                sys.stdout.write("\033[F")
                sys.stdout.write("\x1b[2K")

                if guess not in self.keywords:
                    assert len(guess) == self.config.code_length, \
                        'Invalid length (expected %d)' % self.config.code_length
                    self.symbols.from_sym(guess)

            except KeyboardInterrupt:
                guess = self.exit_keyword

            except Exception as what:
                print('Invalid guess (%s)' % what)
                guess = None

        return guess
    # ###############################################
