from back.direction import Direction


class Agent():
    _id: str
    _x: int
    _y: int
    _last_direction: Direction

    def __init__(self, id: str, x: int, y: int) -> None:
        assert isinstance(id, str)
        assert isinstance(x, int)
        assert isinstance(y, int)

        self._id = id
        self._x = x
        self._y = y
        self._last_direction = Direction['UP']

    def get_position(self) -> tuple[int, int]:
        return (self.x, self.y)

    def get_last_direction(self) -> Direction:
        return self._last_direction

    def get_id() -> str:
        return self._id

    def move(direction: Direction) -> None:
        assert isinstance(direction, Direction)

        if direction == Direction['UP']:
            x, y = 0, -1
        elif direction == Direction['RIGHT']:
            x, y = 1, 0
        elif direction == Direction['DOWN']:
            x, y = 0, 1
        elif direction == Direction['LEFT']:
            x, y = -1, 0

        self._x += x
        self._y += y

        self._last_direction = direction

    def try_move(direction: Direction) -> tuple[int, int]:
        assert isinstance(direction, Direction)

        if direction == Direction['UP']:
            x, y = 0, -1
        elif direction == Direction['RIGHT']:
            x, y = 1, 0
        elif direction == Direction['DOWN']:
            x, y = 0, 1
        elif direction == Direction['LEFT']:
            x, y = -1, 0

        return (self._x + x, self._y + y)
