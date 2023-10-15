class PacErrGeneric(Exception):
    def __init__(self, source: str = 'Unknown') -> None:
        if True:
            print(self.__class__.__name__, source.__class__.__name__)


class PacErrUnknownAgentId(PacErrGeneric):
    pass


class PacErrOutOfBoard(PacErrGeneric):
    pass


class PacErrInvalidAction(PacErrGeneric):
    pass


class PacErrAgentInWall(PacErrGeneric):
    pass
