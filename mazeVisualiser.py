import pygame, sys, random, heapq
from collections import deque

pygame.init()

width, height = 800, 800
cell_size = 26
cols = width // cell_size
rows = height // cell_size

white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
yellow, purple, orange = (255, 255, 0), (112, 1, 248), (255, 165, 0)
blue, green, red = (0, 0, 255), (0, 255, 0), (255, 0, 0)

font = pygame.font.SysFont('segoeui', 24)
font1 = pygame.font.SysFont('segoeui', 20)
largeFont = pygame.font.SysFont('segoeui', 40)
titleFont = pygame.font.SysFont('segoeui', 60, bold=True)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Visualiser")
clock = pygame.time.Clock()

MAIN_MENU = "main"
INFO_SCREEN = "info"
COMPARE_GENERATION = "compare_gen"
COMPARE_SOLVING = "compare_solve"
RUN_SINGLE = "single"

current_screen = MAIN_MENU
run_action = None

predefined_maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,0,1],
    [1,0,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,1,0,1,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,1,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,1],
    [1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1],
    [1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

ROWS = len(predefined_maze)
COLS = len(predefined_maze[0])
start_pos = (1, 1)
end_pos = (COLS - 2, ROWS - 2)

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(x, y, maze):
    directions = [(1,0), (0,1), (-1,0), (0,-1)]
    result = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 0:
            result.append((nx, ny))
    return result

def draw_maze(maze, visited=None, path=None, current=None, label=""):
    screen.fill(black)
    for y in range(ROWS):
        for x in range(COLS):
            color = white if maze[y][x] == 0 else black
            if (x, y) == start_pos:
                color = green
            elif (x, y) == end_pos:
                color = red
            elif path and (x, y) in path:
                color = yellow
            elif visited and (x, y) in visited:
                color = purple
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size + 40, cell_size, cell_size))
    if label:
        label_text = font.render(label, True, orange)
        screen.blit(label_text, (25, 5))
    pygame.display.flip()

def dfs_solve(maze):
    start_time = pygame.time.get_ticks()
    stack = [start_pos]
    visited = set()
    parent = {}
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        if current == end_pos:
            break
        for neighbor in get_neighbors(*current, maze):
            if neighbor not in visited:
                stack.append(neighbor)
                parent.setdefault(neighbor, current)
        draw_maze(maze, visited, None, current, "DFS")
        pygame.time.delay(10)
    path = []
    while current in parent:
        path.append(current)
        current = parent[current]
    path.append(start_pos)
    path.reverse()
    runtime = pygame.time.get_ticks() - start_time
    draw_maze(maze, path=path, label="DFS Final Path")
    pygame.time.delay(1000)
    return len(path), len(visited), runtime

def bfs_solve(maze):
    start_time = pygame.time.get_ticks()
    queue = deque([start_pos])
    visited = set([start_pos])
    parent = {}
    while queue:
        current = queue.popleft()
        if current == end_pos:
            break
        for neighbor in get_neighbors(*current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
        draw_maze(maze, visited, None, current, "BFS")
        pygame.time.delay(10)
    path = []
    while current in parent:
        path.append(current)
        current = parent[current]
    path.append(start_pos)
    path.reverse()
    runtime = pygame.time.get_ticks() - start_time
    draw_maze(maze, path=path, label="BFS Final Path")
    pygame.time.delay(1000)
    return len(path), len(visited), runtime

def a_star_solve(maze):
    start_time = pygame.time.get_ticks()
    open_set = [(0, start_pos)]
    g_score = {start_pos: 0}
    f_score = {start_pos: manhattan(start_pos, end_pos)}
    came_from = {}
    visited = set()
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end_pos:
            break
        visited.add(current)
        for neighbor in get_neighbors(*current, maze):
            tentative = g_score[current] + 1
            if tentative < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative
                f_score[neighbor] = tentative + manhattan(neighbor, end_pos)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
        draw_maze(maze, visited, None, current, "A* Algorithm")
        pygame.time.delay(10)
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start_pos)
    path.reverse()
    runtime = pygame.time.get_ticks() - start_time
    draw_maze(maze, path=path, label="A* Final Path")
    pygame.time.delay(1000)
    return len(path), len(visited), runtime

def dijkstra_solve(maze):
    start_time = pygame.time.get_ticks()
    dist = {start_pos: 0}
    parent = {}
    visited = set()
    queue = [(0, start_pos)]
    while queue:
        _, current = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        if current == end_pos:
            break
        for neighbor in get_neighbors(*current, maze):
            new_dist = dist[current] + 1
            if new_dist < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_dist
                parent[neighbor] = current
                heapq.heappush(queue, (new_dist, neighbor))
        draw_maze(maze, visited, None, current, "Dijkstra's Algorithm")
        pygame.time.delay(10)
    path = []
    while current in parent:
        path.append(current)
        current = parent[current]
    path.append(start_pos)
    path.reverse()
    runtime = pygame.time.get_ticks() - start_time
    draw_maze(maze, path=path, label="Dijkstra Final Path")
    pygame.time.delay(1000)
    return len(path), len(visited), runtime

def generate_prims(visualize=True):
    global generation_maze
    generation_maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    frontier = [(1, 1)]
    generation_maze[1][1] = 0
    while frontier:
        x, y = random.choice(frontier)
        frontier.remove((x, y))
        neighbors = [(x+dx*2, y+dy*2) for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]]
        random.shuffle(neighbors)
        for nx, ny in neighbors:
            if 1 <= nx < COLS-1 and 1 <= ny < ROWS-1 and generation_maze[ny][nx] == 1:
                mx, my = (x+nx)//2, (y+ny)//2
                generation_maze[ny][nx] = 0
                generation_maze[my][mx] = 0
                frontier.append((nx, ny))
        if visualize:
            draw_maze(generation_maze, label="Prim's Algorithm")
            pygame.time.delay(10)
    return generation_maze


def generate_kruskals(visualize=True):
    global generation_maze
    generation_maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    sets = {}
    edges = []
    cell_id = 0
    for y in range(1, ROWS, 2):
        for x in range(1, COLS, 2):
            sets[(x, y)] = cell_id
            cell_id += 1
            generation_maze[y][x] = 0
            for dx, dy in [(2, 0), (0, 2)]:
                nx, ny = x + dx, y + dy
                if 1 <= nx < COLS - 1 and 1 <= ny < ROWS - 1:
                    edges.append(((x, y), (nx, ny)))
    random.shuffle(edges)
    for (x1, y1), (x2, y2) in edges:
        if sets[(x1, y1)] != sets[(x2, y2)]:
            mx, my = (x1+x2)//2, (y1+y2)//2
            generation_maze[my][mx] = 0
            old_id, new_id = sets[(x2, y2)], sets[(x1, y1)]
            for cell in sets:
                if sets[cell] == old_id:
                    sets[cell] = new_id
        if visualize:
            draw_maze(generation_maze, label="Kruskal's Algorithm")
            pygame.time.delay(10)
    return generation_maze

def generate_recursive_backtracking(visualize=True):
    global generation_maze
    generation_maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    stack = [(1, 1)]
    generation_maze[1][1] = 0
    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            nx, ny = x+dx, y+dy
            if 1 <= nx < COLS-1 and 1 <= ny < ROWS-1 and generation_maze[ny][nx] == 1:
                neighbors.append((nx, ny))
        if neighbors:
            next_cell = random.choice(neighbors)
            mx, my = (x+next_cell[0])//2, (y+next_cell[1])//2
            generation_maze[my][mx] = 0
            generation_maze[next_cell[1]][next_cell[0]] = 0
            stack.append(next_cell)
        else:
            stack.pop()
        if visualize:
            draw_maze(generation_maze, label="Recursive Backtracking")
            pygame.time.delay(10)
    return generation_maze

def draw_instructions():
    screen.fill(black)
    title = titleFont.render("Maze Visualiser", True, orange)
    screen.blit(title, (50, 50))
    instructions = [
        "Press 'I' for Info",
        "Press 'C' to Compare Solving",
        "Press 'V' to Compare Maze Generators",
        "Press 'D' for DFS",
        "Press 'B' for BFS",
        "Press 'A' for A* Algorithm",
        "Press 'S' for Dijkstra's Algorithm",
        "Press 'P' for Prim's Algorithm",
        "Press 'K' for Kruskal's Algorithm",
        "Press 'R' for Recursive Backtracking",
        "Press ESC to Exit"
    ]
    y = 150
    for line in instructions:
        screen.blit(font.render(line, True, white), (50, y))
        y += 40
    pygame.display.flip()

def draw_info_screen():
    screen.fill(black)
    info_title = titleFont.render("Algorithm Information", True, white)
    screen.blit(info_title, (30, 30))

    info_text = [
        ("DFS", "O(V + E)", "Explores deeply before backtracking"),
        ("BFS", "O(V + E)", "Finds shortest path exploring level by level"),
        ("Dijkstra", "O((V + E) log V)", "Shortest path in weighted graphs without heuristics"),
        ("A*", "O((V + E) log V)", "Shortest path using cost and heuristic"),
        ("Recursive Backtracking", "O(V + E)", "Explores paths by trying and backtracking"),
        ("Prim's", "O((E) log V)", "Grows the tree from a starting vertex"),
        ("Kruskal's", "O((E) log E)", "Connects the smallest edges without forming cycles"),
    ]
    y = 120
    for name, complexity, desc in info_text:
        text = f"{name:<15} | Time: {complexity:<10} | {desc}"
        screen.blit(font1.render(text, True, orange), (30, y))
        y += 40
    pygame.display.flip()

def draw_solver_results(results_dict):
    screen.fill(black)
    title = titleFont.render("Solving Algorithms Results", True, white)
    screen.blit(title, (50, 10))

    headers = ["Algorithm", "Path Length", "Visited Cells", "Time (ms)"]
    x_positions = [50, 250, 450, 650]

    for i, header in enumerate(headers):
        screen.blit(largeFont.render(header, True, orange), (x_positions[i], 80))

    y = 130
    for name, (path_len, visited, runtime) in results_dict.items():
        values = [name, str(path_len), str(visited), f"{runtime:.2f}"]
        for i, val in enumerate(values):
            screen.blit(font.render(val, True, white), (x_positions[i], y))
        y += 40

    prompt = font.render("Press any key to return to menu...", True, orange)
    screen.blit(prompt, (width // 2 - prompt.get_width() // 2, y + 30))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def draw_generator_results(results_dict):
    screen.fill(black)
    title = titleFont.render("Maze Generation Comparison", True, white)
    screen.blit(title, (50, 10))

    headers = ["Algorithm", "Time (ms)"]
    x_positions = [100, 400]

    for i, header in enumerate(headers):
        screen.blit(largeFont.render(header, True, orange), (x_positions[i], 80))

    y = 130
    for name, runtime in results_dict.items():
        values = [name, f"{runtime:.2f}"]
        for i, val in enumerate(values):
            screen.blit(font.render(val, True, white), (x_positions[i], y))
        y += 40

    prompt = font.render("Press any key to return to menu...", True, orange)
    screen.blit(prompt, (width // 2 - prompt.get_width() // 2, y + 30))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def compare_solvers():
    results = {}
    solvers = [
        ("DFS", dfs_solve),
        ("BFS", bfs_solve),
        ("A*", a_star_solve),
        ("Dijkstra's", dijkstra_solve)
    ]
    for name, solver in solvers:
        maze_copy = [row[:] for row in predefined_maze]
        results[name] = solver(maze_copy)
        pygame.time.delay(300)
    draw_solver_results(results)

def compare_generators():
    results = {}
    algorithms = [
        ("Recursive Backtracking", generate_recursive_backtracking),
        ("Prim's Algorithm", generate_prims),
        ("Kruskal's Algorithm", generate_kruskals)
    ]
    for name, algo in algorithms:
        start = pygame.time.get_ticks()
        maze = algo(visualize=True)  
        duration = pygame.time.get_ticks() - start
        results[name] = duration
        pygame.time.delay(500)

    draw_generator_results(results)

while True:
    clock.tick(60)

    if current_screen == MAIN_MENU:
        draw_instructions()
    elif current_screen == INFO_SCREEN:
        draw_info_screen()
    elif current_screen == COMPARE_SOLVING:
        compare_solvers()
        current_screen = MAIN_MENU
    elif current_screen == COMPARE_GENERATION:
        compare_generators()
        current_screen = MAIN_MENU
    elif current_screen == RUN_SINGLE:
        if run_action:
            maze_copy = [row[:] for row in predefined_maze]
            if run_action == "dfs":
                dfs_solve(maze_copy)
            elif run_action == "bfs":
                bfs_solve(maze_copy)
            elif run_action == "a_star":
                a_star_solve(maze_copy)
            elif run_action == "dijkstra":
                dijkstra_solve(maze_copy)
            elif run_action == "prim":
                generate_prims()
            elif run_action == "kruskal":
                generate_kruskals()
            elif run_action == "backtracking":
                generate_recursive_backtracking()
        run_action = None
        current_screen = MAIN_MENU

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if current_screen == MAIN_MENU:
                if event.key == pygame.K_i:
                    current_screen = INFO_SCREEN
                elif event.key == pygame.K_c:
                    current_screen = COMPARE_SOLVING
                elif event.key == pygame.K_v:
                    current_screen = COMPARE_GENERATION
                elif event.key == pygame.K_d:
                    run_action = "dfs"
                    current_screen = RUN_SINGLE
                elif event.key == pygame.K_b:
                    run_action = "bfs"
                    current_screen = RUN_SINGLE
                elif event.key == pygame.K_a:
                    run_action = "a_star"
                    current_screen = RUN_SINGLE
                elif event.key == pygame.K_s:
                    run_action = "dijkstra"
                    current_screen = RUN_SINGLE
                elif event.key == pygame.K_p:
                    run_action = "prim"
                    current_screen = RUN_SINGLE
                elif event.key == pygame.K_k:
                    run_action = "kruskal"
                    current_screen = RUN_SINGLE
                elif event.key == pygame.K_r:
                    run_action = "backtracking"
                    current_screen = RUN_SINGLE
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif current_screen in [INFO_SCREEN]:
                current_screen = MAIN_MENU


