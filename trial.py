import pygame
import sys
import heapq
import random

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
    queue = [start]
    visited = set()

    while queue:
        current = queue.pop(0)
        visited.add(current)

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                queue.append(neighbor)
                came_from[neighbor] = current

    return None

def depth_first_search(grid, start, goal):
    stack = [start]
    visited = set()

    while stack:
        current = stack.pop()
        visited.add(current)

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                stack.append(neighbor)
                came_from[neighbor] = current

    return None

def greedy_best_first_search(grid, start, goal):
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

def generate_obstacles(grid):
    obstacles = []
    for _ in range(50):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if grid[x][y] == 0:
            obstacles.append((x, y))
            grid[x][y] = 1
    return obstacles

# Initialize the game
pygame.init()
screen = pygame.display.set_mode((GRID_SIZE * GRID_WIDTH, GRID_SIZE * GRID_HEIGHT))
pygame.display.set_caption("Search Algorithm Demo")

grid = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
start = Node(2, 2)
goal = Node(17, 12)

# Create obstacles
obstacles = generate_obstacles(grid)

# Find the path using search algorithms
came_from = {}
for algo in [astar_search, breadth_first_search, depth_first_search, greedy_best_first_search]:
    path = algo(grid, start, goal)
    for node in path:
        came_from[node] = None

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

    # Draw the obstacles
    for x, y in obstacles:
        pygame.draw.rect(screen, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the path
    for node in came_from:
        if came_from[node]:
            x, y = node.x, node.y
            pygame.draw.rect(screen, RED, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()

pygame.quit()
