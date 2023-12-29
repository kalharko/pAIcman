from back.agent import Agent
from back.board_manager import BoardManager
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
        """Load agents from extracted file information

        :param source: list of lines read in the map file
        :type source: list[str]
        :param board_size: board size (width, height)
        :type board_size: tuple[int, int]
        """
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
        """Apply an action to agent

        :param action: action to apply
        :type action: Action
        """
        assert isinstance(action, Action)

        for team in self._teams:
            if id in team.get_ids():
                team.get_agent(id).move(action.direction)
                return
        return PacErrUnknownAgentId(self)

    def update_perceptions(self, board_manager: BoardManager) -> None:
        """Update teams perceptions

        :param board_manager: pacman_game's board_manager
        :type board_manager: BoardManager
        """
        assert isinstance(board_manager, BoardManager)

        # for the moment, only work with 2 teams
        assert len(self._teams) == 2
        self._teams[0].update_perception(board_manager, self._teams[1])
        self._teams[1].update_perception(board_manager, self._teams[0])

    def get_agent(self, id: str) -> Agent:
        """Get agent

        :param id: id of the agent to return
        :type id: str
        :return: agent with the corresponding id
        :rtype: Agent
        """
        assert isinstance(id, str)

        for team in self._teams:
            if id in team.get_ids():
                return team.get_agent(id)
        return PacErrUnknownAgentId(self)

    def get_all_agents(self) -> tuple[Agent]:
        """Get all agents from both teams

        :return: tuple with all agents from both teams
        :rtype: tuple[Agent]
        """
        out = []
        for team in self._teams:
            out += list(team.get_agents())
        return tuple(out)

    def get_teams(self) -> tuple[Team]:
        """Get both teams

        :return: tuple with both teams
        :rtype: tuple[Team]
        """
        return tuple(self._teams)

    def get_ids(self) -> tuple[str]:
        """Get agent id's for both teams

        :return: tuple with agent id's for both teams
        :rtype: tuple[str]
        """
        out = []
        for team in self._teams:
            out += list(team.get_ids())
        return tuple(out)

    def reset(self) -> None:
        """Reset both teams
        """
        for team in self._teams:
            team.reset()

    def is_game_over(self) -> bool:
        """Check if the game is over

        :return: True if the game is over, False if not
        :rtype: bool
        """
        for team in self._teams:
            if team.get_pacman().is_alive() is not True:
                return True
        return False
