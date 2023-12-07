import sys
sys.path.append(sys.path[0].rstrip(sys.path[0].split('/')[-1]))

from back.pacman_game import PacmanGame
from utils.direction import Direction
from utils.action import Action
from back.pacman import Pacman
from back.ghost import Ghost

from front.cli.cli_replay import CliReplay


game = PacmanGame()
game.load_map('maps/collisions.txt')
game.step([Action('Pa', Direction['RIGHT']), Action('Pb', Direction['UP'])])
game.step([Action('Pa', Direction['RIGHT']), Action('Pb', Direction['UP'])])
game.step([Action('Pa', Direction['LEFT']), Action('Pb', Direction['DOWN'])])

replay = CliReplay(game)
