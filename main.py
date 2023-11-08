from back.pacman_game import PacmanGame
from back.pacman import Pacman
from algorithms.pacman_brain import PacmanBrain
from algorithms.ghost_brain import GhostBrain
from utils.strategy import Strategy
from front.cli.cli_replay import CliReplay


class Main():
    id_team_a: tuple[str]
    id_team_b: tuple[str]
    brain_pacman: PacmanBrain
    brain_ghost: GhostBrain
    environment: PacmanGame

    def __init__(self) -> None:
        # set up environment
        self.environment = PacmanGame()
        self.environment.load_map('maps/original.txt')

        # other
        self.brain_ghost = GhostBrain()
        self.brain_pacman = PacmanBrain()

    def simulation_cycle(self) -> None:
        # gather state
        team_a, team_b = self.environment.gather_state()
        print(team_a.get_perception())

        # compute strategy
        # TODO
        strat_team_a = ((agent, Strategy['RANDOM']) for agent in team_a.get_agents())
        strat_team_b = ((agent, Strategy['RANDOM']) for agent in team_b.get_agents())

        # compute agent actions
        actions = []
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
    main = Main()
    for i in range(10):
        main.simulation_cycle()
        input()
    replay = CliReplay(main.environment)
