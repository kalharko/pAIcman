from queue import PriorityQueue
from back.board import Board
from back.cell import Cell
from utils.direction import Direction

#Optional, but required for graph testing
import matplotlib.pyplot as plt
import networkx as nx
import scipy.sparse

class Dijkstra:

    graph = {}
    distances = {}

    def __init__(self, board: Board):
        assert isinstance(board, Board)

        self.board = board

    #Convert board to graph with each entry representing a cell and its neighbours
    def board_to_graph(self):
        graph = {}
        width, height = self.board.get_size()

        for x in range(width):
            for y in range(height):
                current_position = (x, y)
                current_cell = self.board.get_cell(current_position)
                
                if current_cell != (1 or 0):#current_cell.is_movable():
                    neighbors = self.board.get_cell_neighbors(current_position)
                    graph[current_position] = []

                    for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, -1)):
                        neighbor_position = (current_position[0] + dx, current_position[1] + dy)
                        if current_position[0] + dx>=0 and current_position[0] + dx < width and current_position[1] + dy >= 0 and current_position[1] + dy < height:
                            neighbor_cell = self.board.get_cell(neighbor_position)
                            print(neighbor_cell,neighbor_position)
                            if neighbor_cell not in [Cell.WALL, Cell.EMPTY, Cell.UNKNOWN]:
                                graph[current_position].append(neighbor_position)  # Assuming the weight is 1 for now
                                
        return graph

    #Plot a graph of the cells and their relations, 
    #moved from NetworkX to a plot for readability as NetworkX is too busy
    def plot_graph(self, graph): #plot using matplotlib
        x_coords = []
        y_coords = []
        for case in graph: #Add case to coordinates
            x_coords.append(case[0])
            y_coords.append(case[1])
        #show links between cells
        for case in graph:
            for neighbor in graph[case]:
                plt.plot([case[0], neighbor[0]], [case[1], neighbor[1]], 'b-')
        plt.show()

    #Returns cell neighbours
    def get_neighbors(self, graph, cell):
        print(graph[cell])
        return graph[cell]

    #Uses distance to return a path, 
    #go from the end to get closer cells and eventually the start node, 
    #then reverse the obtained path.
    def find_shortest_path(self, graph, distances, start, end):
        shortest_path = []
        current_vertex = end

        #while current_vertex != start:
        for _ in range (distances[end]):
            shortest_path.append(current_vertex)
            neighbors = graph[current_vertex]

            # Find the neighbor with the minimum distance
            min_neighbor = min(neighbors, key=lambda neighbor: distances[neighbor])

            current_vertex = min_neighbor

        shortest_path.append(start)
        shortest_path.reverse()
        return shortest_path

    #Dijkstra Algorithm to determine distance from starting cell.
    #Needs to be tested further as the board tested was behaving strangely
    def dijkstra_algorithm(self, graph, start, end):
        # Initialize distances dictionary with infinity for all nodes except start
        distances = {vertex: float('infinity') for vertex in graph}
        distances[start] = 0
        distance = 1
        
        # Priority queue to keep track of cells with their distances
        priority_queue = PriorityQueue()
        priority_queue.put((0, start))

        while not priority_queue.empty():
            current_distance, current_vertex = priority_queue.get()
            # Ignore if we already found a shorter path to current_vertex
            if current_distance > distances[current_vertex]:
                continue

            for neighbor in graph[current_vertex]:
                new_distance = distances[current_vertex] + distance

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    priority_queue.put((new_distance, neighbor))
        return distances

    #Probably not useful as getting the distance should be done from the distance structure directly
    #Rather than causing an additional call to the djikstra method, which is costly.
    def get_distance(self, start_position: tuple[int, int], end_position: tuple[int, int]):
        graph = self.board_to_graph()
        distances = self.dijkstra_algorithm(graph, start_position)
        return distances[end_position]

    #Main Method to be used.
    def apply_dijkstra(self, start_position: tuple[int, int], end_position: tuple[int, int]):
        graph = self.board_to_graph()
        self.board.plot_board()

        distances = self.dijkstra_algorithm(graph, start_position, end_position)
        print(distances[end_position])
        shortest_path = self.find_shortest_path(graph, distances, start_position, end_position)
        self.plot_graph(graph)
        return distances, shortest_path
