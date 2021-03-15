class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.t = 0
        self.neighbors = []
        self.previous = None

    def find_neighbors(self, node_grid):
        # set x,y
        x, y = self.x, self.y
        try:
            if self.t is not 1:
                for i in range(x + 1, len(node_grid[y])):
                    if node_grid[y][i] is not 1:
                        self.neighbors.append(node_grid[y][i])
                    break
                for i in range(y + 1, len(node_grid)):
                    if node_grid[i][x] is not 1:
                        self.neighbors.append(node_grid[i][x])
                    break
                for i in range(x - 1, - 1, - 1):
                    if node_grid[y][i] is not 1:
                        self.neighbors.append(node_grid[y][i])
                    break
                for i in range(y - 1, - 1, - 1):
                    if node_grid[i][x] is not 1:
                        self.neighbors.append(node_grid[i][x])
                    break
        except:
            pass
