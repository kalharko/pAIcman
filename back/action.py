from back.direction import Direction


class Action():
    id: str
    direction: Direction

    def __init__(self, id: str, direction: Direction) -> None:
        assert isinstance(id, str)
        assert isinstance(direction, Direction)

        self.id = id
        self.direction = direction
