import pygame
import heapq

WIDTH = 600
ROWS = 25
CELL = WIDTH // ROWS

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

def heuristic(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(draw, grid, start, end):
    open_list = []
    heapq.heappush(open_list,(0,start))
    came = {}
    g = {start:0}

    while open_list:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        _, current = heapq.heappop(open_list)

        if current == end:
            while current in came:
                current = came[current]
                if current != start:
                    grid[current[0]][current[1]] = BLUE
                draw()
                pygame.time.delay(40)
            return True

        for d in [(0,1),(1,0),(0,-1),(-1,0)]:
            n = (current[0]+d[0], current[1]+d[1])

            if 0<=n[0]<ROWS and 0<=n[1]<ROWS and grid[n[0]][n[1]]!=BLACK:
                temp = g[current] + 1

                if n not in g or temp < g[n]:
                    g[n] = temp
                    f = temp + heuristic(n,end)
                    heapq.heappush(open_list,(f,n))
                    came[n] = current

                    if n != end:
                        grid[n[0]][n[1]] = YELLOW

        draw()
        pygame.time.delay(20)

    return False

def draw(win, grid):
    win.fill(WHITE)
    for i in range(ROWS):
        for j in range(ROWS):
            pygame.draw.rect(win, grid[i][j],
                (j*CELL, i*CELL, CELL, CELL))
    pygame.display.update()

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH,WIDTH))
    pygame.display.set_caption("A* Pathfinding Visualizer")

    grid = [[WHITE for _ in range(ROWS)] for _ in range(ROWS)]

    start = None
    end = None

    run = True
    while run:
        draw(win, grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                x,y = pygame.mouse.get_pos()
                r,c = y//CELL, x//CELL
                grid[r][c] = BLACK

            if pygame.mouse.get_pressed()[2]:
                x,y = pygame.mouse.get_pos()
                r,c = y//CELL, x//CELL
                grid[r][c] = WHITE

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_s:
                    x,y = pygame.mouse.get_pos()
                    r,c = y//CELL, x//CELL
                    start = (r,c)
                    grid[r][c] = GREEN

                if event.key == pygame.K_e:
                    x,y = pygame.mouse.get_pos()
                    r,c = y//CELL, x//CELL
                    end = (r,c)
                    grid[r][c] = RED

                if event.key == pygame.K_SPACE:
                    if start and end:
                        astar(lambda: draw(win, grid), grid, start, end)

                if event.key == pygame.K_c:
                    grid = [[WHITE for _ in range(ROWS)] for _ in range(ROWS)]
                    start = None
                    end = None

    pygame.quit()

main()
