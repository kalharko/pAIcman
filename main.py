from algorithms.utility import Utility
from back.pacman_game import PacmanGame
from back.pacman import Pacman
from algorithms.pacman_brain import PacmanBrain
from algorithms.ghost_brain import GhostBrain
from utils.strategy import Strategy
from front.cli.cli_replay import CliReplay
from argparse import ArgumentParser


class Main():
    """Main class of our project, that can run 2 teams on a pacman game, using either utility or strategy triangle decision making
    """
    id_team_a: tuple[str]
    id_team_b: tuple[str]
    brain_pacman: PacmanBrain
    brain_ghost: GhostBrain
    environment: PacmanGame
    scenario: int

    def __init__(self, map_path: str, team1_decision_algo: str, team2_decision_algo: str) -> None:
        """Main initialization

        :param map_path: path to the pacman map to load into the game
        :type map_path: str
        :param team1_decision_algo: decision algorithm for team1
        :type team1_decision_algo: str
        :param team2_decision_algo: decision algorithm for team2
        :type team2_decision_algo: str
        """
        self.scenario = 0 if team1_decision_algo != team2_decision_algo else 2
        if self.scenario != 0:
            self.scenario = 1 if team1_decision_algo == 'utility' else 2

        # set up environment
        self.environment = PacmanGame()
        self.environment.load_map(map_path)

        # brains
        self.brain_ghost = GhostBrain()
        self.brain_pacman = PacmanBrain(self.environment.get_agent_manager())

        # other
        self.utility = Utility()

    def cycle(self):
        """Simulation cycle that adapts to the decision system specified at the creation of the class
        """
        # gather team's informations
        team_a, team_b = self.environment.gather_state()

        # different decision systems
        actions = []
        if self.scenario == 0:  # utility vs strategy triangle
            # utility
            actions = self.utility.run(team_a)
            # strategy triangle
            strat_team_b = ((agent, Strategy['RANDOM']) for agent in team_b.get_agents())
            for agent, strat in strat_team_b:
                if isinstance(agent, Pacman):
                    actions.append(self.brain_pacman.compute_action(strat, team_b.get_perception(), agent.get_id()))
                else:
                    actions.append(self.brain_ghost.compute_action(strat, team_b.get_perception(), agent.get_id()))
        elif self.scenario == 1:  # utility vs utility
            actions = self.utility.run(team_a)
            actions += self.utility.run(team_b)
        else:  # strategy triangle vs strategy triangle
            strat_team_a = ((agent, Strategy['EXPLORATION']) for agent in team_a.get_agents())
            strat_team_b = ((agent, Strategy['EXPLORATION']) for agent in team_b.get_agents())
            for agent, strat in strat_team_a:
                if isinstance(agent, Pacman):
                    actions.append(self.brain_pacman.compute_action(strat, team_a.get_perception(), agent.get_id()))
                else:
                    actions.append(self.brain_ghost.compute_action(strat, team_a.get_perception(), agent.get_id()))
            for agent, strat in strat_team_b:
                if isinstance(agent, Pacman):
                    actions.append(self.brain_pacman.compute_action(strat, team_b.get_perception(), agent.get_id()))
                else:
                    actions.append(self.brain_ghost.compute_action(strat, team_b.get_perception(), agent.get_id()))

        # apply to environment
        self.environment.step(actions)


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
                        help='which decision system to use for the team 2 default to strategy_triangle',
                        default='strategy_triangle',
                        type=str)

    args = parser.parse_args()

    main = Main(args.map_path, args.team1_decision_algo, args.team2_decision_algo)
    print(f'Playing on map {args.map_path}, with team1 using {args.team1_decision_algo} and team2 using {args.team2_decision_algo}')
    for i in range(100):
        main.cycle()
        if input(f'Cycle : {i},\t\tq to stop') == 'q':
            break
    replay = CliReplay(main.environment)
