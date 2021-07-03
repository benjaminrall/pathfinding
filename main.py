from node import Node
import pygame
from pygame.locals import *

# Constants
SCALE_FACTOR = 24

SIZE = 15

SCREEN_WIDTH = 80 * SIZE
SCREEN_HEIGHT = 50 * SIZE

FRAMERATE = 60

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Maze Solver')


def create_grid(w, h, size):
    g = []
    for i in range(int(h / size)):
        row = []
        for j in range(int(w / size)):
            row.append(0)
        g.append(row)
    g[0][0] = 2
    g[len(g) - 1][len(g[0]) - 1] = 3
    return g


def find_path(start_pos, end_pos, number_grid):
    # create sets
    open_set = []
    closed_set = []
    node_grid = []
    # create node grid
    for i, row in enumerate(number_grid):
        x = []
        for j, col in enumerate(row):
            if col == 0:
                x.append(Node(j, i))
            else:
                x.append(1)
        node_grid.append(x)

    # get start pos
    sx, sy = start_pos
    ex, ey = end_pos
    # create start and end nodes and append to grid
    start = Node(sx, sy)
    end = Node(ex, ey)
    node_grid[sy][sx] = start
    node_grid[ey][ex] = end
    # create path and append starting node to open set
    path = []
    open_set.append(node_grid[sy][sx])

    # find neighbours
    for row in node_grid:
        for node in row:
            if node is not 1:
                node.find_neighbors(node_grid)

    # set start node t to 1
    start.t = 1

    # while examining nodes
    while len(open_set) > 0:
        winner = 0
        for i in range(len(open_set)):
            if open_set[i].f < open_set[winner].f:
                winner = i

        # current node being examined is node in open set closest to end
        current = open_set[winner]

        # if at the end
        if current == end:
            # reconstruct path
            path = []
            
            temp = current
            path.append(temp)
            while temp.previous is not None:
                path.append(temp.previous)
                temp = temp.previous
            break
        
        # add examined node to closed set
        closed_set.append(current)
        open_set.pop(winner)

        # for every neighbour in the previously examined node
        for neighbor in current.neighbors:
            # if it's not in the closed set (already been examined)
            if neighbor not in closed_set:
                # find distance to neighbour
                diff = abs(neighbor.x - current.x) + abs(neighbor.y - current.y)
                # add distance to travelling distance
                temp_g = current.g + diff
                # add to opens set if not already there
                if neighbor not in open_set:
                    open_set.append(neighbor)
                # set new shortest route if applicable
                elif temp_g < neighbor.g:
                    neighbor.g = temp_g
                # set previous node for neighbour
                neighbor.previous = current
                # work out distance to end point
                neighbor.h = abs(neighbor.x - end.x) + abs(neighbor.y - end.y)
                neighbor.h = ((neighbor.x - end.x) ** 2) + ((neighbor.y - end.y) ** 2)
                # work out f, which is distance travelled + distance to end point
                neighbor.f = neighbor.g + neighbor.h
            else:
                diff = abs(neighbor.x - current.x) + abs(neighbor.y - current.y)
                temp_g = current.g + diff
                if temp_g < neighbor.g:
                    neighbor.g = temp_g
                    neighbor.previous = current
                neighbor.f = neighbor.g + neighbor.h

        for node in open_set:
            if node is not end and node is not start:
                grid[node.y][node.x] = 4

        for node in closed_set:
            if node is not end and node is not start:
                grid[node.y][node.x] = 5

        SCREEN.fill((0, 0, 0))
        draw_grid(number_grid, SIZE, SCREEN)
        pygame.display.update()
    return path


def draw_grid(g, size, screen):
    for y in range(len(g)):
        for x in range(len(g[y])):
            if g[y][x] == 0:
                pygame.draw.rect(screen, (255, 255, 255), (x * size, y * size, size, size))
                pygame.draw.rect(screen, (0, 0, 0), (x * size, y * size, size, size), 1)
            elif g[y][x] == 1:
                pygame.draw.rect(screen, (0, 0, 0), (x * size, y * size, size, size))
            elif g[y][x] == 2:
                if started:
                    pygame.draw.rect(screen, (255, 255, 0), (x * size, y * size, size, size))
                    pygame.draw.rect(screen, (0, 0, 0), (x * size, y * size, size, size), 1)
                else:
                    pygame.draw.rect(screen, (0, 255, 0), (x * size, y * size, size, size))
                    pygame.draw.rect(screen, (0, 0, 0), (x * size, y * size, size, size), 1)
            elif g[y][x] == 3:
                if started:
                    pygame.draw.rect(screen, (0, 255, 255), (x * size, y * size, size, size))
                    pygame.draw.rect(screen, (0, 0, 0), (x * size, y * size, size, size), 1)
                else:
                    pygame.draw.rect(screen, (255, 0, 0), (x * size, y * size, size, size))
                    pygame.draw.rect(screen, (0, 0, 0), (x * size, y * size, size, size), 1)
            elif g[y][x] == 4:
                pygame.draw.rect(screen, (0, 255, 0), (x * size, y * size, size, size))
                pygame.draw.rect(screen, (0, 0, 0), (x * size, y * size, size, size), 1)
            elif g[y][x] == 5:
                pygame.draw.rect(screen, (255, 0, 0), (x * size, y * size, size, size))
                pygame.draw.rect(screen, (0, 0, 0), (x * size, y * size, size, size), 1)
            elif g[y][x] == 6:
                pygame.draw.rect(screen, (255, 0, 255), (x * size, y * size, size, size))
                pygame.draw.rect(screen, (0, 0, 0), (x * size, y * size, size, size), 1)

def update_grid(pos, num):
    x = pos[0] // SIZE
    y = pos[1] // SIZE
    if grid[y][x] == 0 or grid[y][x] == 1:
        if num == 2:
            for row in grid:
                for i in range(len(row)):
                    if row[i] == 2:
                        row[i] = 0
        elif num == 3:
            for row in grid:
                for i in range(len(row)):
                    if row[i] == 3:
                        row[i] = 0
        grid[y][x] = num


clock = pygame.time.Clock()

started = False
found_path = False
left_down = False
right_down = False

SCREEN.fill((255, 255, 255))
grid = create_grid(SCREEN_WIDTH, SCREEN_HEIGHT, SIZE)
draw_grid(grid, SIZE, SCREEN)
pygame.display.update()

if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN and not started:
                if event.button == 1:
                    left_down = True
                elif event.button == 3:
                    right_down = True
                elif event.button == 4:
                    update_grid(pygame.mouse.get_pos(), 2)
                elif event.button == 5:
                    update_grid(pygame.mouse.get_pos(), 3)
            elif event.type == MOUSEBUTTONUP and not started:
                if event.button == 1:
                    left_down = False
                elif event.button == 3:
                    right_down = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if not started:
                        started = True
                    else:
                        started = False
                        found_path = False
                        grid = create_grid(SCREEN_WIDTH, SCREEN_HEIGHT, SIZE)

        if not started:
            if left_down:
                update_grid(pygame.mouse.get_pos(), 1)
            elif right_down:
                update_grid(pygame.mouse.get_pos(), 0)
        elif not found_path:
            for j in range(len(grid)):
                for i in range(len(grid[j])):
                    if grid[j][i] == 2:
                        start = (i, j)
            for j in range(len(grid)):
                for i in range(len(grid[j])):
                    if grid[j][i] == 3:
                        end = (i, j)
            path = find_path(start, end, grid)
            for node in path:
                grid[node.y][node.x] = 6
            found_path = True

        SCREEN.fill((255, 255, 255))
        draw_grid(grid, SIZE, SCREEN)
        pygame.display.update()
