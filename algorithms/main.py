from algorithms.perception import Perception
from back.agent import Agent
from back.pacman_game import PacmanGame
from back.pacman import Pacman
from back.ghost import Ghost
from utils.board import Board
from algorithms.pacman_brain import PacmanBrain
from algorithms.ghost_brain import GhostBrain
from utils.strategy import Strategy


class Main():
    perception_team_a: Perception
    perception_team_b: Perception
    id_team_a: tuple[str]
    id_team_b: tuple[str]
    brain_pacman: PacmanBrain
    brain_ghost: GhostBrain
    environment: PacmanGame

    def __init__(self) -> None:
        self.perception_team_a = Perception()
        self.perception_team_b = Perception()
        self.id_team_a = ('Pa', 'Ga1', 'Ga2', 'Ga3')
        self.id_team_b = ('Pb', 'Gb1', 'Gb2', 'Gb3')

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

    def simulation_cycle(self) -> None:
        # gather state
        board, agents = self.environment.gather_state()

        # mask perception for each agents
        ta_update = []
        tb_update = []
        for agent in agents:
            update = self.mask_perception(board, agent, agents)
            if agent.get_id() in self.id_team_a:
                ta_update.append(update)
            else:
                tb_update.append(update)

        # add to each team's perception
        for perception in ta_update:
            self.perception_team_a.update(perception)
        for perception in tb_update:
            self.perception_team_b.update(perception)

        # compute strategy
        strat_team_a = (Strategy['EXPLORATION'] for i in range(4))
        strat_team_b = (Strategy['EXPLORATION'] for i in range(4))

        # compute agent actions
        

        # apply to environment

    def mask_perception(self, board: Board, agent: Agent, agents: list[Agent]) -> Perception:
        pass
