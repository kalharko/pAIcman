from back.agent import Agent


class Pacman(Agent):
    """Class describing a pacman agent
    """

    # Has the pacman eaten a pacgum
    _pacgum: bool
    _invincibility_time: int

    def __init__(self, team: int, id: str, x: int, y: int) -> None:
        super().__init__(team, id, x, y)
        self._pacgum = False

    def eat_pacgum(self) -> None:
        self._pacgum = True
        self._invincibility_time = 20

    def vulnerable(self) -> None:
        self._pacgum = False

    def invicibility_left(self) -> bool:
        return self._invincibility_time > 0

    def reduce_invicibility(self) -> None:
        self._invincibility_time -= 1

    def is_invicible(self) -> bool:
        return self._pacgum
