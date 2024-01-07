import random

from brain import Brain
from back.perception import Perception
from back.team import Team
from back.cell import Cell
from utils.action import Action
from utils.direction import Direction
from a_star import AStar


class PacmanBrain(Brain):

    def __init__(self, agent_manager):
        super().__init__(agent_manager)

        # define hyper parameters
        self._EXPLORATION_FORGETTING_RATE = 0.1
        self._EXPLORATION_PAC_GUM_SCORE = 1
        self._EXPLORATION_PAC_DOT_SCORE = -1
        self._EXPLORATION_UNKNOWN_CELL_SCORE = 1
        self._EXPLORATION_LAST_CELL_VISITED_SCORE = -5

    def _agression(perception: Perception, agent_id: str, team: Team) -> Action:
        """Give the best agressive action for the given agent

        :param perception: the team perception that the pacman agent will use to make its decision
        :type perception: Perception
        :param agent_id: id of the pacman agent
        :type agent_id: str
        :return: the optimal agressive action for the given agent
        :rtype: Action
        """
        a_star = AStar(team.get_perception().get_board())
        pacman_sightings = team.get_perception().get_sightings()

        ghost_seen = False
        pacgum_activated = False
        ghost_position = None

        for id, sighting in pacman_sightings.items():
            if "g" in id:
                ghost_seen = True
                ghost_position = (sighting[1], sighting[2])
            elif team.get_perception().get_board().get_cell(sighting[1], sighting[2]) == Cell.PAC_GUM and sighting[0] == 0:
                pacgum_activated = True

        if not ghost_seen:
            return Action(agent_id, random.choice(list(Direction)))

        if pacgum_activated:
            #if a pacgum is activated, pacman will try to prioritize attacking the ghost

            ghosts = team.get_perception().get_ghost_ids() #get all the ghost the team can see currently 
            if ghosts:
                nearest_ghost = min(ghosts, key=lambda ghost: a_star.distance(ghost, ghost_position)) #get the nearest ghost by checking the path length between the ghost and the pacman 
                direction = a_star.first_step_of_path(team.get_agent(agent_id), nearest_ghost) #follow the path to the ghost 
                return Action(agent_id, direction)
        else:
            direction = a_star.first_step_of_path(team.get_agent(agent_id), ghost_position)
            return Action(agent_id, direction)

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
