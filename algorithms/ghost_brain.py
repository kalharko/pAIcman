from algorithms.a_star import AStar

from algorithms.brain import Brain
from back.team import Team
from utils.action import Action
from utils.direction import Direction
from utils.distance_matrix import DistanceMatrix
from utils.replay_logger import ReplayLogger


class GhostBrain(Brain):
    def __init__(self, distance_matrix: DistanceMatrix) -> None:
        super().__init__(distance_matrix)

        # defense hyper parameters
        self._DEFENSE_DISTANCE_TO_PACMAN = 5
        # exploration hyper parameters
        self._EXPLORATION_FORGETTING_RATE = 0.1
        self._EXPLORATION_PAC_GUM_SCORE = 0
        self._EXPLORATION_PAC_DOT_SCORE = 0
        self._EXPLORATION_UNKNOWN_CELL_SCORE = 2
        self._EXPLORATION_LAST_CELL_VISITED_SCORE = -5

    def _defense(self, team: Team, agent_id: str) -> Action:
        """Give the best defensive action for the given agent

        :param perception: the team perception that the ghost agent will use to make its decision
        :type perception: Perception
        :param agent_id: id of the ghost agent
        :type agent_id: str
        :return: the optimal defensive action for the given agent
        :rtype: Action
        """
        best_direction = None
        best_distance = 1000
        x, y = team.get_agent(agent_id).get_position()
        pacman_pos = team.get_pacman().get_position()
        ReplayLogger().log_comment("Objective disance to allie Pac-Man : " + self._DEFENSE_DISTANCE_TO_PACMAN.__str__())
        for direction in self.get_legal_move(team.get_perception(), (x, y)):
            dx, dy = direction.value
            distance = self._distances.get_distance(team.get_perception(),  (x + dx, y + dy), pacman_pos)
            difference = abs(distance - self._DEFENSE_DISTANCE_TO_PACMAN)
            ReplayLogger().log_comment(direction.name.__str__() + " -> " + distance.__str__())
            if difference < best_distance:
                best_direction = direction
                best_distance = difference

        return Action(agent_id, best_direction)

    def _agression(self, team: Team, agent_id: str) -> Action:
        """Give the best agressive action for the given agent

        :param perception: the team perception that the ghost agent will use to make its decision
        :type perception: Perception
        :param agent_id: id of the ghost agent
        :type agent_id: str
        :return: the optimal agressive action for the given agent
        :rtype: Action
        """

        pacman_sighting = team.get_perception().get_pacman_sighting()[0]
        if pacman_sighting is None:
            ReplayLogger().log_comment("Enemy Pac-Man non visible -> EXPLORATION")
            return self._exploration(team, agent_id)

        a_star = AStar()
        a_star.load_board(team.get_perception().get_board())

        direction = a_star.first_step_of_path(team.get_agent(agent_id).get_position(), pacman_sighting[1].get_position())
        ReplayLogger().log_comment("Try Kill " + pacman_sighting[1].get_id().__str__() +
                                   " at " + pacman_sighting[1].get_position().__str__())
        return Action(agent_id, direction)
