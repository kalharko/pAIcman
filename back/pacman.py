from back.agent import Agent


class Pacman(Agent):
    """Class describing a pacman agent
    """

    # Has the pacman eaten a pacgum
    _pacgum: bool

    def __init__(self, team: int, id: str, x: int, y: int) -> None:
        super().__init__(team, id, x, y)
        self._pacgum = False

    def eat_pacgum(self) -> None:
        self._pacgum = True

    def is_invicible(self) -> bool:
        return self._pacgum
