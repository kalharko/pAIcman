import sys
sys.path.append(sys.path[0].rstrip(sys.path[0].split('/')[-1]))

from algorithms.perception import Perception
from back.agent import Agent
from back.pacman_game import PacmanGame
from back.pacman import Pacman
from back.ghost import Ghost
from utils.board import Board
from algorithms.pacman_brain import PacmanBrain
from algorithms.ghost_brain import GhostBrain
from utils.strategy import Strategy
from front.cli.cli_replay import CliReplay


class Main():
    perception_team_a: Perception
    perception_team_b: Perception
    id_team_a: tuple[str]
    id_team_b: tuple[str]
    brain_pacman: PacmanBrain
    brain_ghost: GhostBrain
    environment: PacmanGame

    def __init__(self) -> None:
        # set up environment
        self.environment = PacmanGame()
        self.environment.load_map('maps/original.txt')
        self.environment.set_agents([
            Pacman(0, 'Pa', 26, 29),
            Ghost(0, 'Ga1', 23, 26),
            Ghost(0, 'Ga2', 6, 26),
            Ghost(0, 'Ga3', 1, 8),
            Pacman(1, 'Pb', 1, 1),
            Ghost(1, 'Gb1', 12, 5),
            Ghost(1, 'Gb2', 26, 5),
            Ghost(1, 'Gb3', 1, 29)])

        # ids
        self.id_team_a = ('Pa', 'Ga1', 'Ga2', 'Ga3')
        self.id_team_b = ('Pb', 'Gb1', 'Gb2', 'Gb3')
        self.ids = tuple(list(self.id_team_a) + list(self.id_team_b))
        self.id_pacmans = ('Pa', 'Pb')

        # other
        self.perception_team_a = Perception(self.environment.get_board_size(), self.ids)
        self.perception_team_b = Perception(self.environment.get_board_size(), self.ids)
        self.brain_ghost = GhostBrain()
        self.brain_pacman = PacmanBrain()

    def simulation_cycle(self) -> None:
        # gather state
        visions = self.environment.gather_state()

        # add to each team's perception
        self.perception_team_a.step_time()
        self.perception_team_b.step_time()
        for id, board, agents_seen in visions:
            if id in self.id_team_a:
                self.perception_team_a.update(board, agents_seen)
            else:
                self.perception_team_b.update(board, agents_seen)

        # compute strategy
        # TODO
        strat_team_a = ((id, Strategy['RANDOM']) for id in self.id_team_a)
        strat_team_b = ((id, Strategy['RANDOM']) for id in self.id_team_b)

        # compute agent actions
        actions = []
        for id, strat in strat_team_a:
            if id in self.id_pacmans:
                actions.append(self.brain_pacman.compute_action(strat, self.perception_team_a, id))
            else:
                actions.append(self.brain_ghost.compute_action(strat, self.perception_team_a, id))
        for id, strat in strat_team_b:
            if id in self.id_pacmans:
                actions.append(self.brain_pacman.compute_action(strat, self.perception_team_a, id))
            else:
                actions.append(self.brain_ghost.compute_action(strat, self.perception_team_a, id))

        # apply to environment
        print(actions)
        self.environment.step(actions)

    def mask_perception(self, board: Board, agent: Agent, agents: list[Agent]) -> Perception:
        pass


if __name__ == '__main__':
    main = Main()
    for i in range(80):
        main.simulation_cycle()
        input()
    replay = CliReplay(main.environment)
