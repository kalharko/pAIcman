from algorithms.a_star import AStar

from algorithms.brain import Brain
from back.team import Team
from utils.action import Action
from utils.direction import Direction
from utils.distance_matrix import DistanceMatrix


class GhostBrain(Brain):
    def __init__(self, distance_matrix: DistanceMatrix) -> None:
        super().__init__(distance_matrix)

        # defense hyper parameters
        self._DEFENSE_DISTANCE_TO_PACMAN = 4
        # exploration hyper parameters
        self._EXPLORATION_FORGETTING_RATE = 0.1
        self._EXPLORATION_PAC_GUM_SCORE = 0
        self._EXPLORATION_PAC_DOT_SCORE = 0
        self._EXPLORATION_UNKNOWN_CELL_SCORE = 1
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
        for direction in Direction:
            if direction in (Direction['NONE'], Direction['RESPAWN']):
                continue
            dx, dy = direction.value
            distance = self._distances.get_distance((x + dx, y + dy), pacman_pos)
            if abs(distance - self._DEFENSE_DISTANCE_TO_PACMAN) < best_distance:
                best_direction = direction
                best_distance = distance

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
            return self._exploration(team, agent_id)

        a_star = AStar()
        a_star.load_board(team.get_perception().get_board())

        direction = a_star.first_step_of_path(team.get_agent(agent_id).get_position(), pacman_sighting[1].get_position())

        return Action(agent_id, direction)
