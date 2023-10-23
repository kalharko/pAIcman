from utils.board import Board
from copy import deepcopy

class Perception:
    _board: Board
    _last_seen: dict[str, int]

    def __init__(self, board: Board, agent_ids: list[str]) -> None:
        assert isinstance(board, Board)
        assert isinstance(agent_ids, list)
        assert len(agent_ids) > 0
        assert isinstance(agent_ids[0], str)

        self._board = deepcopy(board)
        self._last_seen = {id: None for id in agent_ids}

    def update(self, other: 'Perception') -> None:
        pass
