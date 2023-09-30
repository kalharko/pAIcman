from back.cell import Cell
from back.agent import Agent

import os.path.exist as does_path_exist


class BoardManager():
    _cells: list[list[Cell]]

    def __init__(self) -> None:
        self._cells = None

    def load(self, path: str) -> None:
        assert isinstance(path, str)
        assert does_path_exist(path)

        pass  # TODO

    def get_cell(self, position: tuple[int, int]) -> Cell:
        assert isinstance(position, tuple)
        assert len(position) == 2
        assert isinstance(position[0], int)
        assert isinstance(position[1], int)

        return self._cells[x][y]

    def set_cell(self, position: tuple[int, int], cell: Cell) -> None:
        assert isinstance(position, tuple)
        assert len(position) == 2
        assert isinstance(position[0], int)
        assert isinstance(position[1], int)
        assert isinstance(cell, Cell)

        self._cells[x][y] = cell

    def get_collisions(self, agents: list[Agent]) -> list[tuple[str, str]]:
        assert isinstance(agents, list)
        assert len(agents) > 0
        assert isinstance(agents[0], Agent)

        out = []
        for agent in agents:
            collisions = []
            # collision with cell content
            if cell := self.get_cell(agent.get_position()) != Cell['EMPTY']:
                collisions.append(cell)

            # collision with other agents
            for other_agent in agents:
                if other_agent == agent:
                    continue
                if agent.get_position() == other_agent.get_position():
                    collisions.append(other_agent.get_id())

            for col in collisions:
                if (col, agent.get_id()) not in out:
                    out.append(agent.get_id(), col)
        return out
