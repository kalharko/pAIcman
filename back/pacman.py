from back.agent import Agent


class Pacman(Agent):
    """Class describing a pacman agent
    """
    def __init__(self, team: int, id: str, x: int, y: int) -> None:
        super().__init__(team, id, x, y)
