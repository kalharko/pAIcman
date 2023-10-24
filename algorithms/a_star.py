class AStar():
    def __init__(self, game_map, start_cell, goal_cell):
        self.game_map = game_map
        self.start_cell = start_cell
        self.goal_cell = goal_cell

    # f(n) = g(n) + h(n)
    # g(n) is the cost of the path from the start cell to the cell n
    # h(n) is a heuristic function that estimates the cost of the cheapest path from n to the goal cell

    # define the cost of an action
    def cost(self):
        pass

    # calculatre the distance with the Manhattan heuristic
    def manhattan(self, current_cell):
        # return abs(current_cell.x - self.goal_cell.x) + abs(current_cell.y - self.goal_cell.y)
        pass

    # calculate the distance with the Euclidean heuristic
    def euclidean(self, current_cell):
        # return math.sqrt((current_cell.x - self.goal_cell.x)**2 + (current_cell.y - self.goal_cell.y)**2)
        pass
