import random
from algorithms.brain import Brain
from back.agent_manager import AgentManager
from back.perception import Perception
from utils.action import Action
from utils.direction import Direction
from utils.strategy import Strategy


class PacmanBrain(Brain):
    _agentManager: AgentManager

    def __init__(self, agent_manager):
        self._agentManager = agent_manager

    def compute_action(self, strategy: Strategy, perception: Perception, agent_id: str) -> Action:
        """Decision-making of a pacman agent for a given strategy

        :param strategy: strategy that the pacman agent will apply
        :type strategy: Strategy
        :param perception: the team perception that the pacman agent will use to make its decision
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

        :param perception: the team perception that the pacman agent will use to make its decision
        :type perception: Perception
        :param agent_id: id of the pacman agent
        :type agent_id: str
        :return: the optimal exploration action for the given agent
        :rtype: Action
        """

        bestScore = 0
        chosenDirection = Direction.NONE
        for direction in self.get_legal_move(perception, agent_id):  # TODO : shuffle the order of move
            if self.get_exploration_score(perception, agent_id, self.get_agent_position(agent_id), direction,
                                          []) >= bestScore:
                chosenDirection = direction

        return Action(agent_id, chosenDirection)

    def get_exploration_score(self, perception: Perception, agent_id: str, position: (int, int), direction: Direction,
                              already_visited: [(int, int)]) -> float:
        forgetting_rate = 0.5
        next_cell = perception.get_board().get_next_cell(position, direction)

        # stop case 1 : if is next cell non-legal
        if not perception.get_board().get_cell(position).is_movable():
            return 0.0

        # stop case 2 : if the cell is already visited
        elif already_visited.search(next_cell):
            return 0.0

        # stop case 2 : if is next cell non-visible
        elif not perception.is_visible(next_cell, agent_id):
            return 0.25

        # stop case 3 : if is next cell a pac gum
        elif perception.get_board().get_cell(next_cell).PAC_GUM:
            return 0.5

        # stop case 4 : if is next cell a pac dot
        elif perception.get_board().get_cell(next_cell).PAC_DOT:
            return 1.0

        # recursive case : continue in  all other direction
        else:
            score = 0
            already_visited.append(next_cell)
            for direction in Direction:
                score += self.get_exploration_score(perception, agent_id, next_cell, direction, already_visited)
            return forgetting_rate * score

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

    def get_legal_move(self, perception: Perception, agent_id: str) -> list[Direction]:
        return perception.get_board().get_legal_move(self.get_agent_position(agent_id))

    def get_agent_position(self, agent_id: str) -> (int, int):
        return self._agentManager.get_agent(agent_id).get_position()
