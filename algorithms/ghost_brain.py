import random
from algorithms.brain import Brain
from back.perception import Perception
from utils.direction import Direction
from utils.strategy import Strategy
from utils.action import Action


class GhostBrain(Brain):
    def __init__(self):
        pass

    def compute_action(self, strategy: Strategy, perception: Perception, id: str) -> Action:
        """Decision making of a ghost agent for a given strategy

        :param strategy: strategy that the ghost agent will apply
        :type strategy: Strategy
        :param perception: the team perception that the ghost agent will use to make it's decision
        :type perception: Perception
        :param id: id of the ghost agent
        :type id: str
        :return: the optimal action for the ghost agent for the given strategy
        :rtype: Action
        """
        assert isinstance(strategy, Strategy)
        assert isinstance(perception, Perception)
        assert isinstance(id, str)

        if strategy == Strategy['RANDOM']:
            return Action(id, random.choice(list(Direction)))

        if strategy == Strategy['EXPLORATION']:
            return Action(id, random.choice(list(Direction)))

        if strategy == Strategy['AGRESSION']:
            return Action(id, random.choice(list(Direction)))

        if strategy == Strategy['DEFENSE']:
            return Action(id, random.choice(list(Direction)))

    def _exploration(perception: Perception, agent_id: str) -> Action:
        """Give the best exploration action for the given agent

        :param perception: the team perception that the ghost agent will use to make it's decision
        :type perception: Perception
        :param agent_id: id of the ghost agent
        :type agent_id: str
        :return: the optimal exploration action for the given agent
        :rtype: Action
        """
        return Action(agent_id, random.choice(list(Direction)))

    def _agression(perception: Perception, agent_id: str) -> Action:
        """Give the best agressive action for the given agent

        :param perception: the team perception that the ghost agent will use to make it's decision
        :type perception: Perception
        :param agent_id: id of the ghost agent
        :type agent_id: str
        :return: the optimal agressive action for the given agent
        :rtype: Action
        """
        return Action(agent_id, random.choice(list(Direction)))

    def _defense(perception: Perception, agent_id: str) -> Action:
        """Give the best defensive action for the given agent

        :param perception: the team perception that the ghost agent will use to make it's decision
        :type perception: Perception
        :param agent_id: id of the ghost agent
        :type agent_id: str
        :return: the optimal defensive action for the given agent
        :rtype: Action
        """
        return Action(agent_id, random.choice(list(Direction)))
