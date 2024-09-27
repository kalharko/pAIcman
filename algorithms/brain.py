import random
import copy
from back.agent_manager import AgentManager
from back.perception import Perception
from utils.action import Action
from utils.direction import Direction
from utils.distance_matrix import DistanceMatrix
from utils.replay_logger import ReplayLogger
from utils.strategy import Strategy
# from utils.replay_logger import ReplayLogger
from back.cell import Cell
from back.team import Team


class Brain:
    _agentManager: AgentManager
    _already_visited: list[tuple[int, int]]
    _last_cell_visited: tuple[int, int]
    _distances: DistanceMatrix

    # hyper parameters
    _EXPLORATION_FORGETTING_RATE: float
    _EXPLORATION_PAC_GUM_SCORE: float
    _EXPLORATION_PAC_DOT_SCORE: float
    _EXPLORATION_UNKNOWN_CELL_SCORE: float
    _EXPLORATION_LAST_CELL_VISITED_SCORE: float

    def __init__(self, distances: DistanceMatrix) -> None:
        self._already_visited = None
        self._last_visited = None
        self._distances = distances

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

        ReplayLogger().log_comment('\n' + agent_id + team.get_agent(agent_id).get_position().__str__() + ": " + strategy.name.__str__())

        if strategy == Strategy['RANDOM']:
            direction = Action(agent_id, random.choice(list(Direction)))
            ReplayLogger().log_comment("Choosen Action : " + direction.name.__str__())
            return direction

        if strategy == Strategy['EXPLORATION']:
            direction = self._exploration(team, agent_id)
            ReplayLogger().log_comment("Choosen Action : " + direction.direction.name.__str__())
            return direction

        if strategy == Strategy['AGRESSION']:
            direction = self._agression(team, agent_id)
            ReplayLogger().log_comment("Choosen Action : " + direction.direction.name.__str__())
            return direction

        if strategy == Strategy['DEFENSE']:
            direction = self._defense(team, agent_id)
            ReplayLogger().log_comment("Choosen Action : " + direction.direction.name.__str__())
            return direction

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
        perception = team.get_perception()
        opposite_dir = team.get_pacman().get_last_direction()
        opposite_dir = Direction((opposite_dir.value[0] * -1, opposite_dir.value[1] * -1))
        self._last_cell_visited = perception.get_board().get_next_cell(team.get_pacman().get_position(), opposite_dir)
        for direction in self.get_legal_move(perception, team.get_agent(agent_id).get_position()):  # TODO : shuffle the order of move
            self._already_visited = [team.get_pacman().get_position()]
            exploration_score = self.get_exploration_score(team, agent_id, team.get_agent(agent_id).get_position(), direction)
            ReplayLogger().log_comment(str(direction.name) + ' -> ' + str(round(exploration_score, 2)))
            if bestScore is None or exploration_score >= bestScore:
                chosenDirection = direction
                bestScore = exploration_score

        return Action(agent_id, chosenDirection)

    def get_exploration_score(self, team: Team, agent_id: str, position: tuple[int, int],
                              direction: Direction) -> float:
        perception = team.get_perception()
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

        # stop case 5 : if there is a agent on the next cell
        elif self.is_agent_on_cell(team, next_cell):
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
            for direction in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                score += self.get_exploration_score(team, agent_id, next_cell, Direction(direction))* (1-self._EXPLORATION_FORGETTING_RATE)
            return score

    def get_legal_move(self, perception: Perception, position: tuple[int, int]) -> list[Direction]:
        """get the legal move that the agent can do
        :param perception : the perception of the agent
        :type perception : Perception

        :param agent_id: the id of the agent we are working
        :type : str

        :return : the list of the legal direction
        :rtype: list[Direction]
        """
        return perception.get_board().get_legal_move(position)

    def is_agent_on_cell(self, team: Team, position: tuple[int, int]) -> bool:

        #check if there is an ally
        for allie in team.get_agents():
            if position == allie.get_position():
                return True

        #check if there is an ennemy
        for age, enemy  in team.get_perception().get_sightings():
            if age < 3:
                if position == enemy.get_position():
                    return True

        return False