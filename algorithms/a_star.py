from astar.search import AStar as ImportedAStar
from back.board import Board
from back.cell import Cell
import copy


class AStar():
    def __init__(self, board: Board):
        assert isinstance(board, Board)

        self.cells = copy.deepcopy(board.get_all())
        width, height = board.get_size()
        for x in range(width):
            for y in range(height):
                if self.cells[x][y] in (Cell['WALL'], Cell['DOOR']):
                    self.cells[x][y] = 1
                else:
                    self.cells[x][y] = 0
        self.astar = ImportedAStar(self.cells)

    def distance(self, start: tuple[int], goal: tuple[int]) -> int:
        if (path := self.astar.search(start, goal)) is None:
            return 100
        return len(path)

    def path(self, start: tuple[int], goal: tuple[int]) -> int:
        return self.astar.search(start, goal)
