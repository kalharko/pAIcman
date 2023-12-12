import copy
from back.perception import Perception
from back.cell import Cell
from back.board import Board
from back.agent import Agent


class BoardManager():
    """Class managing a board object
    """
    _board: Board
    _initial_board: Board

    def __init__(self) -> None:
        self._board = Board()

    def load(self, source: list[str]) -> None:
        """Load board from extracted file information

        :param source: list of lines read in the map file
        :type source: list[str]
        """
        assert isinstance(source, list)
        assert len(source) > 0
        assert isinstance(source[0], str)

        translation = {
            ' ': Cell['EMPTY'],
            '#': Cell['WALL'],
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
        """Get the cell at the given position

        :param position: position of the cell to be returned (x, y)
        :type position: tuple[int, int]
        :return: cell value
        :rtype: Cell
        """
        assert isinstance(position, tuple)
        assert len(position) == 2
        assert isinstance(position[0], int)
        assert isinstance(position[1], int)

        return self._board.get_cell(position)

    def get_all_cells(self) -> list[list[Cell]]:
        """Get the whole board description

        :return: whole board description
        :rtype: list[list[Cell]]
        """

        return self._board.get_all()

    def get_board_size(self) -> tuple[int, int]:
        """Get the board's size

        :return: board's size
        :rtype: tuple[int, int]
        """

        return self._board.get_size()

    def set_cell(self, position: tuple[int, int], cell: Cell) -> None:
        """Set a cell's value

        :param position: position of the cell to set
        :type position: tuple[int, int]
        :param cell: value of the cell to set
        :type cell: Cell
        """
        assert isinstance(position, tuple)
        assert len(position) == 2
        assert isinstance(position[0], int)
        assert isinstance(position[1], int)
        assert isinstance(cell, Cell)

        self._board.set_cell(position, cell)

    # Get all the collisions on the board
    def get_collisions(self, agents: tuple[Agent]) -> list[tuple[str, str]]:
        """
        TODO : william will overwrite this non functioning function
        """
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
        """Get agent's vision

        :param agent: which agent's vision we are computing
        :type agent: Agent
        :param other_team_agents: list of the other team's agents
        :type other_team_agents: tuple[Agent]
        :return: Agent's perception
        :rtype: Perception
        """
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
                board.set_cell((cur_x, cur_y), self._board.get_cell((cur_x, cur_y)))
                board.set_cell((cur_x + dy, cur_y + dx), self._board.get_cell((cur_x + dy, cur_y + dx)))
                board.set_cell((cur_x - dy, cur_y - dx), self._board.get_cell((cur_x - dy, cur_y - dx)))

                if self._board.get_cell((cur_x, cur_y)) == Cell['WALL']:
                    break

                distance += 1
                cur_x = x + dx * distance
                cur_y = y + dy * distance

        # vision of other agents
        for a in other_team_agents:
            if a == agent:
                continue
            x, y = a.get_position()
            if board.get_cell((x, y)) != Cell['UNKNOWN']:
                out.update_sightings(a)
        return out

    def reset(self) -> None:
        """Reset the board to it's initial state
        """
        self._board = copy.deepcopy(self._initial_board)
