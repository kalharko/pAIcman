from back.agent import Agent
from back.board import Board
from back.cell import Cell
from copy import deepcopy
from back.ghost import Ghost

from back.pacman import Pacman


class Perception():
    """Class describing a perception of the pacman game (agent or team)
    """
    _board: Board
    _pacman_sighting: list[int, Pacman]  # [time since sighting, Pacman]
    _ghost_sightings: dict[str: list[int, Ghost]]  # id: [time since sighting, Ghost]]
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
        self._last_cell_seen = []
        self._pacman_sighting = None
        self._ghost_sightings = {}

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
        if self._pacman_sighting is not None:
            self._pacman_sighting[0] += 1
        for sighting in self._ghost_sightings.values():
            sighting[0] += 1
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
        sighting = other.get_pacman_sighting()
        if len(sighting) > 0 and sighting[0][0] == 0:
            self._pacman_sighting = [0, deepcopy(sighting[0][1])]
        # update Ghosts seen
        for time, ghost in other.get_ghost_sightings():
            if time == 0:
                self._ghost_sightings[ghost.get_id()] = [0, deepcopy(ghost)]

    def get_board(self) -> Board:
        """Get the perception's board

        :return: the perception's board
        :rtype: Board
        """
        return self._board

    def get_sightings(self) -> list[list[int, Agent]]:
        """Get the perception's sighting of ghosts and pacman combined

        :return: the list of all sightings
        :rtype: list[tuple] [(id, time since sighting, x, y), ...]
        """
        return self.get_ghost_sightings() + self.get_pacman_sighting()

    def get_pacman_sighting(self) -> list[list[int, Pacman]]:
        """Get the perception's pacman sighting

        :return: the pacman sighting
        :rtype: list[int, Pacman]
        """
        if self._pacman_sighting is None:
            return []
        return [self._pacman_sighting]

    def get_ghost_sightings(self) -> list[list[int, Ghost]]:
        """Get the perception's ghost sightings

        :return: the list of ghost sightings
        :rtype: list[list[int, Ghost]]
        """
        return list(self._ghost_sightings.values())

    def update_sightings(self, agent: Agent) -> None:
        """Update the sighting informations of a given agent

        :param agent: agent to add to the sightings
        :type agent: Agent
        """
        if isinstance(agent, Pacman):
            self._pacman_sighting = [0, deepcopy(agent)]
        else:
            self._ghost_sightings[agent.get_id()] = [0, deepcopy(agent)]

    def get_ids(self) -> list[str]:
        """Get ids of all sightings

        :return: list of all ids
        :rtype: list[str]
        """
        return [sighting[1].get_id() for sighting in self.get_sightings()]

    def get_ghost_ids(self) -> list[str]:
        """Get the ids of the ghost that have been seen

        :return: list of ids
        :rtype: list[str]
        """
        return [sighting[1].get_id() for sighting in self.get_ghost_sightings()]

    def __str__(self) -> str:
        out = str(self._board)
        width, _ = self._board.get_size()
        for id, value in self._agents_seen.items():
            if value[0] != 0:
                continue
            print(value)
            _, pos = value
            x, y = pos
            out = out[:(width + 1) * y + x] + id[0] + out[(width + 1) * y + x + 1:]
        return out + str(self._agents_seen) + '\n'
