from argparse import ArgumentParser
# ###############################################
from src.game_config import GameConfig
from src.game import Game
from src.algorithm import Algorithm, Step
from src.utils.chrono import Chrono
from src.utils.symbols import Symbols
# ###############################################

parser = ArgumentParser()
parser.add_argument('-s', '--symbols', type=str, default='123456')
parser.add_argument('-l', '--code_length', type=int, default=4)
parser.add_argument('--no_doublon', action='store_true')
parser.add_argument('-c', '--code', type=str, default=None)
args = parser.parse_args()
# ########################################

chrono = Chrono()

with chrono:
    symbols = Symbols(args.symbols)
    config = GameConfig(
        code_length     = args.code_length,
        symbol_count    = len(symbols), 
        doublons        = not args.no_doublon
    )
    game    = Game(config)
    algo    = Algorithm()

    if args.code is not None:
        code    = symbols.from_sym(args.code)
        code_id = game.codes.to_id(code)
        game.new(code_id)

print('Prepared in %s' % chrono.value)

def print_step(step: Step):
    print('step: %2d, guess:%s hash:%s, remaining:%4d/%d' % (
        step.id, symbols.to_sym(step.guess.value), step.hash, 
        len(algo.C), len(game.codes)
    ))

algo.play(game, None, print_step)
