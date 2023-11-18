from algorithms.utility import Utility
from back.pacman_game import PacmanGame
from back.pacman import Pacman
from algorithms.pacman_brain import PacmanBrain
from algorithms.ghost_brain import GhostBrain
from utils.strategy import Strategy
from front.cli.cli_replay import CliReplay
from argparse import ArgumentParser


class Main():
    id_team_a: tuple[str]
    id_team_b: tuple[str]
    brain_pacman: PacmanBrain
    brain_ghost: GhostBrain
    environment: PacmanGame
    decision_system: int

    def __init__(self, map_path: str, decision_system: int) -> None:
        self.decision_system = decision_system

        # set up environment
        self.environment = PacmanGame()
        self.environment.load_map(map_path)

        # brains
        self.brain_ghost = GhostBrain()
        self.brain_pacman = PacmanBrain()

        # other
        self.utility = Utility()

    def cycle(self):
        # gather team's informations
        team_a, team_b = self.environment.gather_state()

        actions = []
        if self.decision_system == 0:  # utility vs strategy triangle
            # utility
            actions = self.utility.run(team_a)
            # strategy triangle
            strat_team_b = ((agent, Strategy['RANDOM']) for agent in team_b.get_agents())
            for agent, strat in strat_team_b:
                if isinstance(agent, Pacman):
                    actions.append(self.brain_pacman.compute_action(strat, team_b.get_perception(), agent.get_id()))
                else:
                    actions.append(self.brain_ghost.compute_action(strat, team_b.get_perception(), agent.get_id()))
        elif self.decision_system == 1:  # utility vs utility
            actions = self.utility.run(team_a)
            actions += self.utility.run(team_b)
        else:  # strategy triangle vs strategy triangle
            strat_team_a = ((agent, Strategy['RANDOM']) for agent in team_a.get_agents())
            strat_team_b = ((agent, Strategy['RANDOM']) for agent in team_b.get_agents())
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
    parser.add_argument('-d', '--decision_system',
                        help='which decision system to use, default is utility vs triangle, 1 is utility vs utility and 2 is triangle vs triangle.',
                        default=0,
                        type=int)
    args = parser.parse_args()

    main = Main(args.map_path, args.decision_system)
    print(f'Decision system {args.decision_system}, on map {args.map_path}')
    for i in range(100):
        main.cycle()
        if input() == 'q':
            break
    replay = CliReplay(main.environment)
