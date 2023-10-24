from utils.cell import Cell
from utils.board import Board
from back.agent import Agent


class BoardManager():
    _board: Board

    def __init__(self) -> None:
        self._board = Board()

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

        cells = [[Cell['EMPTY'] for y in range(len(source))] for x in range(len(source[0]))]

        y = 0
        for line in source:
            x = 0
            for char in line.rstrip('\n'):
                cells[x][y] = translation[char]
                x += 1
            y += 1
        self._board.set_board(cells)

    def get_cell(self, position: tuple[int, int]) -> Cell:
        assert isinstance(position, tuple)
        assert len(position) == 2
        assert isinstance(position[0], int)
        assert isinstance(position[1], int)

        return self._board.get_cell(position[0], position[1])

    def get_all_cells(self) -> list[list[Cell]]:
        return self._board.get_all()

    def get_board_size(self) -> tuple[int, int]:
        return self._board.get_size()

    def set_cell(self, position: tuple[int, int], cell: Cell) -> None:
        assert isinstance(position, tuple)
        assert len(position) == 2
        assert isinstance(position[0], int)
        assert isinstance(position[1], int)
        assert isinstance(cell, Cell)

        self._board.set_cell(position[0], position[1], cell)

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

    def get_vision(self, agent: Agent, agents: list[Agent]) -> tuple[Board, tuple[tuple[str, int, int]]]:
        assert isinstance(agent, Agent)
        assert isinstance(agents, list)
        assert len(agents) > 0
        assert isinstance(agents[0], Agent)

        # board vision
        width, height = self._board.get_size()
        board = Board()
        board.set_board(
            [[Cell['UNKNOWN'] for y in range(height)] for x in range(width)]
            )
        x, y = agent.get_position()
        self._board.set_cell(x, y, self._board.get_cell(x, y))
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            distance = 1
            cur_x = x + dx * distance
            cur_y = y + dy * distance
            while (0 <= cur_x < width and
                  0 <= cur_y < height and
                  self._board.get_cell(cur_x, cur_y) != Cell['WALL']):
                board.set_cell(cur_x, cur_y, self._board.get_cell(cur_x, cur_y))
                board.set_cell(cur_x + dy, cur_y + dx, self._board.get_cell(cur_x + dy, cur_y + dx))
                board.set_cell(cur_x - dy, cur_y - dx, self._board.get_cell(cur_x - dy, cur_y - dx))

                distance += 1
                cur_x = dx * distance
                cur_y = dy * distance

        # vision of other agents
        agents_seen = [(agent.get_id(), agent.get_x(), agent.get_y())]
        for a in agents:
            if a == agent:
                continue
            x, y = a.get_position()
            if board.get_cell(x, y) != Cell['UNKNOWN']:
                agents_seen.append((a.get_id(), x, y))

        return (board, tuple(agents_seen))
