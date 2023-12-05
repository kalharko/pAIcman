from back.agent import Agent
from back.board_manager import BoardManager
from back.errors import PacErrUnknownAgentId
from back.pacman import Pacman
from back.ghost import Ghost
from back.perception import Perception


class Team():
    """Class managing the agents in a team
    """
    _pacman: Pacman
    _ghosts: list[Ghost]
    _perception: Perception
    _score: int

    def __init__(self, board_size: tuple[int, int]) -> None:
        """Team's initialization

        :param board_size: the game board's size
        :type board_size: tuple[int, int]
        """
        assert isinstance(board_size, tuple)
        assert len(board_size) == 2
        assert isinstance(board_size[0], int)

        self._pacman = None
        self._ghosts = []
        self._perception = Perception(board_size)
        self._score = 0

    def set_pacman(self, value: Pacman) -> None:
        """Set the team's pacman

        :param value: the pacman to add to the team
        :type value: Pacman
        """
        assert isinstance(value, Pacman)

        self._pacman = value

    def add_ghost(self, value: Ghost) -> None:
        """Add a ghost to the team's agents

        :param value: ghost to add to the team
        :type value: Ghost
        """
        assert isinstance(value, Ghost)

        self._ghosts.append(value)

    def get_agents(self) -> tuple[Agent]:
        """Get all the team's agents

        :return: list of all the team's agents
        :rtype: tuple[Agent]
        """
        return tuple([self._pacman] + self._ghosts)

    def get_agent(self, id: str) -> Agent:
        """Get agent with the given id

        :param id: id of the agent to return
        :type id: str
        :return: the agent with the given id
        :rtype: Agent
        """
        assert isinstance(id, str)

        for agent in self.get_agents():
            if id == agent.get_id():
                return agent
        return PacErrUnknownAgentId(self)

    def get_pacman(self) -> Pacman:
        """Get the team's pacman

        :return: the team's pacman
        :rtype: Pacman
        """
        return self._pacman

    def get_ghosts(self) -> tuple[Ghost]:
        """Get the team's ghosts

        :return: list of all the team's ghosts
        :rtype: tuple[Ghost]
        """
        return tuple(self._ghosts)

    def get_ids(self) -> tuple[str]:
        """Get the ids of the team's agents

        :return: tuple with the ids of the team's agents
        :rtype: tuple[str]
        """
        return (agent.get_id() for agent in self.get_agents())

    def get_perception(self) -> Perception:
        """Get the team's perception

        :return: the team's perception
        :rtype: Perception
        """
        return self._perception

    def get_score(self) -> int:
        """Get the team's score

        :return: the team's score
        :rtype: int
        """
        return self._score

    def update_perception(self, board_manager: BoardManager, other_team: 'Team') -> None:
        """Update the team's perception

        :param board_manager: the game's board manager
        :type board_manager: BoardManager
        :param other_team: The other team in the game
        :type other_team: Team
        """
        assert isinstance(board_manager, BoardManager)
        assert isinstance(other_team, Team)

        self._perception.step_time()
        for agent in self.get_agents():
            self._perception.update(board_manager.get_vision(agent, other_team.get_agents()))

    def reset(self) -> None:
        """Reset all the agents in the team, and the team score
        """
        for agent in self.get_agents():
            agent.respawn()
        self._score = 0

    def __str__(self) -> str:
        out = 'Team\n'
        out += str(list(self.get_ids())) + '\n'
        out += str(self._perception) + '\n'
        return out
