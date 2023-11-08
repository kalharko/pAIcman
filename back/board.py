from back.cell import Cell


class Board():
    _cells: list[list[Cell]]
    _width: int
    _height: int

    def __init__(self) -> None:
        self._cells = None
        self._height = 0
        self._width = 0

    def set_board(self, board: list[list[Cell]]) -> None:
        assert isinstance(board, list)
        assert len(board) > 0
        assert isinstance(board[0], list)
        assert len(board[0]) > 0
        assert isinstance(board[0][0], Cell)

        self._cells = board
        self._height = len(self._cells[0])
        self._width = len(self._cells)

    def set_cell(self, x: int, y: int, value: Cell) -> None:
        assert isinstance(x, int)
        assert isinstance(y, int)
        assert 0 <= x < self._width
        assert 0 <= y < self._height
        assert isinstance(value, Cell)

        self._cells[x][y] = value

    def get_cell(self, x: int, y: int) -> Cell:
        assert isinstance(x, int)
        assert isinstance(y, int)
        assert 0 <= x < self._width
        assert 0 <= y < self._height

        return self._cells[x][y]

    def get_all(self) -> list[list[Cell]]:
        return self._cells

    def get_size(self) -> tuple[int, int]:
        return (self._width, self._height)

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
