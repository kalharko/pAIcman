import random
import copy
from back.agent_manager import AgentManager
from back.perception import Perception
from utils.action import Action
from utils.direction import Direction
from utils.strategy import Strategy
# from utils.replay_logger import ReplayLogger
from back.cell import Cell
from back.team import Team



class Brain:
    _agentManager: AgentManager
    _already_visited: list[tuple[int, int]]
    _last_cell_visited: tuple[int, int]

    # hyper parameters
    _EXPLORATION_FORGETTING_RATE: float
    _EXPLORATION_PAC_GUM_SCORE: float
    _EXPLORATION_PAC_DOT_SCORE: float
    _EXPLORATION_UNKNOWN_CELL_SCORE: float
    _EXPLORATION_LAST_CELL_VISITED_SCORE: float

    def __init__(self, agent_manager):
        self._agentManager = agent_manager
        self._already_visited = None
        self._last_visited = None

    def compute_action(self, strategy: Strategy, team: Team, agent_id: str) -> Action:
        """Decision-making of a pacman agent for a given strategy

        :param strategy: strategy that the pacman agent will apply
        :type strategy: Strategy
        :param team: the team that the pacman agent will use to make its decision
        :type team: Team
        :param agent_id: id of the pacman agent
        :type agent_id: str
        :return: the optimal action for the pacman agent for the given strategy
        :rtype: Action
        """
        assert isinstance(strategy, Strategy)
        assert isinstance(team, Team)
        assert isinstance(agent_id, str)

        if strategy == Strategy['RANDOM']:
            return Action(agent_id, random.choice(list(Direction)))

        if strategy == Strategy['EXPLORATION']:
            return self._exploration(team, agent_id)

        if strategy == Strategy['AGRESSION']:
            return self._agression(team, agent_id)

        if strategy == Strategy['DEFENSE']:
            return self._defense(team, agent_id)

    def _exploration(self, team: Team, agent_id: str) -> Action:
        """Give the best exploration action for the given agent

        :param team: the team that the pacman agent will use to make its decision
        :type team: Team
        :param agent_id: id of the pacman agent
        :type agent_id: str
        :return: the optimal exploration action for the given agent
        :rtype: Action
        """

        bestScore = None
        chosenDirection = None
        # ReplayLogger().log_comment('\n' + agent_id)
        perception = team.get_perception()
        opposite_dir = team.get_pacman().get_last_direction()
        opposite_dir = Direction((opposite_dir.value[0] * -1, opposite_dir.value[1] * -1))
        self._last_cell_visited = perception.get_board().get_next_cell(team.get_pacman().get_position(), opposite_dir)
        for direction in self.get_legal_move(perception, agent_id):  # TODO : shuffle the order of move
            self._already_visited = [team.get_pacman().get_position()]
            exploration_score = self.get_exploration_score(perception, agent_id, self.get_agent_position(agent_id), direction)
            # ReplayLogger().log_comment(str(direction) + ' ' + str(exploration_score))
            if bestScore is None or exploration_score >= bestScore:
                chosenDirection = direction
                bestScore = exploration_score

        # print(chosenDirection)
        return Action(agent_id, chosenDirection)

    def get_exploration_score(self, perception: Perception, agent_id: str, position: (int, int),
                              direction: Direction) -> float:
        next_cell = perception.get_board().get_next_cell(position, direction)

        # stop case 1 : if is next cell non-legal
        if not perception.get_board().get_cell(position).is_movable():
            return 0.0

        # stop case 2 : if the cell is already visited
        elif next_cell in self._already_visited:
            return 0.0

        # stop case 3 : if is next cell unknown
        elif perception.get_board().get_cell(next_cell) == Cell['UNKNOWN']:
            return self._EXPLORATION_UNKNOWN_CELL_SCORE

        # stop case 4 : if the next cell is non-visible
        elif next_cell not in perception.get_last_cells_seen():
            return 0.0

        # recursive case : continue in  all other direction
        else:
            score = 0
            if perception.get_board().get_cell(next_cell) == Cell['PAC_GUM']:
                score = self._EXPLORATION_PAC_GUM_SCORE
            elif perception.get_board().get_cell(next_cell) == Cell['PAC_DOT']:
                score = self._EXPLORATION_PAC_DOT_SCORE

            if next_cell == self._last_cell_visited:
                score = self._EXPLORATION_LAST_CELL_VISITED_SCORE
            self._already_visited.append(copy.copy(next_cell))
            for direction in Direction:
                score += self.get_exploration_score(perception, agent_id, next_cell, direction)
            return score * self._EXPLORATION_FORGETTING_RATE

    def get_legal_move(self, perception: Perception, agent_id: str) -> list[Direction]:
        """get the legal move that the agent can do
        :param perception : the perception of the agent
        :type perception : Perception

        :param agent_id: the id of the agent we are working
        :type : str

        :return : the list of the legal direction
        :rtype: list[Direction]
        """
        return perception.get_board().get_legal_move(self.get_agent_position(agent_id))

    def get_agent_position(self, agent_id: str) -> (int, int):
        """get the position of the agent

        :param agent_id: the id of the agent we want the position
        :type agent_id : str

        :return: the position of the agent
        :rtype : (int, int)
        """

        return self._agentManager.get_agent(agent_id).get_position()
