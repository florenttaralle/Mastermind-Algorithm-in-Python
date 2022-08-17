from tqdm import trange
from collections import Counter
import numpy as np
# ###############################################
from src.game_config import GameConfig
from src.game import Game
from src.algorithm import Algorithm
# ###############################################

config      = GameConfig(4, 6, True)
game        = Game(config)
algo        = Algorithm()
first_guess = np.array([0, 0, 1, 2])
nb_guesses  = []

for solution in trange(len(game.codes)):
    game.new(solution)
    last_step = algo.play(game, first_guess)
    nb_guesses.append(last_step.id)

print('First Guess:', game[0].guess)

print('Mean: %.2f' % np.mean(nb_guesses))
print('Min:  %d' % min(nb_guesses))
print('Max:  %d' % max(nb_guesses))

counter = Counter(nb_guesses)
for k in range(1, max(counter) + 1):
    nb  = counter.get(k, 0)
    prc = int(100 * nb / len(nb_guesses))
    print('%d: %3d%% (%d)' % (k, prc, nb))

long_ids    = np.where(np.array(nb_guesses) > 5)[0]
long_codes  = game.codes[long_ids]
print(list(map(lambda c: ''.join(map(str, c)), long_codes)))
