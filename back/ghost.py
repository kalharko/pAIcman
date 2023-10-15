
from back.agent import Agent


class Ghost(Agent):
    _panic: bool

    def __init__(self, id: str, x: int, y: int) -> None:
        super().__init__(id, x, y)
        self._panic = False

    def get_panic(self) -> None:
        return self._panic

    def set_panic(self, state: bool) -> None:
        assert isinstance(state, bool)

        self._panic = state
