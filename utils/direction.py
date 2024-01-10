from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    NONE = (0, 0)
    RESPAWN = (1, 1)

    def opposite(self):
        match self:
            case Direction.UP:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.UP
            case Direction.LEFT:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.LEFT
            case Direction.RESPAWN:
                return Direction.RESPAWN
            case Direction.NONE:
                print('asks for oposite of direction NONE and dont like it')
                return Direction.NONE


