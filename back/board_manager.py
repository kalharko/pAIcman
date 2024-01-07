import copy
import os
import pickle
from algorithms.a_star import AStar
from back.perception import Perception
from back.cell import Cell
from back.board import Board
from back.agent import Agent
from utils.distance_matrix import DistanceMatrix


class BoardManager():
    """Class managing a board object
    """
    _board: Board
    _initial_board: Board
    _path_to_board: str

    def __init__(self) -> None:
        self._board = Board()
        self._path_to_board = None

    def load(self, source: list[str], path: str) -> None:
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

        cells = [[Cell['EMPTY'] for y in range(len(source))] for x in range(len(source[0].rstrip('\n')))]

        y = 0
        for line in source:
            x = 0
            for char in line.rstrip('\n'):
                cells[x][y] = translation[char]
                x += 1
            y += 1
        self._board.set_board(cells)
        self._path_to_board = path
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

    def get_collisions(self, agent: Agent) -> tuple[str]:
        """Get the board collisions for an agent

        :param agent: agent for which we want to get the collisions
        :type agent: Agent

        :return: tuple of the agents collisions
        :rtype: tuple
        """

        assert isinstance(agent, Agent)

        collisions = []

        # collision with cell content
        if (cell := self.get_cell(agent.get_position())) != Cell['EMPTY']:
            collisions.append(cell)

        return collisions

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
                print(cur_x, cur_y)
                board.set_cell((cur_x, cur_y), self._board.get_cell((cur_x, cur_y)))
                if dy == 0:
                    board.set_cell((cur_x, cur_y + dy), self._board.get_cell((cur_x, cur_y + dy)))
                    board.set_cell((cur_x, cur_y - dy), self._board.get_cell((cur_x, cur_y - dy)))
                if dx == 0:
                    board.set_cell((cur_x + dx, cur_y), self._board.get_cell((cur_x + dx, cur_y)))
                    board.set_cell((cur_x - dx, cur_y), self._board.get_cell((cur_x - dx, cur_y)))

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

    def is_game_over(self) -> bool:
        """Check if the game is over

        :return: True if the game is over, False if it is not
        :rtype: bool
        """
        for y in range(self._board.get_size()[1]):
            for x in range(self._board.get_size()[0]):
                if self._board.get_cell((x, y)) == Cell['PAC_DOT']:
                    return False
        return True

    def get_board_distances(self) -> DistanceMatrix:
        files = os.listdir('maps/distances/')
        save_file_name = os.path.basename(self._path_to_board).rstrip('.txt') + '_distances.pkl'
        if save_file_name in files:
            return DistanceMatrix(pickle.load(open('maps/distances/' + save_file_name, 'rb')))

        return DistanceMatrix(self.pre_compute_board_distances())

    def pre_compute_board_distances(self) -> DistanceMatrix:
        """Precompute the distance matrix of all the non wall coordinates in a map. Saves it as a pickle file.

        :param path: path to the map file for wich precomputing is necessary
        :type path: str
        """

        print("\nPrecomputing the board's distance matrix")
        # find all positions to include in the matrix
        width, height = self._board.get_size()
        positions = []
        for y in range(height):
            for x in range(width):
                if self._board.get_cell((x, y)) != Cell['WALL']:
                    positions.append((x, y))

        # initialize a star
        astar = AStar()
        astar.load_board(self._board)

        # compute
        out = dict()
        for pos1 in positions:
            print('\rProgress', positions.index(pos1), '/', len(positions), end='')
            for pos2 in positions:
                if pos1 == pos2:
                    pass

                if pos1 not in out.keys():
                    out[pos1] = dict()
                if pos2 not in out.keys():
                    out[pos2] = dict()

                if pos2 in out[pos1].keys():
                    continue

                distance = astar.distance(pos1, pos2)
                out[pos1][pos2] = distance
                out[pos2][pos1] = distance

        # save
        path = 'maps/distances/' + os.path.basename(self._path_to_board).rstrip('.txt') + '_distances.pkl'
        pickle.dump(out, open(path, 'wb'))
        print('\nPrecomputing done\ndistancest saved at', path, '\n')

        return out
