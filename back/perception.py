from back.board import Board
from back.cell import Cell
from copy import deepcopy


class Perception():
    _board: Board
    _last_seen: dict[str: list[int, int, int]]  # time, x, y

    def __init__(self, board_size: tuple[int, int]) -> None:
        assert isinstance(board_size, tuple)
        assert len(board_size) > 0
        assert isinstance(board_size[0], int)

        self._board = Board()
        self._board.set_board(
            [[Cell['UNKNOWN'] for y in range(board_size[1])] for x in range(board_size[0])])
        self._last_seen = {}

    def set_board(self, board: Board) -> None:
        assert isinstance(board, Board)

        self._board = deepcopy(Board)

    def step_time(self) -> None:
        for key in self._last_seen.keys():
            if self._last_seen[key][0] is not None:
                self._last_seen[key][0] += 1

    def update(self, other: 'Perception') -> None:
        assert isinstance(other, Perception)

        # update board
        width, height = self._board.get_size()
        other_board = other.get_board()
        for x in range(width):
            for y in range(height):
                if self._board.get_cell(x, y) == Cell['UNKNOWN']:
                    self._board.set_cell(x, y, other_board.get_cell(x, y))
        # update agents seen
        for id, value in other.get_last_seen().items():
            if value[0] == 0:
                self._last_seen[id] = list(value)

    def get_board(self) -> Board:
        return self._board

    def get_last_seen(self) -> dict:
        return self._last_seen

    def update_agent_seen(self, agent_id, position) -> None:
        self._last_seen[agent_id] = (0, position)

    def __str__(self) -> str:
        return str(self._board) + str(self._last_seen) + '\n'
