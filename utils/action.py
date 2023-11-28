from utils.direction import Direction


class Action():
    id: str
    direction: Direction

    def __init__(self, id: str, direction: Direction) -> None:
        assert isinstance(id, str)
        assert isinstance(direction, Direction)

        self.id = id
        self.direction = direction

    def __str__(self) -> str:
        return f'({self.id}, {self.direction})'
