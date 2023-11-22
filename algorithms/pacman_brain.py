import random
from algorithms.brain import Brain
from back.agent_manager import AgentManager
from back.perception import Perception
from utils.action import Action
from utils.direction import Direction
from utils.strategy import Strategy


class PacmanBrain(Brain):
    _agentManager: AgentManager

    def __init__(self, agentManager):
        self._agentManager = agentManager

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

    def _exploration(self, perception: Perception, agent_id: str) -> Action:
        """Give the best exploration action for the given agent

        :param perception: the team perception that the pacman agent will use to make it's decision
        :type perception: Perception
        :param agent_id: id of the pacman agent
        :type agent_id: str
        :return: the optimal exploration action for the given agent
        :rtype: Action
        """

        bestScore = 0
        choosenDirection = Direction.NONE
        for direction in self.get_legal_move(perception, agent_id):  # TODO : shuffle the order of move
            if self.get_exploration_score(perception, agent_id, direction) >= bestScore:
                choosenDirection = direction

        return Action(agent_id, choosenDirection)

    def get_exploration_score(self, perception: Perception, agent_id: str, direction: Direction) -> int:
        return 1

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

    def get_legal_move(self, perception: Perception, agent_id: str, ) -> list[Direction]:
        (agentX, agentY) = self._agentManager.get_agent(agent_id).get_position()
        return perception.get_board().get_legal_move(agentX, agentY)
