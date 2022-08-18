from tqdm import trange
from collections import Counter
import numpy as np
from argparse import ArgumentParser
# ###############################################
from src.game_config import GameConfig
from src.game import Game
from src.algorithm import Algorithm
from src.utils.symbols import Symbols
# ###############################################

parser = ArgumentParser()
parser.add_argument('-s', '--symbols', type=str, default='123456')
parser.add_argument('-l', '--code_length', type=int, default=4)
parser.add_argument('--no_doublon', action='store_true')
parser.add_argument('-f', '--first_guess', type=str, default=None)
args = parser.parse_args()
# ########################################

symbols = Symbols(args.symbols)
config = GameConfig(
    code_length     = args.code_length,
    symbol_count    = len(symbols), 
    doublons        = not args.no_doublon
)
game    = Game(config)
algo    = Algorithm()
# ########################################

if args.first_guess is not None:
    first_guess = symbols.from_sym(args.first_guess)
else:
    first_guess = None
# ########################################


nb_guesses  = []
for solution in trange(len(game.codes)):
    game.new(solution)
    last_step = algo.play(game, first_guess)
    nb_guesses.append(last_step.id)
# ########################################

first_guess = game[0].guess
print('First Guess: %s (%r)' % (
    symbols.to_sym(first_guess),
    first_guess
))
print('Mean: %.2f' % np.mean(nb_guesses))
print('Max:  %d' % max(nb_guesses))
# ########################################

# show the repartition of game lengthes
counter = Counter(nb_guesses)
for k in range(1, max(counter) + 1):
    nb  = counter.get(k, 0)
    prc = int(100 * nb / len(nb_guesses))
    print('%d: %3d%% (%d)' % (k, prc, nb))
# ########################################

# for a standard game, show the codes 
# where the algorithm was longer than 5 guesses
if config == GameConfig(4, 6, True):
    long_ids    = np.where(np.array(nb_guesses) > 5)[0]
    long_codes  = game.codes[long_ids]
    print(list(map(symbols.to_sym, long_codes)))
# ########################################

