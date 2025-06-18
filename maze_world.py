import pygame
import random
import heapq

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define grid parameters
GRID_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 15

# Define classes
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

def heuristic(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)

def get_neighbors(grid, node):
    neighbors = []
    if node.x > 0 and not grid[node.x - 1][node.y]:
        neighbors.append(Node(node.x - 1, node.y))
    if node.x < GRID_WIDTH - 1 and not grid[node.x + 1][node.y]:
        neighbors.append(Node(node.x + 1, node.y))
    if node.y > 0 and not grid[node.x][node.y - 1]:
        neighbors.append(Node(node.x, node.y - 1))
    if node.y < GRID_HEIGHT - 1 and not grid[node.x][node.y + 1]:
        neighbors.append(Node(node.x, node.y + 1))
    return neighbors



def astar_search(grid, start, goal):
    open_list = []
    closed_list = []

    heapq.heappush(open_list, (0, start))
    came_from = {}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        closed_list.append(current)

        for neighbor in get_neighbors(grid, current):
            if neighbor in closed_list:
                continue
            tentative_g = current.g + 1

            if neighbor not in [n[1] for n in open_list] or tentative_g < neighbor.g:
                neighbor.g = tentative_g
                neighbor.h = heuristic(neighbor, goal)
                came_from[neighbor] = current
                heapq.heappush(open_list, (neighbor.g + neighbor.h, neighbor))

    return None




def breadth_first_search(grid, start, goal):
    # Implementation of BFS
    open_list = [start]
    came_from = {start: None}

    while open_list:
        current = open_list.pop(0)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(grid, current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                open_list.append(neighbor)

    return None


def depth_first_search(grid, start, goal):
    # Implementation of DFS

    stack = [start]
    visited = set()

    while stack:
        current = stack.pop()
        visited.add(current)

        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(start)
            return path[::-1]

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                neighbor.parent = current
                stack.append(neighbor)

def greedy_best_first_search(grid, start, goal):
    # Implementation of Greedy Best First search
    # ...
    open_list = []
    closed_list = []
    heapq.heappush(open_list, (heuristic(start, goal), start))
    came_from = {}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path

        closed_list.append(current)

        for neighbor in get_neighbors(grid, current):
            if neighbor in closed_list:
                continue

            if neighbor not in [n[1] for n in open_list]:
                heapq.heappush(open_list, (heuristic(neighbor, goal), neighbor))
                came_from[neighbor] = current

    return None


# Initialize the game
pygame.init()
screen = pygame.display.set_mode((GRID_SIZE * GRID_WIDTH, GRID_SIZE * GRID_HEIGHT))
pygame.display.set_caption("Maze World with Search Algorithms")

grid = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
start = Node(2, 2)
goal = Node(17, 12)

# Generate the maze
def generate_maze(grid):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if random.random() < 0.3:
                grid[x][y] = 1

generate_maze(grid)

# Find the path using search algorithms
path_astar = astar_search(grid, start, goal)
path_bfs = breadth_first_search(grid, start, goal)
path_dfs = depth_first_search(grid, start, goal)
path_greedy = greedy_best_first_search(grid, start, goal)

# ... (previous code)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # Draw the grid
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            color = GREEN if grid[x][y] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the path for each algorithm
    for path in [path_astar, path_bfs, path_dfs, path_greedy]:
        if path:
            for node in path:
                x, y = node.x, node.y
                pygame.draw.rect(screen, RED, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()
    pygame.time.delay(100)
# Properly quit pygame
pygame.quit()
