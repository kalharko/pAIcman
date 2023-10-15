import random
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
    Pacman('Pa', 26, 29),
    Ghost('Ga1', 23, 26),
    Ghost('Ga2', 6, 26),
    Ghost('Ga3', 1, 8),
    Pacman('Pb', 1, 1),
    Ghost('Gb1', 12, 5),
    Ghost('Gb2', 26, 5),
    Ghost('Gb3', 1, 29)])

for loop in range(200):
    game.step([Action(agent, random.choice(list(Direction))) for agent in 'Pa Pb Ga1 Ga2 Ga3 Gb1 Gb2 Gb3'.split(' ')])

replay = CliReplay(game.get_replay())
