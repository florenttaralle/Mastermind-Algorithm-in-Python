from argparse import ArgumentParser
from termcolor import colored
from itertools import count, compress
# ###############################################
from src.game_config import GameConfig
from src.algorithm import Algorithm
from src.game import Game
from src.utils.symbols import Symbols
from src.utils.custom_input import CustomInput
# ###############################################

def grid_colormap(level: float) -> str:
    if level >= 0.66: return 'green'
    if level >= 0.33: return 'yellow'
    if level >= 0.01: return 'blue'
    return 'grey'
# ###############################################

def show_grid(symbols: Symbols, algo: Algorithm,
    prefix='', suffix='', short=True):
    
    grid = algo.summary_grid()

    if short:
        used    = grid.sum(1) > 0
        grid    = grid[used]
        symbols = compress(symbols, used)

    grid = grid / grid.sum(0) # normalise columns

    for symbol, row in zip(symbols, grid):
        print('%s%s%s' % (
            prefix, 
            ''.join([
                colored(symbol, grid_colormap(col))
                for col in row
            ]), 
            suffix
        ))
# ###############################################


def play_one_game(game_id: int, 
    symbols: Symbols, game: Game, 
    algo: Algorithm, input: CustomInput) -> bool:

    game.new()
    algo.reset(game)

    print('#' * 50)
    print('New Game (%d) !' % game_id)
    print('Write your guess as a string of %d symbols in %s with no spaces' % (
        game.cfg.code_length, symbols))
    print('> Ctrl+C or "exit" to show solution and exit')
    print('> "help" for the computer to play something for you')
    print('> "grid" to show an helping table')

    while game:
        guess_sym   = input()
        
        if guess_sym == 'exit':
            break
        elif guess_sym == 'grid':
            show_grid(symbols, algo, 
                colored(' ' * 15 + '|', 'yellow'), 
                colored('|', 'yellow'))
            continue
        elif guess_sym == 'help':
            guess = algo.next_guess()
            helped = True
        else:
            guess = symbols.from_sym(guess_sym)
            helped = False
        
        step = game.guess(guess)
        algo.update(step)

        color = 'yellow' if helped else 'blue'
        print('Step %2d, guess: %s, %s, %s, %s' % (
            step.id,
            colored(symbols.to_sym(step.guess.value), color),
            colored('%d well placed' % step.hash.wp, 'green'),
            colored('%3d ill-placed' % step.hash.ip, 'yellow'),
            '%d remaining hypothesis' % len(algo.C)
        ))

    if not game:
        print(colored('You won in %d steps' % len(game), 'green'))
        return True
    else:
        print(colored('Solution was: %s' % game.state.solution, 'yellow'))
        return False
# ###############################################


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-s', '--symbols', type=str, default='123456')
    parser.add_argument('-l', '--code_length', type=int, default=4)
    parser.add_argument('--no_doublon', action='store_true')
    parser.add_argument('-n', '--nb_games', type=int, default=None)
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
    input   = CustomInput(config, symbols, {'help', 'grid'}, 'exit')
    # ########################################

    for gid in range(args.nb_games) if args.nb_games else count():
        keep_playing = play_one_game(gid + 1, symbols, game, algo, input)
        if not keep_playing: break
    # ########################################
