from utils.direction import Direction


class Agent():
    _id: str
    _x: int
    _y: int
    _start_x: int
    _start_y: int
    _last_direction: Direction
    _score: int
    _team: int
    # Is the agent alive
    _alive: bool
    # Number of steps before the agent respawns
    _respawn_time: int

    def __init__(self, team: int, id: str, x: int, y: int) -> None:
        assert isinstance(team, int)
        assert team in (0, 1)
        assert isinstance(id, str)
        assert isinstance(x, int)
        assert isinstance(y, int)

        self._id = id
        self._x = x
        self._y = y
        self._start_x = x
        self._start_y = y
        self._last_direction = Direction['UP']
        self._score = 0
        self._team = team
        self._alive = true
        self._respawn_time = 4

    def get_position(self) -> tuple[int, int]:
        return (self._x, self._y)

    def get_last_direction(self) -> Direction:
        return self._last_direction

    def get_id(self) -> str:
        return self._id

    def add_score(self, value: int) -> None:
        assert isinstance(value, int)

        self._score += value

    def get_score(self) -> int:
        return self._score

    def move(self, direction: Direction) -> None:
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

    def try_move(self, direction: Direction) -> tuple[int, int]:
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

    def respawn(self):
        self._x = self._start_x
        self._y = self._start_y

    def get_team(self) -> int:
        return self._team

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y
