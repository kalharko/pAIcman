import random
from algorithms.brain import Brain
from back.perception import Perception
from back.team import Team
from utils.direction import Direction
from utils.strategy import Strategy
from utils.action import Action
from algorithms.a_star import AStar


class GhostBrain(Brain):
    def __init__(self):
        self.behavior = {
            'predictive': self._predictive_aggression,
            'close_proximity': self._close_proximity_aggression,
        }

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
            return self._aggression(perception, id)
            # return Action(id, random.choice(list(Direction)))

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

    def _agression(team: Team, agent_id: str) -> Action:
        """Give the best agressive action for the given agent

        :param team: the team perception that the ghost agent will use to make it's decision
        :type team: Team
        :param agent_id: id of the ghost agent
        :type agent_id: str
        :return: the optimal agressive action for the given agent
        :rtype: Action
        """

        a_star = AStar(team.get_perception().get_board())
        sightings = team.get_perception().get_sightings()

        pacman_seen = False

        for id in sightings.keys() :
            if "P" in id : 
                pacman_sighting = sightings[id]
                pacman_seen = True

        pacman_position = (pacman_sighting[1], pacman_sighting[2])

        if not pacman_seen : 
            return Action(agent_id, random.choice(list(Direction)))

        direction = a_star.first_step_of_path(team.get_agent(agent_id),pacman_position )

        return Action(agent_id, direction)
        

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
    
