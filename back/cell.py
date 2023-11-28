from enum import Enum


class Cell(Enum):
    """Enum describing the possible states of a cell
    """
    EMPTY = 0
    WALL = 1
    PAC_DOT = 2
    PAC_GUM = 3
    UNKNOWN = 4
