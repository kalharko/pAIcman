import sys
sys.path.append(sys.path[0].rstrip(sys.path[0].split('/')[-1]))

from back.pacman_game import PacmanGame
from back.direction import Direction
from back.action import Action
from back.pacman import Pacman
from back.ghost import Ghost

from front.cli.cli_replay import CliReplay

game = PacmanGame()
game.load_map('maps/original.txt')
game.set_agents([
    Pacman('Pa', 12, 23),
    Ghost('Gb', 11, 20)
    ])


game.step([Action('Pa', Direction['UP']), Action('Gb', Direction['RIGHT'])])
game.step([Action('Pa', Direction['UP']), Action('Gb', Direction['DOWN'])])
game.step([Action('Pa', Direction['UP']), Action('Gb', Direction['DOWN'])])
game.step([Action('Pa', Direction['UP']), Action('Gb', Direction['DOWN'])])

print('moved')

replay = CliReplay(game.get_replay())
