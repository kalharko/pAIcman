import sys
sys.path.append(sys.path[0].rstrip(sys.path[0].split('/')[-1]))

from back.pacman_game import PacmanGame
from utils.direction import Direction
from utils.action import Action
from back.pacman import Pacman
from back.ghost import Ghost
from utils.replay_logger import ReplayLogger


from front.cli.cli_replay import CliReplay

game_map = 'maps/collisions.txt'

game = PacmanGame()
game.load_map(game_map)
ReplayLogger().log_map(game_map)

actions = [Action('Pa', Direction['RIGHT']), Action('Pb', Direction['UP'])]
game.step(actions)
ReplayLogger().log_step(actions)

actions = [Action('Pa', Direction['RIGHT']), Action('Pb', Direction['UP'])]
game.step(actions)
ReplayLogger().log_step(actions)

actions = [Action('Pa', Direction['LEFT']), Action('Pb', Direction['DOWN'])]
game.step(actions)
ReplayLogger().log_step(actions)

actions = [Action('Pa', Direction['LEFT']), Action('Pb', Direction['DOWN'])]
game.step(actions)
ReplayLogger().log_step(actions)

replay = CliReplay('dark')
