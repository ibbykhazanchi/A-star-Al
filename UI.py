from A_Star_Settings import *
from Graph import Graph
from Algorithms import *
import pygame as pg

#initialize pygame
pg.init()

clock = pg.time.Clock()
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)

pg.font.init()
myfont = pg.font.SysFont(FONT, FONT_SIZE, True)

forward_prompt = myfont.render('Press "1" for Repeated Forward', False, PURPLE, BLACK)
backward_prompt = myfont.render('Press "2" for Repeated Backward', False, ORANGE, BLACK)
adaptive_prompt = myfont.render('Press "3" for Adaptive', False, TURQUOISE, BLACK)
start_prompt = myfont.render('Start State', False, GREEN, BLACK)
goal_prompt = myfont.render('Goal State', False, RED, BLACK)

def draw(win, gr, grid_dim, block_dim, win_dim, fps):
    win.fill(BG_COLOR)
    for x in range(len(gr.graph)):
        for y in range(len(gr.graph[x])):
            gr.graph[y][x].draw_node(win)
    draw_grid(win, grid_dim, block_dim, win_dim)
    win.blit(forward_prompt,(610,10))
    win.blit(backward_prompt,(610,50))
    win.blit(adaptive_prompt,(610,90))
    win.blit(start_prompt,(610,130))
    win.blit(goal_prompt,(610,170))
    pg.display.update()
    clock.tick(fps)

def draw_grid(win, grid_dim, block_dim, win_dim):
    gap = block_dim
    for i in range(0, grid_dim):
        pg.draw.line(win, GREY, (0, i * gap), (win_dim, i * gap))
        for j in range(0, grid_dim +1):
            pg.draw.line(win, GREY, (j * gap, 0), (j *gap, win_dim))

def main():
    graph = Graph(GRID_DIM,GRID_DIM)
    start = selectRandomNode(graph)
    print(start)
    goal = selectRandomNode(graph)
    print(goal)

    init_graph(graph)
    graph.draw_blocks(start, goal)

    run = True
    while run:

        draw(WIN, graph, GRID_DIM, BLOCK_DIM, WIN_DIM, FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                repeatedForwardsAlgo(lambda: draw(WIN, graph, GRID_DIM, BLOCK_DIM, WIN_DIM, FPS), graph, start, goal)

            if event.key == pg.K_2:
                repeatedBackwardsAlgo(lambda: draw(WIN, graph, GRID_DIM, BLOCK_DIM, WIN_DIM, FPS), graph, start, goal)

            if event.key == pg.K_3:
                adaptiveAlgorithm(lambda: draw(WIN, graph, GRID_DIM, BLOCK_DIM, WIN_DIM, FPS), graph, start, goal)

    pg.quit()

main()
