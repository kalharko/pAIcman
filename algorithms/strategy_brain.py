from back.agent import Agent
from back.agent_manager import AgentManager
from back.team import Team
from utils.strategy import Strategy


class StrategyBrain:
    """Class making the decision of the strategy of each agent of a team"""

    _agentManager: AgentManager
    _team: Team

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

    def __init__(self, agent_manager: AgentManager, team: Team):
        """StrategyBrain's initialization
        :param agent_manager: the agentManager of the game
        :type agent_manager: AgentManager
        :param team : the team object of the team to compute
        :type team: Team
        """

        self._agentManager = agent_manager
        self._team = team

        # define hyper parameters

        self._STRATEGY_AGRESSION_PAC_DOT_RANGE = 10
        self._STRATEGY_AGRESSION_ENEMY_RANGE = 15
        self._STRATEGY_AGRESSION_ENEMY_AMOUNT = 2
        self._STRATEGY_AGRESSION_ENEMY_PACMAN = True

        # we must have _STRATEGY_DEFENCE_ENEMY_RANGE <= _STRATEGY_AGRESSION_PAC_DOT_RANGE
        self._STRATEGY_DEFENCE_ENEMY_RANGE = 5
        # we must have _STRATEGY_DEFENCE_ENEMY_AMOUNT <= _STRATEGY_AGRESSION_ENEMY_RANGE
        self._STRATEGY_DEFENCE_ENEMY_AMOUNT = 1
        self._STRATEGY_DEFENCE_ENEMY_PACMAN = False

        self._STRATEGY_DEFENCE_PACMAN_DIST = 20
        self._STRATEGY_AGRESSION_PACMAN_DIST = 20

    def compute_team_strategy(self) -> dict[str, Strategy]:
        """For a certain team of the pac man game give the strategy (
        Exploration, Attack, Defence) for each agent

        :return: A dictionary containing as key the id of the agent and the value is the chosen strategy
        :rtype {str, Strategy}
        """

        strategy = {}

        # Compute for the pac man of the team
        pacman = self._team.get_pacman()

        # if (Pac dot close AND Enemy close) OR Invincible mode active -> then AGRESSION
        if (self.is_pac_dot_close(pacman, self._STRATEGY_AGRESSION_PAC_DOT_RANGE)
                and self.is_enemy_close(pacman, self._STRATEGY_AGRESSION_ENEMY_RANGE,
                                        self._STRATEGY_AGRESSION_ENEMY_AMOUNT, self._STRATEGY_AGRESSION_ENEMY_PACMAN)
                or pacman.is_invicible()):
            strategy[pacman.get_id()] = Strategy.AGRESSION

        # elif Enemy close -> then DEFENCE
        elif (self.is_enemy_close(pacman, self._STRATEGY_DEFENCE_ENEMY_RANGE, self._STRATEGY_DEFENCE_ENEMY_AMOUNT,
                                  self._STRATEGY_DEFENCE_ENEMY_PACMAN)):
            strategy[pacman.get_id()] = Strategy.DEFENSE

        # else EXPLORATION
        else:
            strategy[pacman.get_id()] = Strategy.EXPLORATION

        # Compute for the ghosts
        for ghosts in self._team.get_ghosts():

            # if allie pac man in defence strategy and close OR enemy pac man invincible -> then Defence
            if (strategy[pacman.get_id()] == Strategy.DEFENSE and self.allie_pacman_distance(
                    ghosts) <= self._STRATEGY_DEFENCE_PACMAN_DIST or self.is_enemy_invincible()):
                strategy[ghosts.get_id()] = Strategy.DEFENSE

            # elif enemy pac man close -> Agression
            elif self.ennemi_pacman_distance(ghosts) <= self._STRATEGY_AGRESSION_PACMAN_DIST:
                strategy[ghosts.get_id()] = Strategy.AGRESSION

            # else -> Exploration
            else:
                strategy[ghosts.get_id()] = Strategy.EXPLORATION

        return strategy

    def is_pac_dot_close(self, agent: Agent, dist: int) -> bool:
        # TODO: implement
        return True

    def is_enemy_close(self, agent: Agent, dist: int, amount: int, cont_pac_man: bool) -> bool:
        # TODO: implement
        return True

    def allie_pacman_distance(self, agent: Agent) -> int:
        # TODO : Oscar
        return 0

    def ennemi_pacman_distance(self, agent: Agent) -> int:
        # TODO : Oscar
        return 0

    def is_enemy_invincible(self) -> bool:
        # TODO : implement
        return True
