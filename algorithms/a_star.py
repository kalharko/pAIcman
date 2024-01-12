import random
from astar.search import AStar as ImportedAStar
from back.board import Board
from back.cell import Cell
from utils.direction import Direction
from copy import deepcopy


class AStar():
    _cells: list[list[int]]
    _cells_with_agents: list[list[int]]

    def __init__(self) -> None:
        self._cells = None
        self._cells_with_agents = None
        self.astar = ImportedAStar(None)

    def load_perception(self, team) -> None:

        perception = team.get_perception()
        self.load_board(perception.get_board())
        self._cells_with_agents = deepcopy(self._cells)

        for sighting_age, agent in perception.get_sightings():
            if agent.is_alive() and sighting_age < 2:
                self._cells_with_agents[agent.get_position()[0]][agent.get_position()[1]] = 1

        for agent in team.get_agents():
            if agent.is_alive():
                self._cells_with_agents[agent.get_position()[0]][agent.get_position()[1]] = 1

        self.astar.world = self._cells_with_agents

    def load_board(self, board: Board) -> None:
        assert isinstance(board, Board)

        self._cells = deepcopy(board.get_all())
        width, height = board.get_size()
        for x in range(width):
            for y in range(height):
                if self._cells[x][y] == Cell['WALL']:
                    self._cells[x][y] = 1
                else:
                    self._cells[x][y] = 0
        self.astar.world = self._cells

    def distance(self, start: tuple[int], goal: tuple[int]) -> int:
        if (path := self.astar.search(start, goal)) is None:
            return 100
        return len(path)

    def path(self, start: tuple[int], goal: tuple[int]) -> list[tuple[int]]:
        return self.astar.search(start, goal)

    def first_step_of_path(self, start: tuple[int], goal: tuple[int]) -> Direction:
        if start == goal:
            # print('astar with start equal to goal')
            return random.choice((Direction['UP'], Direction['DOWN'], Direction['LEFT'], Direction['RIGHT']))
        path = self.path(start, goal)
        if path is None:
            self.astar.world = self._cells
            path = self.path(start, goal)
            if self._cells_with_agents is not None:
                self.astar.world = self._cells_with_agents

        # diff premier mouvement moins le start pour avoir la direction
        first_direction = (path[1][0] - start[0], path[1][1] - start[1])  # tuple
        return Direction(first_direction)
