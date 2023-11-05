import copy
from back.perception import Perception
from back.cell import Cell
from back.board import Board
from back.agent import Agent


class BoardManager():
    _board: Board
    _initial_board: Board

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
        self._initial_board = copy.deepcopy(self._board)

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

    def get_collisions(self, agents: tuple[Agent]) -> list[tuple[str, str]]:
        assert isinstance(agents, tuple)
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

    def get_vision(self, agent: Agent, other_team_agents: tuple[Agent]) -> Perception:
        assert isinstance(agent, Agent)
        assert isinstance(other_team_agents, tuple)
        assert len(other_team_agents) > 0
        assert isinstance(other_team_agents[0], Agent)

        out = Perception(self._board.get_size())
        board = out.get_board()

        # board vision
        width, height = board.get_size()
        x, y = agent.get_position()
        # self._board.set_cell(x, y, self._board.get_cell(x, y))  # wtf is this line ?
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            distance = 0
            cur_x = x + dx * distance
            cur_y = y + dy * distance
            while (0 <= cur_x < width and 0 <= cur_y < height):
                board.set_cell(cur_x, cur_y, self._board.get_cell(cur_x, cur_y))
                board.set_cell(cur_x + dy, cur_y + dx, self._board.get_cell(cur_x + dy, cur_y + dx))
                board.set_cell(cur_x - dy, cur_y - dx, self._board.get_cell(cur_x - dy, cur_y - dx))

                if self._board.get_cell(cur_x, cur_y) == Cell['WALL']:
                    break

                distance += 1
                cur_x = x + dx * distance
                cur_y = y + dy * distance

        # vision of other agents
        out.update_agent_seen(agent.get_id(), agent.get_position())
        for a in other_team_agents:
            if a == agent:
                continue
            x, y = a.get_position()
            if board.get_cell(x, y) != Cell['UNKNOWN']:
                out.update_agent_seen(a.get_id(), (x, y))

        return out

    def reset(self) -> None:
        self._board = copy.deepcopy(self._initial_board)
