import random
import math
from algorithms.brain import Brain
from utils.action import Action
from utils.direction import Direction
from back.team import Team
from utils.replay_logger import ReplayLogger


class PacmanBrain(Brain):

    def __init__(self, agent_manager):
        super().__init__(agent_manager)

        # define hyper parameters
        # exploration
        self._EXPLORATION_FORGETHING_RATE = 0.5
        self._EXPLORATION_PAC_GUM_SCORE = 1
        self._EXPLORATION_PAC_DOT_SCORE = -1
        self._EXPLORATION_UNKNOWN_CELL_SCORE = 1
        self._EXPLORATION_LAST_CELL_VISITED_SCORE = -2
        # defense
        self._DEFENSE_FLEE_CUT_OFF = 2

    def _agression(self, team: Team, agent_id: str) -> Action:
        """Give the best agressive action for the given agent

        :param perception: the team perception that the pacman agent will use to make its decision
        :type perception: Perception
        :param agent_id: id of the pacman agent
        :type agent_id: str
        :return: the optimal agressive action for the given agent
        :rtype: Action
        """
        return Action(agent_id, random.choice(list(Direction)))

    def _defense(self, team: Team, agent_id: str) -> Action:
        """Give the best defensive action for the given agent

        :param perception: the team perception that the pacman agent will use to make its decision
        :type perception: Perception
        :param agent_id: id of the pacman agent
        :type agent_id: str
        :return: the optimal defensive action for the given agent
        :rtype: Action
        """
        # data
        perception = team.get_perception()
        pacman_position = team.get_pacman().get_position()
        #
        other_ghosts_sightings = perception.get_ghost_sightings()
        if len(other_ghosts_sightings) == 0:
            ReplayLogger().log_comment(agent_id + ' No ghost sightings, do Exploration instead')
            return self._exploration(team, agent_id)
        flee_direction = [0, 0]
        cut_off = len(other_ghosts_sightings)
        for sighting in other_ghosts_sightings:
            time = sighting[0]
            x = sighting[1][0]
            y = sighting[1][1]
            vect = [pacman_position[0] - x, pacman_position - y]
            # check if the sighting is relevant (too far or too long ago)
            if math.sqrt(vect[0] ** 2 + vect[1] ** 2) * time > self._DEFENSE_FLEE_CUT_OFF:
                cut_off -= 1
            flee_direction = [(flee_direction[0] + vect[0]) / time,
                              (flee_direction[1] + vect[1]) / time]

        norm = math.sqrt(flee_direction[0] ** 2 + flee_direction[1] ** 2)
        # soh cah toa
        angle = math.degrees(math.atan(flee_direction[1] / flee_direction[0]))
        closest = math.inf
        direction = 0
        for a in [0, 90, 180, 270]:
            if abs(a - angle) < closest:
                direction = a
                closest = abs(a - angle)
        direction = [0, 90, 180, 270].index(direction)


        # if all sightings are too far
        if cut_off == 0:
            ReplayLogger().log_comment(agent_id + ' Defense Cut off, do Exploration instead')
            return self._exploration(team, agent_id)





        return Action(agent_id, random.choice(list(Direction)))
