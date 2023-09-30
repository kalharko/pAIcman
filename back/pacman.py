from back.agent import Agent


class Pacman(Agent):
    _score: int

    def __init__(self, id: str, x: int, y: int) -> None:
        super().__init__(id, x, y)

        self._score = 0

    def add_score(self, value: int) -> None:
        assert isinstance(value, int)

        self._score += value

    def get_score(self) -> int:
        return self._score
