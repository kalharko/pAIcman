# import pickle
import time

from back.board import Board
from back.cell import Cell
from algorithms.a_star import AStar
from back.pacman_game import PacmanGame


def pre_compute_board_distances(board: Board) -> dict[tuple[int, int]: dict[tuple[int, int]: int]]:
    """Precompute the distance matrix of all the non wall coordinates in a map. Saves it as a pickle file.

    :param path: path to the map file for wich precomputing is necessary
    :type path: str
    """
    assert isinstance(board, Board)

    print("\nPrecomputing the board's distance matrix")
    # find all positions to include in the matrix
    width, height = board.get_size()
    positions = []
    for y in range(height):
        for x in range(width):
            if board.get_cell((x, y)) == Cell['WALL']:
                pass
            else:
                positions.append((x, y))

    # initialize a star
    astar = AStar()
    astar.load_board(board)

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

    print('\nPrecomputing done, normal')
