import sys
sys.path.append(sys.path[0].rstrip(sys.path[0].split('/')[-1]))

from back.pacman_game import PacmanGame
from back.direction import Direction
from back.action import Action

from front.cli.cli_replay import CliReplay


game = PacmanGame()
game.load('maps/original.txt')

game.step([Action('Pa', Direction['LEFT'])])
game.step([Action('Pa', Direction['UP'])])
game.step([Action('Pa', Direction['UP'])])
game.step([Action('Pa', Direction['UP'])])
game.step([Action('Pa', Direction['LEFT'])])
game.step([Action('Pa', Direction['LEFT'])])
game.step([Action('Pa', Direction['LEFT'])])
game.step([Action('Pa', Direction['UP'])])
game.step([Action('Pa', Direction['UP'])])
game.step([Action('Pa', Direction['UP'])])
game.step([Action('Pa', Direction['UP'])])
game.step([Action('Pa', Direction['UP'])])
game.step([Action('Pa', Direction['UP'])])
game.step([Action('Pa', Direction['LEFT'])])
game.step([Action('Pa', Direction['LEFT'])])
game.step([Action('Pa', Direction['LEFT'])])
game.step([Action('Pa', Direction['LEFT'])])

replay = CliReplay(game.get_replay())
