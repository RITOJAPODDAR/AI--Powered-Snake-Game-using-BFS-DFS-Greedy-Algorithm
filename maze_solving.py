from collections import deque
import pygame
import heapq

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define grid parameters
GRID_SIZE = 40
GRID_WIDTH = 15
GRID_HEIGHT = 10

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

# Implement the A* search algorithm
def astar_search(grid, start, goal):
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {(node.x, node.y): float('inf') for row in grid for node in row}
    g_score[(start.x, start.y)] = 0

    while open_list:
        _, current = heapq.heappop(open_list)

        if (current.x, current.y) == (goal.x, goal.y):
            path = []
            while (current.x, current.y) in came_from:
                path.append(current)
                current = came_from[(current.x, current.y)]
            return path

        closed_list.add((current.x, current.y))

        for neighbor in get_neighbors(grid, current):
            neighbor_x, neighbor_y = neighbor.x, neighbor.y
            if (neighbor_x, neighbor_y) in closed_list:
                continue

            tentative_g_score = g_score[(current.x, current.y)] + 1
            if tentative_g_score < g_score[(neighbor_x, neighbor_y)]:
                came_from[(neighbor_x, neighbor_y)] = current
                g_score[(neighbor_x, neighbor_y)] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score, neighbor))

    return None
def bfs_search(grid, start, goal):
    visited = set()
    queue = deque()
    queue.append(start)

    while queue:
        current = queue.popleft()

        if current == goal:
            path = []
            while current.parent is not None:
                path.append(current)
                current = current.parent
            path.append(start)  # Add the start node
            return path[::-1]

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                neighbor.parent = current
                queue.append(neighbor)

    return None


def dfs_search(grid, current, goal, visited):
    if (current.x, current.y) == (goal.x, goal.y):
        return [current]

    visited[current.x][current.y] = True

    for neighbor in get_neighbors(grid, current):
        neighbor_x, neighbor_y = neighbor.x, neighbor.y
        if not visited[neighbor_x][neighbor_y] and grid[neighbor_x][neighbor_y] == 0:
            path = dfs_search(grid, neighbor, goal, visited)
            if path:
                return [current] + path

    return None

def greedy_best_first_search(grid, start, goal):
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, goal)  # Start with the goal as the initial node
    came_from = {}

    while open_list:
        current = heapq.heappop(open_list)

        if (current.x, current.y) == (start.x, start.y):
            path = []
            while (current.x, current.y) in came_from:
                path.append(current)
                current = came_from[(current.x, current.y)]
            return path

        closed_list.add((current.x, current.y))

        for neighbor in get_neighbors(grid, current):
            neighbor_x, neighbor_y = neighbor.x, neighbor.y
            if (neighbor_x, neighbor_y) in closed_list:
                continue

            came_from[(neighbor_x, neighbor_y)] = current
            heapq.heappush(open_list, neighbor)

    return None

def iterative_deepening_search(grid, start, goal, max_depth):
    for depth in range(max_depth):
        result = depth_limited_search(grid, start, goal, depth)
        if result is not None:
            return result

def depth_limited_search(grid, start, goal, depth):
    if depth == 0:
        if (start.x, start.y) == (goal.x, goal.y):
            return [start]
        else:
            return None

    if (start.x, start.y) == (goal.x, goal.y):
        return [start]

    for neighbor in get_neighbors(grid, start):
        result = depth_limited_search(grid, neighbor, goal, depth - 1)
        if result is not None:
            return [start] + result

# Define heuristic function for A* search
def heuristic(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)

# Implement get_neighbors function
def get_neighbors(grid, node):
    neighbors = []
    # Define how neighbors are obtained based on game logic
    # For example:
    x, y = node.x, node.y
    if x > 0 and not grid[x - 1][y]:
        neighbors.append(Node(x - 1, y))
    if x < GRID_WIDTH - 1 and not grid[x + 1][y]:
        neighbors.append(Node(x + 1, y))
    if y > 0 and not grid[x][y - 1]:
        neighbors.append(Node(x, y - 1))
    if y < GRID_HEIGHT - 1 and not grid[x][y + 1]:
        neighbors.append(Node(x, y + 1))
    return neighbors

# Initialize the game window
screen = pygame.display.set_mode((GRID_SIZE * GRID_WIDTH, GRID_SIZE * GRID_HEIGHT))
pygame.display.set_caption("A* Search Maze Solver")

# Create the grid with obstacles, start, and goal
grid = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
start = Node(1, 1)
goal = Node(13, 8)

# Place obstacles in the grid (customize this as needed)
# For example, block a specific grid cell:
# grid[5][5] = 1

# Find the path using A* search
path = astar_search(grid, start, goal)
visited = [[False for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

# Find the path using DFS
path = dfs_search(grid, start, goal, visited)

# Find the path using Greedy Best-First Search
path = greedy_best_first_search(grid, start, goal)

# Find the path using Iterative Deepening Search
max_depth = max(GRID_WIDTH, GRID_HEIGHT)
path = iterative_deepening_search(grid, start, goal, max_depth)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # Draw the grid
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            color = GREEN if grid[x][y] == 1 else WHITE
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the path
    if path:
        for node in path:
            pygame.draw.rect(screen, RED, (node.x * GRID_SIZE, node.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
