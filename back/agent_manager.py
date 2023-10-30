from back.agent import Agent
from back.ghost import Ghost
from back.pacman import Pacman
from back.team import Team
from utils.action import Action
from back.errors import PacErrUnknownAgentId


class AgentManager():
    _teams: list[Team]

    def __init__(self) -> None:
        self._teams = []

    def load(self, source: list[str], board_size: tuple[int, int]) -> None:
        assert isinstance(source, list)
        assert len(source) > 0
        assert isinstance(source[0], str)
        assert isinstance(board_size, tuple)
        assert len(board_size) == 2
        assert isinstance(board_size[0], int)
        assert isinstance(board_size[1], int)

        self._teams = [Team(board_size), Team(board_size)]
        for line in source:
            line = line.rstrip('\n').split(', ')
            if line[2] == 'Pacman':
                self._teams[int(line[0])].set_pacman(Pacman(int(line[0]), line[1], int(line[3]), int(line[4])))
            else:
                self._teams[int(line[0])].add_ghost(Ghost(int(line[0]), line[1], int(line[3]), int(line[4])))

    def apply(self, action: Action) -> bool:
        assert isinstance(action, Action)

        if action.id not in self._agents.keys():
            return PacErrUnknownAgentId(self)

        self._agents[action.id].move((action.direction))

    def get_agent(self, id: str) -> Agent:
        assert isinstance(id, str)

        for team in self._teams:
            if id in team.get_ids():
                return team.get_agent(id)
        return PacErrUnknownAgentId(self)

    def get_all_agents(self) -> tuple[Agent]:
        out = []
        for team in self._teams:
            out += list(team.get_agents())
        return tuple(out)

    def get_teams(self) -> tuple[Team]:
        return tuple(self._teams)

    def reset(self) -> None:
        for team in self._teams:
            team.reset()
