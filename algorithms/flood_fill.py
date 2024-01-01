from back.board import Board
from back.cell import Cell


def closest_cell(og_x: int, og_y: int, searching_for: Cell, board: Board) -> int:
    if board.get_cell((og_x, og_y)) == searching_for:
        return 0

    unvisited = [(0, og_x, og_y)]  # (distance, x, y)
    visited = set()  # [(x, y)]
    min_distance_found = 1000

    while unvisited != []:
        # move node from unvisited to visited
        distance, x, y = unvisited.pop(0)
        visited.add((x, y))

        # check neighbors
        for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            # continue if already visited
            if (x + dx, y + dy) in visited:
                continue
            cell = board.get_cell((x + dx, y + dy))
            # register and continue if is what we are looking for
            if cell == searching_for:
                if distance + 1 < min_distance_found:
                    min_distance_found = distance + 1
                continue
            # continue if is a wall
            if cell in (Cell['WALL'], Cell['UNKNOWN']):
                continue
            # if not too far, add to unvisited
            if distance + 1 < min_distance_found:
                unvisited.append((distance + 1, x + dx, y + dy))

    return min_distance_found
