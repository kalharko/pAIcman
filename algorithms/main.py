from algorithms.perception import Perception
from back.pacman_game import PacmanGame
from back.pacman import Pacman
from back.ghost import Ghost
from utils.board import Board


class Main():
    team_a_perception: Perception
    team_b_perception: Perception
    environment: PacmanGame

    def __init__(self) -> None:
        self.team_a_perception = Perception()
        self.team_b_perception = Perception()

        # set up environment
        self.environment = PacmanGame()
        self.environment.load_map('maps/original.txt')
        self.environment.set_agents([
            Pacman('Pa', 26, 29),
            Ghost('Ga1', 23, 26),
            Ghost('Ga2', 6, 26),
            Ghost('Ga3', 1, 8),
            Pacman('Pb', 1, 1),
            Ghost('Gb1', 12, 5),
            Ghost('Gb2', 26, 5),
            Ghost('Gb3', 1, 29)])

    def run(self) -> None:
        # simulation cycle
        state = self.environment.gather_state()

    def mask_perception(self, board: Board) -> None:
        pass
