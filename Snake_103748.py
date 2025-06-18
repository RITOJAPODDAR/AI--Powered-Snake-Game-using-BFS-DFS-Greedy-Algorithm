import pygame
import random
import heapq
import sys

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
SNAKE_SPEED = 3

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Load the food image
food_image = pygame.image.load('food.png')  # Make sure to place your food image file in the same directory as your script.

# Snake and Food
snake = [(5, 5)]
food = (15, 15)

# Obstacle Positions
# Define the positions of obstacles in a predetermined pattern
obstacle_positions = [
    (9, 7),
    (10, 8),
    (11, 9),
    (12, 10),
    (13, 11),
    (5, 8),
    (5, 9),
    (5, 10),
    (5, 11),
    (5, 12),
    (5, 13),
    (5, 14),
    (6, 14),
    (7, 14),
    (8, 14),
    (9, 14),
    (10, 14),
    (11, 14),
    (12, 14),
    # Add more obstacle positions as needed
]

def heuristic(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)  # Manhattan distance

# Define a function for Greedy Best First Search
def greedy_best_first_search(start, goal, obstacles):
    # Convert start, goal, and obstacle positions to tuples
    start = tuple(start)
    goal = tuple(goal)
    obstacles = set(tuple(pos) for pos in obstacles)

    open_list = []
    closed_list = set()
    came_from = {}

    def greedy_heuristic(pos):
        return heuristic(pos, goal)

    open_list.append((greedy_heuristic(start), start))

    while open_list:
        open_list.sort()  # Sort the open list based on the heuristic value
        current = open_list.pop(0)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        closed_list.add(current)

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)

            if neighbor in closed_list or neighbor in obstacles:
                continue

            if neighbor not in [n[1] for n in open_list]:
                came_from[neighbor] = current
                open_list.append((greedy_heuristic(neighbor), neighbor))

    return None  # No path found


# Define a function for DFS search
def a_star_search(start, goal, obstacles):
    # Convert start, goal, and obstacle positions to tuples
    start = tuple(start)
    goal = tuple(goal)
    obstacles = set(tuple(pos) for pos in obstacles)

    open_list = []
    closed_list = set()
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    heapq.heappush(open_list, (f_score[start], start))

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        closed_list.add(current)

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)

            if neighbor in closed_list or neighbor in obstacles:
                continue

            tentative_g_score = g_score[current] + 1

            if neighbor not in [n[1] for n in open_list] or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None  # No path found

# Define a function for DFS search
def dfs_search(start, goal, obstacles):
    stack = [(start, [])]  # Initialize a stack with the start position and an empty path
    visited = set()  # Keep track of visited positions to avoid loops

    while stack:
        current_position, path = stack.pop()  # Get the current position and path

        if current_position == goal:
            # Found a path to the goal
            return path
        
        visited.add(current_position)

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current_position[0] + dx, current_position[1] + dy)

            if (
                neighbor not in visited and
                neighbor not in obstacles and
                0 <= neighbor[0] < GRID_WIDTH and 0 <= neighbor[1] < GRID_HEIGHT
            ):
                # Add the neighbor to the stack with the updated path
                stack.append((neighbor, path + [current_position]))

    # If no path is found, return an empty path
    return []

# Define a function for BFS search
def bfs_search(start, goal, obstacles):
    queue = [(start, [])]  # Initialize a queue with the start position and an empty path
    visited = set()  # Keep track of visited positions to avoid loops

    while queue:
        current_position, path = queue.pop(0)  # Get the current position and path

        if current_position == goal:
            # Found a path to the goal
            return path

        visited.add(current_position)

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current_position[0] + dx, current_position[1] + dy)

            if (
                neighbor not in visited and
                neighbor not in obstacles and
                0 <= neighbor[0] < GRID_WIDTH and 0 <= neighbor[1] < GRID_HEIGHT
            ):
                # Add the neighbor to the queue with the updated path
                queue.append((neighbor, path + [current_position]))

    # If no path is found, return an empty path
    return []

# Main game loop
running = True
clock = pygame.time.Clock()

# Set up boundaries around the screen
boundary = [(x, 0) for x in range(GRID_WIDTH)] + [(x, GRID_HEIGHT - 1) for x in range(GRID_WIDTH)] + \
           [(0, y) for y in range(1, GRID_HEIGHT - 1)] + [(GRID_WIDTH - 1, y) for y in range(1, GRID_HEIGHT - 1)]

def check_collision(new_head):
    if new_head in snake[1:] or new_head in boundary:
        return True
    return False

def generate_random_food(obstacle_positions):
    while True:
        food = (random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2))
        if food not in obstacle_positions:
            return food
        
# Initialize the food position
food = generate_random_food(obstacle_positions)

# eaten_food_count = False  # Variable to track if the snake has eaten the food
eaten_food_count = 0  # Variable to track how many times the snake has eaten food
path = []  # Initialize a list to store the path coordinates
total_path_length = 0  # Initialize total path length

# Initialize a variable to track the type of search algorithm
search_algorithm = "A*"  # Start with A* search

# Add a new variable for the second food
food2 = None

# Add a new variable for the third food
food3 = None

while running and eaten_food_count < 3:  # Run the game until the snake eats food three times
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # # Snake Movement (manual control)
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_UP] and (len(snake) < 2 or (snake[0][0], snake[0][1] - 1) != snake[1]):
    #     direction = (0, -1)
    # elif keys[pygame.K_DOWN] and (len(snake) < 2 or (snake[0][0], snake[0][1] + 1) != snake[1]):
    #     direction = (0, 1)
    # elif keys[pygame.K_LEFT] and (len(snake) < 2 or (snake[0][0] - 1, snake[0][1]) != snake[1]):
    #     direction = (-1, 0)
    # elif keys[pygame.K_RIGHT] and (len(snake) < 2 or (snake[0][0] + 1, snake[0][1]) != snake[1]):
    #     direction = (1, 0)

    # Check if the snake has eaten both foods to end the game
    if eaten_food_count >= 3:
        running = False

    if food2 is None and eaten_food_count == 1:
        # Generate the second food after eating the first
        food2 = generate_random_food(obstacle_positions)

    if food3 is None and eaten_food_count == 2:
        # Generate the second food after eating the first
        food3 = generate_random_food(obstacle_positions)

    if eaten_food_count == 0:
        if search_algorithm == "A*":
            direction = a_star_search(snake[0], food, obstacle_positions)
        elif search_algorithm == "DFS":
            direction = dfs_search(snake[0], food2, obstacle_positions)
        elif search_algorithm == "BFS":
            direction = bfs_search(snake[0], food3, obstacle_positions)
        else:
            direction = greedy_best_first_search(snake[0], food, obstacle_positions)
    elif eaten_food_count == 1:
        if search_algorithm == "A*":
            direction = a_star_search(snake[0], food, obstacle_positions)
        elif search_algorithm == "DFS":
            direction = dfs_search(snake[0], food2, obstacle_positions)
        elif search_algorithm == "BFS":
            direction = bfs_search(snake[0], food3, obstacle_positions)
        else:
            direction = greedy_best_first_search(snake[0], food2, obstacle_positions)
    elif eaten_food_count == 2:
        if search_algorithm == "A*":
            direction = a_star_search(snake[0], food, obstacle_positions)
        elif search_algorithm == "DFS":
            direction = dfs_search(snake[0], food2, obstacle_positions)
        elif search_algorithm == "BFS":
            direction = bfs_search(snake[0], food3, obstacle_positions)
        else:
            direction = greedy_best_first_search(snake[0], food3, obstacle_positions)
    
    # Check if direction is not None
    if direction is not None:
        # if direction:  # Check if direction is not empty
        next_position = direction[0]
            
        dx, dy = next_position[0] - snake[0][0], next_position[1] - snake[0][1]  # Calculate the direction

        # Add the new head position to the path list
        path.append((snake[0][0] + dx, snake[0][1] + dy))

        # Calculate the length of the path list as the snake moves
        total_path_length = len(path)
        
        # Calculate the Manhattan distance between the snake's head and the food
        manhattan_distance = abs(snake[0][0] - food[0]) + abs(snake[0][1] - food[1])

        # Move snake
        new_head = (snake[0][0] + dx, snake[0][1] + dy)
        # new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if new_head == food:
            if not eaten_food_count:
                eaten_food_count += 1
                food = generate_random_food(obstacle_positions)  # Generate a new food position
            else:
                # Update the direction to move towards the second food
                direction = a_star_search(snake[0], food, obstacle_positions)
                # Optionally, you can also check if there's no possible path to the second food and handle that case.
        else:
            # If food is not eaten, continue moving the snake
            snake.pop()

        # Check for collision with obstacles
        if new_head in obstacle_positions:
            running = False

        if check_collision(new_head):
            running = False

        snake.insert(0, new_head)

    # Check if the snake's head has reached the first food
    if snake[0] == food:
        food = generate_random_food(obstacle_positions)  # Generate the next food position
        eaten_food_count += 1  # Increase the count of eaten food

        if eaten_food_count == 1:
            search_algorithm = "A*"  # Display A* algorithm info for the first food

    # Check if the snake's head has reached the second food
    if snake[0] == food2:
        food2 = generate_random_food(obstacle_positions)  # Generate the next food position
        eaten_food_count += 1  # Increase the count of eaten food

        if eaten_food_count == 2:
            search_algorithm = "DFS"  # Display DFS algorithm info for the second food

    # Check if the snake's head has reached the third food
    if snake[0] == food3:
        food3 = None  # Remove the third food
        eaten_food_count += 1  # Increase the count of eaten food    

    # Draw everything
    screen.fill(BLACK)

    # Draw obstacles
    for obs in obstacle_positions:
        pygame.draw.rect(screen, GREEN, (obs[0] * GRID_SIZE, obs[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    # Draw the head
    pygame.draw.rect(screen, RED, (snake[0][0] * GRID_SIZE, snake[0][1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the food image
    screen.blit(food_image, (food[0] * GRID_SIZE, food[1] * GRID_SIZE))

    # Draw the boundary
    for point in boundary:
        pygame.draw.rect(screen, GREEN, (point[0] * GRID_SIZE, point[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Display the information when approaching the first food
    if eaten_food_count == 0:
        # Calculate the Manhattan distance
        manhattan_distance = abs(snake[0][0] - food[0]) + abs(snake[0][1] - food[1])

        # Display A* algorithm info
        font = pygame.font.Font(None, 24)
        algorithm_info = font.render(f'   A* Algorithm', True, WHITE)
        screen.blit(algorithm_info, (10, 20))

        # Display Manhattan distance
        distance_text = font.render(f'   Manhattan Distance: {manhattan_distance}', True, WHITE)
        screen.blit(distance_text, (10, 40))

        # Display Total Path Length
        path_length_text = font.render(f'   Total Path Length: {total_path_length}', True, WHITE)
        screen.blit(path_length_text, (10, 60))
  
    # Display the information when approaching the second food
    if eaten_food_count == 1:
        # Calculate the Manhattan distance
        manhattan_distance = abs(snake[0][0] - food[0]) + abs(snake[0][1] - food[1])

        # Display DFS algorithm info
        font = pygame.font.Font(None, 24)
        algorithm_info = font.render(f'   DFS Algorithm', True, WHITE)
        screen.blit(algorithm_info, (10, 20))

        # Display Manhattan distance
        distance_text = font.render(f'   Manhattan Distance: {manhattan_distance}', True, WHITE)
        screen.blit(distance_text, (10, 40))

        # Display Total Path Length
        path_length_text = font.render(f'   Total Path Length: {total_path_length}', True, WHITE)
        screen.blit(path_length_text, (10, 60))
    
    # Display the information when approaching the third food
    if eaten_food_count == 2:
        # Calculate the Manhattan distance
        manhattan_distance = abs(snake[0][0] - food[0]) + abs(snake[0][1] - food[1])

        # Display BFS algorithm info
        font = pygame.font.Font(None, 24)
        algorithm_info = font.render(f'   BFS Algorithm', True, WHITE)
        screen.blit(algorithm_info, (10, 20))

        # Display Manhattan distance
        distance_text = font.render(f'   Manhattan Distance: {manhattan_distance}', True, WHITE)
        screen.blit(distance_text, (10, 40))

        # Display Total Path Length
        path_length_text = font.render(f'   Total Path Length: {total_path_length}', True, WHITE)
        screen.blit(path_length_text, (10, 60))

    
    
    pygame.display.flip()
    clock.tick(SNAKE_SPEED)

# "Game Over" message
font = pygame.font.Font(None, 36)
if eaten_food_count:
    game_over_text = font.render("      Game Over", True, RED)
else:
    game_over_text = font.render("      Game Over", True, RED)
screen.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 20))
pygame.display.flip()

# Keep the game running even after game over
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()