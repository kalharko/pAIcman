from back.board import Board
from back.cell import Cell
from copy import deepcopy


class Perception():
    """Class describing a perception of the pacman game (agent or team)
    """
    _board: Board
    _sightings: dict[str: list[int, int, int]]  # time, x, y
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
        # update agents seen
        for id, value in other.get_sightings().items():
            if value[0] == 0:
                self._agents_seen[id] = list(value)

    def get_board(self) -> Board:
        """Get the perception's board

        :return: the perception's board
        :rtype: Board
        """
        return self._board

    def get_sightings(self) -> dict:
        """Get the perception's sightings

        :return: A dict {agent_id: (time, x, y)} storing the time and position of last sighting
        :rtype: dict
        """
        return self._agents_seen

    def update_sightings(self, agent_id, position) -> None:
        """Update the sighting informations of a given agent

        :param agent_id: id of the agent to update
        :type agent_id: _type_
        :param position: position of the agent to update
        :type position: _type_
        """
        self._agents_seen[agent_id] = (0, position)


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
