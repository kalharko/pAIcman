from back.cell import Cell
from utils.direction import Direction


class Board():
    """Class storing the description of a pacman's board
    """
    _cells: list[list[Cell]]
    _width: int
    _height: int

    def __init__(self) -> None:
        self._cells = None
        self._height = 0
        self._width = 0

    def set_board(self, board: list[list[Cell]]) -> None:
        """Set the board description

        :param board: board description to be set
        :type board: list[list[Cell]]
        """
        assert isinstance(board, list)
        assert len(board) > 0
        assert isinstance(board[0], list)
        assert len(board[0]) > 0
        assert isinstance(board[0][0], Cell)

        self._cells = board
        self._height = len(self._cells[0])
        self._width = len(self._cells)

    def set_cell(self, x: int, y: int, value: Cell) -> None:
        """Set a cell's value

        :param x: x position of the cell to set
        :type x: int
        :param y: y position of the cell to set
        :type y: int
        :param value: value to set
        :type value: Cell
        """
        assert isinstance(x, int)
        assert isinstance(y, int)
        assert 0 <= x < self._width
        assert 0 <= y < self._height
        assert isinstance(value, Cell)

        self._cells[x][y] = value

    def get_cell(self, x: int, y: int) -> Cell:
        """Get a cell's value

        :param x: x position of the cell to get
        :type x: int
        :param y: y position of the cell to get
        :type y: int
        :return: cell's value
        :rtype: Cell
        """
        assert isinstance(x, int)
        assert isinstance(y, int)
        assert 0 <= x < self._width
        assert 0 <= y < self._height

        return self._cells[x][y]

    def get_cell_neighbors(self, x: int, y: int) -> list[Cell]:
        """Get a cell's neighbors

        :param x: x position of the cell whose neighbors we want
        :type x: int
        :param y: y position of the cell whose neighbors we want
        :type y: int
        :return: list of the positions of the cell's neighbors
        :rtype: list[Cell]
        """
        assert isinstance(x, int)
        assert isinstance(y, int)
        assert 0 <= x < self._width
        assert 0 <= y < self._height

        out = []
        for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, -1)):
            out.append(self._cells[x + dx][y + dy])
        return out

    def get_next_cell(self,x, y, direction: Direction) -> Cell:
        """Get the next after moving in a certain direction

        :param x: x position of the cell whose neighbors we want
        :type x: int
        :param y: y position of the cell whose neighbors we want
        :type y: int
        :param direction : the direction where we move
        :type direction : Direction

        :return : the cell where we arrive after moving in the direction
        :rtype : Cell
        """
        assert isinstance(x, int)
        assert isinstance(y, int)
        assert 0 <= x < self._width
        assert 0 <= y < self._height
        (dx, dy) = direction
        return self._cells[x + dx][y + dy]



    def get_all(self) -> list[list[Cell]]:
        """Get the full description of the board

        :return: the full description of the board
        :rtype: list[list[Cell]]
        """
        return self._cells

    def get_size(self) -> tuple[int, int]:
        """Get the board's size

        :return: the board's size (width, height)
        :rtype: tuple[int, int]
        """
        return (self._width, self._height)

    def get_legal_move(self, x : int, y : int) -> list[Direction]:
        """
        Get all the move that the agent is able to do in a given position (x, y)

        :param x: x position of the cell we are
        :type x: int
        :param y: y position of the cell we are
        :type y: int
        :return: list of the direction we can move
        :rtype: list[Direction]
        """

        legal_move = []
        for direction in Direction:
            if self.get_next_cell(x, y, direction).is_movable():
                legal_move.append(direction)
        return legal_move

    def __str__(self) -> str:
        translation = {
            Cell['EMPTY']: ' ',
            Cell['WALL']: '#',
            Cell['DOOR']: '_',
            Cell['PAC_DOT']: '.',
            Cell['PAC_GUM']: 'o',
            Cell['PIPE']: 'P',
            Cell['UNKNOWN']: '~'
        }
        out = ''
        for y in range(self._height):
            for x in range(self._width):
                out += translation[self._cells[x][y]]
            out += '\n'
        return out
