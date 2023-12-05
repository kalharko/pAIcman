
from back.agent import Agent


class Ghost(Agent):
    """Class describing a ghost agent
    """
    _vulnerability: bool

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
        self._vulnerability = False

    def is_vulnerable(self) -> bool:
        """Get the ghost's panic state

        :return: ghost's panic state
        :rtype: _type_
        """
        return self._vulnerability

    def set_vulnerability(self, state: bool) -> None:
        """Set the ghost's vulnerability state

        :param state: True if the ghost is panicking, False if not
        :type state: bool
        """
        assert isinstance(state, bool)

        self._vulnerability = state
