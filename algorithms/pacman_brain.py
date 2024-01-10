import random

from algorithms.brain import Brain
from back.team import Team
from back.cell import Cell
from utils.action import Action
from utils.direction import Direction
from algorithms.a_star import AStar
from utils.distance_matrix import DistanceMatrix
from utils.replay_logger import ReplayLogger


class PacmanBrain(Brain):

    def __init__(self, distance_matrix: DistanceMatrix) -> None:
        super().__init__(distance_matrix)

        # defense hyper parameters
        self._DEFENSER_MIN_DISTANCE_TO_GHOST = 5

        # define hyper parameters
        self._EXPLORATION_FORGETTING_RATE = 0.1
        self._EXPLORATION_PAC_GUM_SCORE = -10
        self._EXPLORATION_PAC_DOT_SCORE = 2
        self._EXPLORATION_UNKNOWN_CELL_SCORE = 1
        self._EXPLORATION_LAST_CELL_VISITED_SCORE = -3

    def _agression(self, team: Team, agent_id: str) -> Action:
        """Give the best agressive action for the given agent

        :param perception: the team perception that the pacman agent will use to make its decision
        :type perception: Perception
        :param agent_id: id of the pacman agent
        :type agent_id: str
        :return: the optimal agressive action for the given agent
        :rtype: Action
        """

        a_star = AStar()
        a_star.load_board(team.get_perception().get_board())
        pacman = team.get_pacman()
        perception = team.get_perception()

        if pacman.is_invicible():
            # find the closest enemy ghost sighting
            ghosts = team.get_perception().get_ghost_sightings()
            if ghosts == []:
                return self._exploration(team, agent_id)
            for ghost in ghosts:
                if not ghost[1].is_alive():
                    ghosts.remove(ghost)
            nearest_ghost = min(ghosts, key=lambda ghost: self._distances.get_distance(perception, ghost[1].get_position(), pacman.get_position()))

            direction = a_star.first_step_of_path(pacman.get_position(), nearest_ghost[1].get_position())
            ReplayLogger().log_comment("Pac-Man invincible\nTry Kill " + nearest_ghost[1].get_id() + " at " + nearest_ghost[1].get_position())
            return Action(agent_id, direction)
        else:
            # find the closest pacgum
            return self._defense(team, agent_id)

    def _defense(self, team: Team, agent_id: str) -> Action:
        """Give the best defensive action for the given agent

        :param perception: the team perception that the pacman agent will use to make its decision
        :type perception: Perception
        :param agent_id: id of the pacman agent
        :type agent_id: str
        :return: the optimal defensive action for the given agent
        :rtype: Action
        """

        perception = team.get_perception()
        pacman = team.get_pacman()
        pacgums = perception.get_pac_gum_sightings()

        # find the closest enemy ghost sighting
        ghosts = team.get_perception().get_ghost_sightings()  # get all the ghost the team can see currently
        if ghosts == []:
            return self._exploration(team, agent_id)
        for ghost in ghosts:
            if not ghost[1].is_alive():
                ghosts.remove(ghost)
        nearest_ghost = min(ghosts, key=lambda ghost: self._distances.get_distance(perception, ghost[1].get_position(), pacman.get_position()))
        dist_to_ghost = self._distances.get_distance(perception, nearest_ghost[1].get_position(), pacman.get_position())

        # go to the nearest pac gum if it does not get the pacman closer to the nearest ghost
        a_star = AStar()
        a_star.load_board(perception.get_board())

        # If there is a pac gum visible find the pac gum
        if (len(pacgums.keys()) != 0):
            # find the closest pacgum
            closest_pacgum_pos = min(pacgums.keys(), key=lambda pacgum: self._distances.get_distance(perception, pacgum, pacman.get_position()))
            # direction to closest pacgum
            direction = a_star.first_step_of_path(pacman.get_position(), closest_pacgum_pos).value
            x, y = pacman.get_position()
            new_dist_to_ghost = self._distances.get_distance(perception, (x + direction[0], y + direction[1]), nearest_ghost[1].get_position())
            # direction is not accepted if distance to ghost is too close and direction gets closer to ghost
            if new_dist_to_ghost < dist_to_ghost and new_dist_to_ghost <= self._DEFENSER_MIN_DISTANCE_TO_GHOST:
                ReplayLogger().log_comment("Try reach pac gum at" + closest_pacgum_pos +
                                         "\nBut " + nearest_ghost[1].get_id() +
                                         " at " +nearest_ghost[1].get_position() + " block the way")
                legal_moves = self.get_legal_move(perception, pacman.get_position())
                legal_moves.remove(direction)
                if direction.opposite() in legal_moves:
                    return Action(agent_id, direction.opposite())
                else:
                    return Action(agent_id, random.choice(legal_moves))

                ReplayLogger().log_comment("Try reach pac gum at" + closest_pacgum_pos +
                                         "\nAnd then kill " + nearest_ghost[1].get_id() +
                                         " at " + nearest_ghost[1].get_position())
            return Action(agent_id, direction)

        # else go in the opposite direction of the nearest ghosts
        else:
            ghosts_direction = a_star.first_step_of_path(pacman.get_position(), nearest_ghost[1].get_position())
            legal_moves = self.get_legal_move(perception, pacman.get_position())
            legal_moves.remove(ghosts_direction)
            ReplayLogger().log_comment("No Pac-Gum Reachable or known\nRun away from " + nearest_ghost[1].get_id().__str__() +
                                     " at " + nearest_ghost[1].get_position().__str__())
            if ghosts_direction.opposite() in legal_moves:
                return Action(agent_id, ghosts_direction.opposite())
            else:
                return Action(agent_id, random.choice(legal_moves))


