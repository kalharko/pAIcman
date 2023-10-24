from utils.board import Board
from utils.cell import Cell
from copy import deepcopy
from back.agent import Agent


class Perception():
    _board: Board
    _last_seen: dict[str: list[int, int, int]]  # time, x, y

    def __init__(self, board_size: tuple[int, int], agent_ids: tuple[str]) -> None:
        assert isinstance(board_size, tuple)
        assert len(board_size) > 0
        assert isinstance(board_size[0], int)
        assert isinstance(agent_ids, tuple)
        assert len(agent_ids) > 0
        assert isinstance(agent_ids[0], str)

        self._board = Board()
        self._board.set_board(
            [[Cell['UNKNOWN'] for y in range(board_size[1])] for x in range(board_size[0])]
            )
        self._last_seen = {id: [None, None, None] for id in agent_ids}

    def set_board(self, board: Board) -> None:
        assert isinstance(board, Board)

        self._board = deepcopy(Board)

    def step_time(self) -> None:
        for key in self._last_seen.keys():
            if self._last_seen[key][0] is not None:
                self._last_seen[key][0] += 1

    def update(self, board: Board, agent_seen: tuple[tuple[str, int, int]]) -> None:
        assert board.get_size() == self._board.get_size()

        # board update
        width, height = self._board.get_size()
        for y in range(height):
            for x in range(width):
                cell = board.get_cell(x, y)
                if cell != Cell['UNKNOWN']:
                    self._board.set_cell(x, y, cell)

        # agent position update
        for id, x, y in agent_seen:
            self._last_seen[id] = [0, x, y]

    def __str__(self) -> str:
        return str(self._board) + '\n' + str(self._last_seen)
