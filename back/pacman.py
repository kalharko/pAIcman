from back.agent import Agent


class Pacman(Agent):
    def __init__(self, id: str, x: int, y: int) -> None:
        super().__init__(id, x, y)
