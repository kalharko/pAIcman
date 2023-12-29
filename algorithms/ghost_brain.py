import random

from algorithms.brain import Brain
from back.perception import Perception
from utils.action import Action
from utils.direction import Direction


class GhostBrain(Brain):
    def __init__(self, agent_manager):
        super().__init__(agent_manager)

        # define hyper parameters
        self._EXPLORATION_FORGETTING_RATE = 0.1
        self._EXPLORATION_PAC_GUM_SCORE = 0
        self._EXPLORATION_PAC_DOT_SCORE = 0
        self._EXPLORATION_UNKNOWN_CELL_SCORE = 1
        self._EXPLORATION_LAST_CELL_VISITED_SCORE = -5

    def _defense(perception: Perception, agent_id: str) -> Action:
        """Give the best defensive action for the given agent

        :param perception: the team perception that the ghost agent will use to make its decision
        :type perception: Perception
        :param agent_id: id of the ghost agent
        :type agent_id: str
        :return: the optimal defensive action for the given agent
        :rtype: Action
        """
        return Action(agent_id, random.choice(list(Direction)))
