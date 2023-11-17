
from back.agent import Agent


class Ghost(Agent):
    """Class describing a ghost agent
    """
    _panic: bool

    def __init__(self, team: int, id: str, x: int, y: int) -> None:
        """Ghost initialization

        :param team: ghost's team id
        :type team: int
        :param id: ghost's id
        :type id: str
        :param x: ghost's initial x position
        :type x: int
        :param y: ghost's initial y position
        :type y: int
        """
        super().__init__(team, id, x, y)
        self._panic = False

    def get_panic(self) -> None:
        """Get the ghost's panic state

        :return: ghost's panic state
        :rtype: _type_
        """
        return self._panic

    def set_panic(self, state: bool) -> None:
        """Set the ghost's panic state

        :param state: True if the ghost is panicking, False if not
        :type state: bool
        """
        assert isinstance(state, bool)

        self._panic = state
