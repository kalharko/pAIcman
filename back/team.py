from back.agent import Agent
from back.board_manager import BoardManager
from back.errors import PacErrUnknownAgentId
from back.pacman import Pacman
from back.ghost import Ghost
from back.perception import Perception


class Team():
    _pacman: Pacman
    _ghosts: list[Ghost]
    _perception: Perception
    _score: int

    def __init__(self, board_size: tuple[int, int]) -> None:
        assert isinstance(board_size, tuple)
        assert len(board_size) == 2
        assert isinstance(board_size[0], int)

        self._pacman = None
        self._ghosts = []
        self._perception = Perception(board_size)
        self._score = 0

    def set_pacman(self, value: Pacman) -> None:
        assert isinstance(value, Pacman)

        self._pacman = value

    def add_ghost(self, value: Ghost) -> None:
        assert isinstance(value, Ghost)

        self._ghosts.append(value)

    def get_agents(self) -> tuple[Agent]:
        return tuple([self._pacman] + self._ghosts)

    def get_agent(self, id: str) -> Agent:
        assert isinstance(id, str)

        for agent in self.get_agents():
            if id == agent.get_id():
                return agent
        return PacErrUnknownAgentId(self)

    def get_pacman(self) -> Pacman:
        return self._pacman

    def get_ghosts(self) -> tuple[Ghost]:
        return tuple(self._ghosts)

    def get_ids(self) -> tuple[str]:
        return (agent.get_id() for agent in self.get_agents())

    def get_perception(self) -> Perception:
        return self._perception

    def get_score(self) -> int:
        return self._score

    def update_perception(self, board_manager: BoardManager, other_team: 'Team') -> None:

        self._perception.step_time()
        for agent in self.get_agents():
            self._perception.update(board_manager.get_vision(agent, other_team.get_agents()))

    def reset(self) -> None:
        for agent in self.get_agents():
            agent.respawn()
        self._score = 0
