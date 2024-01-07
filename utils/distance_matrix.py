from back.cell import Cell
from back.perception import Perception
from utils.direction import Direction


class DistanceMatrix:
    def __init__(self, distances: dict[tuple[int], dict[tuple[int], int]]) -> None:
        self.distances = distances

    def get_distance(self, perception: Perception, position1: tuple[int], position2: tuple[int]) -> int:
        assert isinstance(perception, Perception)
        assert isinstance(position1, tuple)
        assert isinstance(position2, tuple)
        assert len(position1) == len(position2) == 2
        assert isinstance(position1[0], int)
        assert isinstance(position1[1], int)
        assert isinstance(position2[0], int)
        assert isinstance(position2[1], int)

        board = perception.get_board()
        width, height = board.get_size()
        added_distance = 0

        def manhatan(pos1, pos2) -> int:
            return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

        if board.get_cell(position1) == Cell['UNKNOWN']:
            # find the closest known cell
            closest_position = None
            closest_distance = 10000
            for y in range(height):
                for x in range(width):
                    if board.get_cell((x, y)) in (Cell['UNKNOWN'], Cell['WALL']):
                        continue
                    if (dist := manhatan((x, y), position1)) < closest_distance:
                        closest_position = (x, y)
                        closest_distance = dist
            position1 = closest_position
            added_distance += closest_distance

        if board.get_cell(position2) == Cell['UNKNOWN']:
            # find the closest known cell
            closest_position = None
            closest_distance = 10000
            for y in range(height):
                for x in range(width):
                    if board.get_cell((x, y)) in (Cell['UNKNOWN'], Cell['WALL']):
                        continue
                    if (dist := manhatan((x, y), position2)) < closest_distance:
                        closest_position = (x, y)
                        closest_distance = dist
            position2 = closest_position
            added_distance += closest_distance

        return self.distances[position1][position2] + added_distance
