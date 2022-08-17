import numpy as np
from typing import Callable
# ###############################################
from .game import Game, Step
from .hash_table import HashTable
# ###############################################


class Algorithm:
    def __init__(self, game: Game=None):
        self.game       = None
        self.hashes     = None
        self.C          = None # list of compatible solutions
        if self.game is not None:
            self.reset(game)
    # ###############################################

    def reset(self, game: Game=None):
        # if game changes, replace it
        if game is not None: 
            # re-compute hash-tables only if required
            if (self.game is None) or (game.cfg != self.game.cfg):
                self.hashes = HashTable(game.codes)
            self.game = game        
        # check that a game has been provided 
        assert self.game is not None, 'Must provide a game'
        assert not self.game.state.over, 'Game already over'
        # initilize id arrays
        self.C      = np.arange(len(game.codes))
        # use game history
        for step in game.state.steps:
            self.update(step)

        return self
    # ###############################################

    def update(self, step: Step):
        # filter remaining compatible solutions
        if not step.winner:
            # keep only solutions sharing the same hash
            M_wp    = self.hashes.M_wp[step.guess.id, self.C]
            M_ip    = self.hashes.M_ip[step.guess.id, self.C]
            keep    = (M_wp == step.hash.wp) & \
                    (M_ip == step.hash.ip) & \
                    (self.C != step.guess.id)

            self.C  = self.C[keep]
        else:
            self.C = np.array([step.guess.id])
    # ###############################################

    @staticmethod
    def row_heuristic(row: np.ndarray) -> float:
        """ Heuristic that determines the strength of a guess
            The LOWER the value, the BETTER the guess
            Re-implements this method to change the strategy

            Here we use an agreement score.
            This is the best heuristic so faar.
        """
        _, group_sizes  = np.unique(row, return_counts=True)
        agreement    = (group_sizes**2).sum()
        return agreement
    # ###############################################

    def next_guess(self) -> int:
        """ select the next guess so that
            it brings as much information as possible
            it selects the guess that minimizes "hash agreement score"
        """
        M_h         = self.hashes.M_h[self.C][:, self.C]
        heuristics  = np.apply_along_axis(self.row_heuristic, 0, M_h)
        id          = np.argmin(heuristics)
        guess_id    = int(self.C[id])
        
        return guess_id
    # ###############################################

    def play(self, game: Game=None, 
        first_guess: np.ndarray=None,
        callback: Callable[[Step], None]=None):

        self.reset(game)
        while game:
            if (first_guess is not None) and (len(self.game.state.steps) == 0):
                guess = first_guess
            else:
                guess = self.next_guess()
            step = game.guess(guess)
            self.update(step)
            if callback is not None:
                callback(step)

        return step # the last step
    # ###############################################

    def summary_grid(self) -> np.ndarray:
        """ 
            counts[symbol, position] = nb code with this symbol at that position
        """
        symbols = np.arange(self.game.cfg.symbol_count)
        nS      = len(symbols)
        codes   = self.game.codes[self.C]
        nC, nP  = codes.shape
        codes   = np.stack([codes.T] * nS)
        symbols = symbols.repeat(nC*nP).reshape((nS, nP, nC))
        counts  = (codes == symbols).sum(axis=-1)
        return counts
    # ###############################################