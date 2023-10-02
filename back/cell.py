from enum import Enum


class Cell(Enum):
    EMPTY = 0
    WALL = 1
    DOOR = 2
    PAC_DOT = 3
    PAC_GUM = 4
    PIPE = 5
