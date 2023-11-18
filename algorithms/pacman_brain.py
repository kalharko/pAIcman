import random
from algorithms.brain import Brain
from back.perception import Perception
from utils.action import Action
from utils.direction import Direction
from utils.strategy import Strategy


class PacmanBrain(Brain):
    def __init__(self):
        pass

    def compute_action(self, strategy: Strategy, perception: Perception, agent_id: str) -> Action:
        """Decision making of a pacman agent for a given strategy

        :param strategy: strategy that the pacman agent will apply
        :type strategy: Strategy
        :param perception: the team perception that the pacman agent will use to make it's decision
        :type perception: Perception
        :param agent_id: id of the pacman agent
        :type agent_id: str
        :return: the optimal action for the pacman agent for the given strategy
        :rtype: Action
        """
        assert isinstance(strategy, Strategy)
        assert isinstance(perception, Perception)
        assert isinstance(agent_id, str)

        if strategy == Strategy['RANDOM']:
            return Action(agent_id, random.choice(list(Direction)))

        if strategy == Strategy['EXPLORATION']:
            return self._exploration(perception, agent_id)

        if strategy == Strategy['AGRESSION']:
            return self._agression(perception, agent_id)

        if strategy == Strategy['DEFENSE']:
            return self._defense(perception, agent_id)

    def _exploration(perception: Perception, agent_id: str) -> Action:
        """Give the best exploration action for the given agent

        :param perception: the team perception that the pacman agent will use to make it's decision
        :type perception: Perception
        :param agent_id: id of the pacman agent
        :type agent_id: str
        :return: the optimal exploration action for the given agent
        :rtype: Action
        """
        return Action(agent_id, random.choice(list(Direction)))

    def _agression(perception: Perception, agent_id: str) -> Action:
        """Give the best agressive action for the given agent

        :param perception: the team perception that the pacman agent will use to make it's decision
        :type perception: Perception
        :param agent_id: id of the pacman agent
        :type agent_id: str
        :return: the optimal agressive action for the given agent
        :rtype: Action
        """
        return Action(agent_id, random.choice(list(Direction)))

    def _defense(perception: Perception, agent_id: str) -> Action:
        """Give the best defensive action for the given agent

        :param perception: the team perception that the pacman agent will use to make it's decision
        :type perception: Perception
        :param agent_id: id of the pacman agent
        :type agent_id: str
        :return: the optimal defensive action for the given agent
        :rtype: Action
        """
        return Action(agent_id, random.choice(list(Direction)))
