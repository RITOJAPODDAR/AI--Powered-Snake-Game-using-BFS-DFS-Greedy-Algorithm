import sys
import pygame
import math
from queue import PriorityQueue

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualization")

# Define node and grid constants
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Define node states
EMPTY = 0
WALL = 1
START = 2
END = 3
OPEN = 4
CLOSED = 5
PATH = 6

# Create grid
grid = [[EMPTY for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Define start and end positions
start = (5, 5)
end = (GRID_WIDTH - 6, GRID_HEIGHT - 6)

# Initialize Pygame clock
clock = pygame.time.Clock()

# Define fonts
font = pygame.font.Font(None, 36)

# Define heuristic function (Manhattan distance)
def heuristic(node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    return abs(x1 - x2) + abs(y1 - y2)

# Define A* search
def astar_search():
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start, end)

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]

        if current == end:
            reconstruct_path(came_from, end)
            return True

        for neighbor in get_neighbors(current):
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, end)
                if neighbor not in [item[1] for item in open_set.queue]:
                    open_set.put((f_score[neighbor], neighbor))
                    grid[neighbor[1]][neighbor[0]] = OPEN

        draw()

        if current != start:
            grid[current[1]][current[0]] = CLOSED

    return False

# Define neighbor retrieval
def get_neighbors(node):
    neighbors = []
    x, y = node
    if x > 0 and grid[y][x - 1] != WALL:
        neighbors.append((x - 1, y))
    if x < GRID_WIDTH - 1 and grid[y][x + 1] != WALL:
        neighbors.append((x + 1, y))
    if y > 0 and grid[y - 1][x] != WALL:
        neighbors.append((x, y - 1))
    if y < GRID_HEIGHT - 1 and grid[y + 1][x] != WALL:
        neighbors.append((x, y + 1))
    return neighbors

# Define path reconstruction
def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]
        if current != start:
            grid[current[1]][current[0]] = PATH

# Define grid drawing
def draw():
    win.fill(WHITE)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == WALL:
                pygame.draw.rect(win, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif grid[y][x] == START:
                pygame.draw.rect(win, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif grid[y][x] == END:
                pygame.draw.rect(win, RED, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif grid[y][x] == CLOSED:
                pygame.draw.rect(win, (200, 200, 200), (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif grid[y][x] == OPEN:
                pygame.draw.rect(win, (0, 255, 0), (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(win, BLACK, (0, y * GRID_SIZE), (WIDTH, y * GRID_SIZE))
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(win, BLACK, (x * GRID_SIZE, 0), (x * GRID_SIZE, HEIGHT))

    pygame.display.update()

# Initialize grid
for y in range(GRID_HEIGHT):
    for x in range(GRID_WIDTH):
        if (x, y) == start:
            grid[y][x] = START
        elif (x, y) == end:
            grid[y][x] = END
        elif x == 0 or x == GRID_WIDTH - 1 or y == 0 or y == GRID_HEIGHT - 1 or (x % 3 == 0 and y % 3 == 0):
            grid[y][x] = WALL

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if astar_search():
                    print("Path found!")

    draw()

    pygame.display.update()

# Main loop (cont.)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    clock.tick(60)

pygame.quit()
