import pygame as pg
import random
import math
import sys
from os import path
from queue import PriorityQueue

MAPFILE = 'onegraph.txt'
TITLE = 'A Star Test'

#Define Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

#width/height of window
ROWS = 101
WIDTH, HEIGHT = 606, 606
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        #DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        #UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        #RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        #LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

#define heuristic function(Manhattan distance)
def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1 -y2)

#go back to start node and draw optimal path
def reconstruct_path(last, current, draw):
    while current in last:
        current = last[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    #for breaking ties
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    last = {}

    g = {node: float("inf") for row in grid for node in row}
    g[start] = 0

    f = {node: float("inf") for row in grid for node in row}
    f[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(last, end, draw)
            end.make_end()
            return True
        for neighbor in current.neighbors:
            temp_g = g[current] + 1

            if temp_g < g[neighbor]:
                last[neighbor] = current
                g[neighbor] = temp_g
                f[neighbor] = temp_g + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


#store nodes in lists and append to rows of grid
def make_grid(rows, width):
    alg_folder = path.dirname(__file__)
    map_data = []
    grid = []
    gap = width // rows
    with open(path.join(alg_folder, MAPFILE), 'rt') as f:
        for line in f:
            map_data.append(line)

    # for i in range(rows):
    #     grid.append([])
    #     for j in range(rows):
    #         node = Node(i, j, gap, rows)
    #         grid[i].append(node)

    for i, blocks in enumerate(map_data):
        print(i, blocks)
        grid.append([])
        for j, block in enumerate(blocks):
            if block == 'X':
                node = Node(i, j, gap, rows)
                grid[i].append(node)
                node.make_barrier()
            else:
                node = Node(i, j, gap, rows)
                grid[i].append(node)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pg.draw.line(win, GREY, (0, i * gap), (width, i *gap))
        for j in range(rows):
            pg.draw.line(win, GREY, (j * gap, 0), (j *gap, width))

def draw(win, grid, rows, width):
    #fill screen
    win.fill(WHITE)
    #draw a rect with color
    for row in grid:
        for node in row:
            node.draw(win)
    #draw grid lines
    draw_grid(win, rows, width)

    pg.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    #ROWS = 101
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            #if left mouse button is pressed
            if pg.mouse.get_pressed()[0]:
                #gives x, y coordinate of mouse position
                pos = pg.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]

                if not start and node != end:
                    if node.is_barrier() == True:
                        start = None

                    else:
                        start = node
                        start.make_start()

                if not end and node != start:
                    if node.is_barrier() == True:
                        end = None

                    else:
                        end = node
                        end.make_end()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                #reset program
                if event.key == pg.K_r:
                    start = None
                    end = None
                    grid = make_grid(ROWS,width)

    pg.quit()

main(WIN, WIDTH)
