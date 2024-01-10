from back.agent import Agent
from back.cell import Cell
from back.perception import Perception
from back.team import Team
from utils.distance_matrix import DistanceMatrix
from utils.replay_logger import ReplayLogger
from utils.strategy import Strategy
from algorithms.flood_fill import closest_cell


class StrategyBrain:
    """Class making the decision of the strategy of each agent of a team"""

    _distances: DistanceMatrix

    # Hyper parameters
    _STRATEGY_AGRESSION_PAC_DOT_RANGE: int
    _STRATEGY_AGRESSION_ENEMY_RANGE: int
    _STRATEGY_AGRESSION_ENEMY_AMOUNT: int
    _STRATEGY_AGRESSION_ENEMY_PACMAN: bool

    _STRATEGY_DEFENCE_ENEMY_RANGE: int
    _STRATEGY_DEFENCE_ENEMY_AMOUNT: int
    _STRATEGY_DEFENCE_ENEMY_PACMAN: bool

    _STRATEGY_DEFENCE_PACMAN_DIST: int
    _STRATEGY_AGRESSION_PACMAN_DIST: int
    _STRATEGY_DEFENCE_PACMAN_COLLISION_DIST: int

    def __init__(self, distances: DistanceMatrix) -> None:
        """StrategyBrain's initialization
        :param distances : teh distance matrix between agents
        :type distances : DistanceMatrix
        """

        self._distances = distances

        # define hyper parameters

        self._STRATEGY_AGRESSION_PAC_DOT_RANGE = 5
        self._STRATEGY_AGRESSION_ENEMY_RANGE = 10
        self._STRATEGY_AGRESSION_ENEMY_AMOUNT = 1
        self._STRATEGY_AGRESSION_ENEMY_PACMAN = True

        # we must have _STRATEGY_DEFENCE_ENEMY_RANGE <= _STRATEGY_AGRESSION_PAC_DOT_RANGE
        self._STRATEGY_DEFENCE_ENEMY_RANGE = 5
        # we must have _STRATEGY_DEFENCE_ENEMY_AMOUNT <= _STRATEGY_AGRESSION_ENEMY_RANGE
        self._STRATEGY_DEFENCE_ENEMY_AMOUNT = 1
        self._STRATEGY_DEFENCE_ENEMY_PACMAN = False

        self._STRATEGY_DEFENCE_PACMAN_DIST = 10
        self._STRATEGY_AGRESSION_PACMAN_DIST = 20
        self._STRATEGY_DEFENCE_PACMAN_COLLISION_DIST = 3

    def compute_team_strategy(self, team: Team) -> dict[str, Strategy]:
        """For a certain team of the pac man game give the strategy (
        Exploration, Attack, Defence) for each agent

        :return: A dictionary containing as key the id of the agent and the value is the chosen strategy
        :rtype {str, Strategy}
        """

        strategy = {}
        perception = team.get_perception()
        board = perception.get_board()

        # Compute for the pac man of the team
        pacman = team.get_pacman()


        # if (Pac dot close AND Enemy close) OR Invincible mode active -> then AGRESSION
        if ((self.pac_gum_distance(pacman, team) < self._STRATEGY_AGRESSION_PAC_DOT_RANGE
             and self.is_enemy_close(pacman, perception))
                or pacman.is_invicible()):
            strategy[pacman.get_id()] = Strategy.AGRESSION

        # elif Enemy close -> then DEFENCE
        elif self.is_enemy_close(pacman, perception):
            strategy[pacman.get_id()] = Strategy.DEFENSE

        # else EXPLORATION
        else:
            strategy[pacman.get_id()] = Strategy.EXPLORATION

        # Compute for the ghosts
        for ghost in team.get_ghosts():
            # if allie pac man in defence strategy and close OR allie pac-man collisionable OR enemy pac man
            # invincible -> then Defence
            #ReplayLogger().log_comment("allie pac man dist : " + self.allie_pacman_distance(ghost, team).__str__())
            if (strategy[pacman.get_id()] == Strategy.DEFENSE
                    and self.allie_pacman_distance(ghost, team) <= self._STRATEGY_DEFENCE_PACMAN_DIST
                    or self.allie_pacman_distance(ghost, team) <= self._STRATEGY_DEFENCE_PACMAN_COLLISION_DIST
                    or self.is_enemy_invincible(team)):
                strategy[ghost.get_id()] = Strategy.DEFENSE

            # elif enemy pac man close -> Agression
            elif self.ennemi_pacman_distance(ghost, team) <= self._STRATEGY_AGRESSION_PACMAN_DIST:
                strategy[ghost.get_id()] = Strategy.AGRESSION

            # else -> Exploration
            else:
                strategy[ghost.get_id()] = Strategy.EXPLORATION

        return strategy

    def is_enemy_close(self, agent: Agent, perception: Perception) -> bool:
        """Returns True if the agent is close to multiple ennemies
        """

        nb_enemy_in_range = 0
        sightings = perception.get_ghost_sightings()
        if self._STRATEGY_DEFENCE_ENEMY_PACMAN:
            sightings += perception.get_pacman_sighting()

        for enemy in sightings:
            if enemy[1].is_alive():
                if self._distances.get_distance(perception, agent.get_position(),
                                                enemy[1].get_position()) <= self._STRATEGY_AGRESSION_ENEMY_RANGE:
                    nb_enemy_in_range += 1
                    if nb_enemy_in_range >= self._STRATEGY_DEFENCE_ENEMY_AMOUNT:
                        return True

        return False

    def allie_pacman_distance(self, agent: Agent, team: Team) -> int:
        """Returns the distance between the agent the team's pacman

        :param agent: the agent we want to know the team's pacman distance to
        :type agent: Agent
        :param team : the team object of the team we are working on
        :type team : Team
        :return: the distance between the agent and the team's pacman
        :rtype: int
        """

        return self._distances.get_distance(team.get_perception(), agent.get_position(),
                                            team.get_pacman().get_position())

    def pac_gum_distance(self, agent: Agent, team: Team) -> int:
        """Returns the distance between the agent and the closest pac-gum

        :param agent: the agent we want to know the pac-gum distance to
        :type agent: Agent
        :param team : the team object of the team we are working on
        :type team : Team
        :return: the distance between the agent and the closest pac-gum
        :rtype: int
        """
        min_distance = 1000
        pac_gum_sightings = team.get_perception().get_pac_gum_sightings()
        for pac_gum in pac_gum_sightings:
            (time, x, y) = pac_gum
            pac_gum_pos = (x, y)
            pac_gum_dist = self._distances.get_distance(team.get_perception(), agent.get_position(), (x,y))
            if pac_gum_dist < min_distance:
                min_distance = pac_gum_dist

        return min_distance

    def ennemi_pacman_distance(self, agent: Agent, team: Team) -> int:
        """Returns the distance between an agent and the annemy's pacman

        :param agent: the agent we want to know the ennemy's pacman distance to
        :type agent: Agent
        :return: the distance between the agent and the ennemy's pacman
        :rtype: int
        """
        perception = team.get_perception()
        sighting = perception.get_pacman_sighting()
        if sighting == []:
            return 100

        enemy_pacman = sighting[0][1]
        return self._distances.get_distance(perception, agent.get_position(), enemy_pacman.get_position())

    def is_enemy_invincible(self, team: Team) -> bool:
        return team.get_ghosts()[0].is_vulnerable()
