from algorithms.strategy_brain import StrategyBrain
from algorithms.utility import Utility
from back.pacman_game import PacmanGame
from algorithms.pacman_brain import PacmanBrain
from algorithms.ghost_brain import GhostBrain
from argparse import ArgumentParser
from utils.action import Action
from utils.replay_logger import ReplayLogger
import time


class Main():
    """Main class of our project, that can run 2 teams on a pacman game, using either utility or strategy triangle decision making
    """
    id_team_a: tuple[str]
    id_team_b: tuple[str]
    brain_pacman: PacmanBrain
    brain_ghost: GhostBrain
    environment: PacmanGame
    scenario: int
    _team1_decision_algo: str
    _team2_decision_algo: str
    _small_history: list[list[Action]]

    def __init__(self, map_path: str, team1_decision_algo: str, team2_decision_algo: str, verbose: bool = True) -> None:
        """Main initialization

        :param map_path: path to the pacman map to load into the game
        :type map_path: str
        :param team1_decision_algo: decision algorithm for team1
        :type team1_decision_algo: str
        :param team2_decision_algo: decision algorithm for team2
        :type team2_decision_algo: str
        """
        self._team1_decision_algo = team1_decision_algo
        self._team2_decision_algo = team2_decision_algo

        # set up environment
        self.environment = PacmanGame()
        self.environment.load_map(map_path)
        ReplayLogger().log_map(map_path)

        # brains
        self.brain_ghost = GhostBrain(self.environment.get_board_distances())
        self.brain_pacman = PacmanBrain(self.environment.get_board_distances())
        self.strategy_brain = StrategyBrain(self.environment.get_board_distances())

        # other
        self.utility = Utility(self.environment.get_board_distances())
        self.verbose = verbose
        self._small_history = []
        if self.verbose:
            ReplayLogger().log_map(map_path)

    def cycle(self) -> bool:
        """Simulation cycle that adapts to the decision system specified at the creation of the class
        :return: True if the game is not over, False if it is
        :rtype: bool
        """
        # gather team's informations
        team_a, team_b = self.environment.gather_state()

        # different decision systems
        actions = []

        ReplayLogger().log_comment('Team a')
        if self._team1_decision_algo == 'utility':
            actions += self.utility.run(team_a)
        elif self._team1_decision_algo == 'behaviors':
            strategies = self.strategy_brain.compute_team_strategy(team_a)
            for agent_id, strategy in strategies.items():
                if agent_id == team_a.get_pacman().get_id():
                    actions.append(self.brain_pacman.compute_action(strategy, team_a, agent_id))
                else:
                    actions.append(self.brain_ghost.compute_action(strategy, team_a, agent_id))

        ReplayLogger().log_comment('\nTeam b')

        if self._team2_decision_algo == 'utility':
            actions += self.utility.run(team_b)
        elif self._team2_decision_algo == 'behaviors':
            strategies = self.strategy_brain.compute_team_strategy(team_b)
            for agent_id, strategy in strategies.items():
                if agent_id == team_b.get_pacman().get_id():
                    actions.append(self.brain_pacman.compute_action(strategy, team_b, agent_id))
                else:
                    actions.append(self.brain_ghost.compute_action(strategy, team_b, agent_id))

        # apply to environment
        self.environment.step(actions)
        # save for replay
        ReplayLogger().log_step(actions)
        # save for is repeating function
        self._small_history.append(actions)
        if len(self._small_history) == 5:
            self._small_history = self._small_history[1:]
        # return wether the game is over or not
        return not self.environment.is_game_over()

    def play_until_game_over(self) -> None:
        """Play until the game is over
        """
        while self.cycle():
            pass

    def set_teams_utility_parameters(self, value_1: tuple[float], value_2: tuple[float]) -> None:
        """Set both teams utility parameters

        :param value_1: team 1 utility parameters
        :type value_1: list[float]
        :param value_2: team 2 utility parameters
        :type value_2: list[float]
        """
        assert self._team1_decision_algo == 'utility'
        assert self._team2_decision_algo == 'utility'

        t1, t2 = self.environment.get_teams()
        t1.set_utility_parameters(value_1)
        t2.set_utility_parameters(value_2)

    def reset(self) -> None:
        """Reset the game
        """
        self._small_history = []
        self.environment.reset()
        ReplayLogger().reset()

    def get_winning_team_number(self) -> int:
        """Get the winning team

        :return: winning team
        :rtype: Team
        """
        return self.environment.winning_team

    def is_repeating(self) -> bool:
        """Returns wether or not the game is repeating and fruitless

        :return: wether or not the game is repeating
        :rtype: bool
        """
        if len(self._small_history) < 4:
            return False

        if all([a1.id == a2.id and a1.direction == a2.direction for a1, a2 in zip(self._small_history[-4], self._small_history[-2])]):
            if all([a1.id == a2.id and a1.direction == a2.direction for a1, a2 in zip(self._small_history[-3], self._small_history[-1])]):
                # commet
                return True

        return False


if __name__ == '__main__':
    parser = ArgumentParser(prog='Paicman',
                            description='Run two opposing teams in a pacman game',
                            epilog='epilog')
    parser.add_argument('-m', '--map_path',
                        help='path to the map to use',
                        default='maps/original.txt')
    parser.add_argument('-t1', '--team1_decision_algo',
                        help='which decision system to use for the team 1, default to utility',
                        default='utility',
                        type=str)
    parser.add_argument('-t2', '--team2_decision_algo',
                        help='which decision system to use for the team 2 default to behaviors',
                        default='behaviors',
                        type=str)
    parser.add_argument('-c', '--color',
                        help='chose color theme, possible values : dark, light',
                        default='dark',
                        type=str)

    args = parser.parse_args()

    main = Main(args.map_path, args.team1_decision_algo, args.team2_decision_algo)
    print(f'Playing on map {args.map_path}, with team1 using {args.team1_decision_algo} and team2 using {args.team2_decision_algo}')
    i = 0
    while i < 100:
        start_time = time.time()
        print('\riteration :', i, end='')
        if not main.cycle():
            print('\nGame Over')
            break
        if main.is_repeating():
            print('\nIs repeating')
            break
        i += 1
        if time.time() - start_time > 5:
            print('\nToo long, stopping')
            break

ReplayLogger().save_replay('last_replay.pkl')
