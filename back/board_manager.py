from back.cell import Cell
from back.agent import Agent


class BoardManager():
    _cells: list[list[Cell]]

    def __init__(self) -> None:
        self._cells = None

    def load(self, source: list[str]) -> None:
        assert isinstance(source, list)
        assert len(source) > 0
        assert isinstance(source[0], str)

        translation = {
            ' ': Cell['EMPTY'],
            '#': Cell['WALL'],
            'D': Cell['DOOR'],
            '.': Cell['PAC_DOT'],
            'O': Cell['PAC_GUM'],
            'P': Cell['WALL']
        }

        self._cells = [[Cell['EMPTY'] for y in range(len(source))] for x in range(len(source[0]) - 1)]

        y = 0
        for line in source:
            x = 0
            for char in line.rstrip('\n'):
                self._cells[x][y] = translation[char]
                x += 1
            y += 1

    def get_cell(self, position: tuple[int, int]) -> Cell:
        assert isinstance(position, tuple)
        assert len(position) == 2
        assert isinstance(position[0], int)
        assert isinstance(position[1], int)

        return self._cells[position[0]][position[1]]

    def get_all_cells(self) -> list[list[Cell]]:
        return self._cells

    def set_cell(self, position: tuple[int, int], cell: Cell) -> None:
        assert isinstance(position, tuple)
        assert len(position) == 2
        assert isinstance(position[0], int)
        assert isinstance(position[1], int)
        assert isinstance(cell, Cell)

        self._cells[position[0]][position[1]] = cell

    def get_collisions(self, agents: list[Agent]) -> list[tuple[str, str]]:
        assert isinstance(agents, list)
        assert len(agents) > 0
        assert isinstance(agents[0], Agent)

        out = []
        for agent in agents:
            collisions = []
            # collision with cell content
            if (cell := self.get_cell(agent.get_position())) != Cell['EMPTY']:
                collisions.append(cell)

            # collision with other agents
            for other_agent in agents:
                if other_agent == agent:
                    continue
                if agent.get_position() == other_agent.get_position():
                    collisions.append((other_agent.get_id()))

            for col in collisions:
                if (col, agent.get_id()) not in out:
                    out.append((agent.get_id(), col))
        return out
