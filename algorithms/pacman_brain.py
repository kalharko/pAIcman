import random
import copy
from algorithms.brain import Brain
from back.agent_manager import AgentManager
from back.perception import Perception
from utils.action import Action
from utils.direction import Direction
from utils.strategy import Strategy
from utils.replay_logger import ReplayLogger
from back.cell import Cell
from back.team import Team


class PacmanBrain(Brain):

    def __init__(self, agent_manager):
        super().__init__(agent_manager)

        #define hyper parameters
        self._EXPLORATION_FORGETHING_RATE = 0.5
        self._EXPLORATION_PAC_GUM_SCORE = 1
        self._EXPLORATION_PAC_DOT_SCORE = -1
        self._EXPLORATION_UNKNOWN_CELL_SCORE = 1
        self._EXPLORATION_LAST_CELL_VISITED_SCORE = -2



    def _agression(perception: Perception, agent_id: str) -> Action:
        """Give the best agressive action for the given agent

        :param perception: the team perception that the pacman agent will use to make its decision
        :type perception: Perception
        :param agent_id: id of the pacman agent
        :type agent_id: str
        :return: the optimal agressive action for the given agent
        :rtype: Action
        """
        return Action(agent_id, random.choice(list(Direction)))

    def _defense(perception: Perception, agent_id: str) -> Action:
        """Give the best defensive action for the given agent

        :param perception: the team perception that the pacman agent will use to make its decision
        :type perception: Perception
        :param agent_id: id of the pacman agent
        :type agent_id: str
        :return: the optimal defensive action for the given agent
        :rtype: Action
        """
        return Action(agent_id, random.choice(list(Direction)))


