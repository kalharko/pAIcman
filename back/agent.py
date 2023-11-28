from utils.direction import Direction


class Agent():
    """Class describing an agent's state
    """
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
        """Agent's initialization

        :param team: agent's team id
        :type team: int
        :param id: agent's id
        :type id: str
        :param x: agent's initial x position
        :type x: int
        :param y: agent's initial y position
        :type y: int
        """
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
        self._alive = True
        self._respawn_time = 8

    def get_position(self) -> tuple[int, int]:
        """Get agent's position

        :return: agent's position (x, y)
        :rtype: tuple[int, int]
        """
        return (self._x, self._y)

    def get_last_direction(self) -> Direction:
        """Get agent's last applied direction

        :return: direction enum
        :rtype: Direction
        """
        return self._last_direction

    def get_id(self) -> str:
        """Get agent's id

        :return: agent's id
        :rtype: str
        """
        return self._id

    def add_score(self, value: int) -> None:
        """Increment agent's score

        :param value: value to add to the agent's score
        :type value: int
        """
        assert isinstance(value, int)

        self._score += value

    def get_score(self) -> int:
        """Get agent's score

        :return: agent's score
        :rtype: int
        """
        return self._score

    def move(self, direction: Direction) -> None:
        """Move the agent in the given direction for a distance of 1

        :param direction: direction enum in wich to move the agent
        :type direction: Direction
        """
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
        """Return's the position the agent would in if it moved in the given direction

        :param direction: direction to fake move the agent in
        :type direction: Direction
        :return: the position the agent would be in if the direction was applied (x, y)
        :rtype: tuple[int, int]
        """
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
        """Sets the agent's position to it's original position
        """
        self._x = self._start_x
        self._y = self._start_y

    def get_team(self) -> int:
        """Get the agent's team id

        :return: the agent's team id
        :rtype: int
        """
        return self._team

    def get_x(self) -> int:
        """Get agent's x position

        :return: agent's x position
        :rtype: int
        """
        return self._x

    def get_y(self) -> int:
        """Get agent's y position

        :return: agent's y position
        :rtype: int
        """
        return self._y

    def __str__(self) -> str:
        return f'{self._id} : {self.get_position()}'
