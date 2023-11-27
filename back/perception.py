from back.agent import Agent
from back.board import Board
from back.cell import Cell
from copy import deepcopy

from back.pacman import Pacman


class Perception():
    """Class describing a perception of the pacman game (agent or team)
    """
    _board: Board
    _pacman_sightings: dict[str: tuple[int, int, int]]  # id: time, x, y
    _ghost_sightings: dict[str: tuple[int, int, int]]  # id: time, x, y
    _last_cell_seen: list[tuple[int, int]]  # x, y

    def __init__(self, board_size: tuple[int, int]) -> None:
        """Perception's initialization

        :param board_size: game board's size
        :type board_size: tuple[int, int]
        """
        assert isinstance(board_size, tuple)
        assert len(board_size) > 0
        assert isinstance(board_size[0], int)

        self._board = Board()
        self._board.set_board(
            [[Cell['UNKNOWN'] for y in range(board_size[1])] for x in range(board_size[0])])
        self._agents_seen = {}
        self._last_cell_seen = []

    def set_board(self, board: Board) -> None:
        """Set the perception's board

        :param board: board to set
        :type board: Board
        """
        assert isinstance(board, Board)

        self._board = deepcopy(Board)

    def step_time(self) -> None:
        """Step the time in the perception, increase the counters telling how long ago we saw each agents
        """
        # step_time
        for key in self._agents_seen.keys():
            if self._agents_seen[key][0] is not None:
                self._agents_seen[key][0] += 1
        # refresh last cell seen
        self._last_cell_seen = []

    def update(self, other: 'Perception') -> None:
        """Update a peception with the informations of an other

        :param other: other perception with the update informations
        :type other: Perception
        """
        assert isinstance(other, Perception)

        # update board
        width, height = self._board.get_size()
        other_board = other.get_board()
        for x in range(width):
            for y in range(height):
                if other_board.get_cell(x, y) == Cell['UNKNOWN']:
                    continue
                if (x, y) not in self._last_cell_seen:
                    self._last_cell_seen.append((x, y))
                self._board.set_cell(x, y, other_board.get_cell(x, y))
        # update Pacman seen
        for id, value in other.get_pacman_sightings().items():
            if value[0] == 0:
                self._pacman_sightings[id] = value
        # update Ghosts seen
        for id, value in other.get_ghost_sightings().items():
            if value[0] == 0:
                self._ghost_sightings[id] = value

    def get_board(self) -> Board:
        """Get the perception's board

        :return: the perception's board
        :rtype: Board
        """
        return self._board

    def get_pacman_sightings(self) -> dict:
        """Get the perception's sightings

        :return: A dict {agent_id: (time, x, y)} storing the time and position of last sighting
        :rtype: dict
        """
        return self._pacman_sightings

    def get_ghost_sightings(self) -> dict:
        """Get the perception's sightings

        :return: A dict {agent_id: (time, x, y)} storing the time and position of last sighting
        :rtype: dict
        """
        return self._ghost_sightings

    def update_sightings(self, agent: Agent) -> None:
        """Update the sighting informations of a given agent

        :param agent: agent to add to the sightings
        :type agent: Agent
        """
        pos = agent.get_position()
        if isinstance(agent, Pacman):
            self._pacman_sightings[agent.get_id()] = (0, pos[0], pos[1])
        else:
            self._ghost_sightings[agent.get_id()] = (0, pos[0], pos[1])

    def __str__(self) -> str:
        out = str(self._board)
        width, height = self._board.get_size()
        for id, value in self._agents_seen.items():
            if value[0] != 0:
                continue
            print(value)
            _, pos = value
            x, y = pos
            out = out[:(width + 1) * y + x] + id[0] + out[(width + 1) * y + x + 1:]
        return out + str(self._agents_seen) + '\n'
