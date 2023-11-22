from enum import Enum

from utils.direction import Direction


class Cell(Enum):
    """Enum describing the possible states of a cell
    """
    EMPTY = 0
    WALL = 1
    DOOR = 2
    PAC_DOT = 3
    PAC_GUM = 4
    PIPE = 5
    UNKNOWN = 6

    def is_movable(self) -> bool:
        return self == Cell.EMPTY or self == Cell.PAC_DOT or self == Cell.PAC_GUM or self  == Cell.PIPE



