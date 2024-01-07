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

        print('get_distance_matrix', position1, position2)

        board = perception.get_board()
        width, height = board.get_size()
        added_distance = 0
        if board.get_cell(position1) == Cell['UNKNOWN']:
            # find the known cell closest to position1
            closest_position = None
            closest_distances = 1000
            for direction in Direction:
                if direction in (Direction['NONE'], Direction['RESPAWN']):
                    continue
                dx, dy = direction.value
                d = 0
                x = position1[0] + d * dx
                y = position1[1] + d * dy
                while 0 <= x < width and 0 <= y < height and board.get_cell((x, y)) in (Cell['WALL'], Cell['UNKNOWN']):
                    d += 1
                    x = position1[0] + d * dx
                    y = position1[1] + d * dy
                if 0 <= x < width and 0 <= y < height and board.get_cell((x, y)) in (Cell['PAC_DOT'], Cell['PAC_GUM'], Cell['EMPTY']):
                    if d < closest_distances:
                        closest_position = (position1[0] + d * dx, position1[1] + d * dy)
                        closest_distances = d
            position1 = closest_position
            added_distance += closest_distances

        if board.get_cell(position2) == Cell['UNKNOWN']:
            # find the known cell closest to position2
            closest_position = None
            closest_distances = 1000
            for direction in Direction:
                if direction in (Direction['NONE'], Direction['RESPAWN']):
                    continue
                dx, dy = direction.value
                d = 0
                x = position2[0] + d * dx
                y = position2[1] + d * dy
                while 0 <= x < width and 0 <= y < height and board.get_cell((x, y)) in (Cell['WALL'], Cell['UNKNOWN']):
                    d += 1
                    x = position2[0] + d * dx
                    y = position2[1] + d * dy
                if 0 <= x < width and 0 <= y < height and board.get_cell((x, y)) in (Cell['PAC_DOT'], Cell['PAC_GUM'], Cell['EMPTY']):
                    if d < closest_distances:
                        closest_position = (position2[0] + d * dx, position2[1] + d * dy)
                        closest_distances = d
            position2 = closest_position
            added_distance += closest_distances

        return self.distances[position1][position2] + added_distance
