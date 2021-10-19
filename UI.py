from A_Star_Settings import *
from Graph import Graph
from Algorithms import *
import pygame as pg
from os import path

#initialize pygame
pg.init()

clock = pg.time.Clock()
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)

pg.font.init()
myfont = pg.font.SysFont(FONT, FONT_SIZE, True)

forward_prompt = myfont.render('Press "1" for Repeated Forward', False, PURPLE)
cpath_forward = myfont.render('Computed Repeated Forward Path', False, BLUE)
backward_prompt = myfont.render('Press "2" for Repeated Backward', False, ORANGE)
cpath_backward = myfont.render('Computed Repeated Backward Path', False, DARK_CHAR)
adaptive_prompt = myfont.render('Press "3" for Adaptive', False, TURQUOISE)
cpath_adaptive = myfont.render('Computed Adaptive Path', False, DEEP_PINK)
start_prompt = myfont.render('Start State', False, GREEN)
goal_prompt = myfont.render('Goal State', False, RED)
reset_prompt = myfont.render('Press "c" to reset grid', False, YELLOW)
load_forward = myfont.render('Press "f" to load Repeated Forward grid', False, PURPLE)
load_backward = myfont.render('Press "b" to load Repeated Backward grid', False, ORANGE)
load_adaptive = myfont.render('Press "a" to load Adaptive grid', False, TURQUOISE)
expanded_prompt = myfont.render('Expanded Nodes:', False, WHITE)
expanded_line = myfont.render('______________', False, WHITE)

def make_prompt(n_exp, color):
    return myfont.render(str(n_exp), False, color)

def graphAsString(graph):
    string = ''
    for x in range(GRID_DIM):
        for y in range(GRID_DIM):
            if graph.graph[y][x].color == LIGHTGREY:
                string = string + '1'
            elif graph.graph[y][x].color == WHITE:
                string = string + '0'
            elif graph.graph[y][x].color == BLACK:
                string = string + 'V'
            elif graph.graph[y][x].color == GREEN:
                string = string + 'S'
            elif graph.graph[y][x].color == RED:
                string = string + 'G'
            elif graph.graph[y][x].color == BLUE:
                string = string + 'B'
            elif graph.graph[y][x].color == DARK_CHAR:
                string = string + 'C'
            elif graph.graph[y][x].color == DEEP_PINK:
                string = string + 'K'
            elif graph.graph[y][x].color == PURPLE:
                string = string + 'P'
            elif graph.graph[y][x].color == ORANGE:
                string = string + 'O'
            elif graph.graph[y][x].color == TURQUOISE:
                string = string + 'T'
        string = string + '\n'
    return string

def loadGraph(graph, gFile):
    folder = path.dirname(__file__)
    map_data = []
    with open(path.join(folder, gFile), 'rt') as f:
        for line in f:
            map_data.append(line)
    for i, row in enumerate(map_data):
        for j, node in enumerate(row):
                    if node == '1':
                        graph.graph[j][i].is_blocked()
                    elif node == '0':
                        graph.graph[j][i].reset()
                    elif node == 'V':
                        graph.graph[j][i].is_visibly_blocked()
                    elif node == 'S':
                        graph.graph[j][i].is_start()
                    elif node == 'G':
                        graph.graph[j][i].is_goal()
                    elif node == 'B':
                        graph.graph[j][i].is_cpath_forward()
                    elif node == 'C':
                        graph.graph[j][i].is_cpath_backward()
                    elif node == 'K':
                        graph.graph[j][i].is_cpath_adaptive()
                    elif node == 'P':
                        graph.graph[j][i].is_forward_path()
                    elif node == 'O':
                        graph.graph[j][i].is_backward_path()
                    elif node == 'T':
                        graph.graph[j][i].is_adaptive_path()

def saveGraph(graph, fName):
    file = open(fName, 'w')
    file.write(graphAsString(graph))
    file.write('\n')
    file.close()

def resetGraph(graph):
    for x in range(GRID_DIM):
        for y in range(GRID_DIM):
            if graph.graph[x][y].blocked == True and graph.graph[x][y].color != LIGHTGREY:
                graph.graph[x][y].is_blocked()
            elif graph.graph[x][y].blocked == False and graph.graph[x][y].color != GREEN and graph.graph[x][y].color != RED:
                graph.graph[x][y].reset()

def draw(win, gr, grid_dim, block_dim, win_dim, fps, fNode, bNode, aNode):
    win.fill(BG_COLOR)
    for x in range(len(gr.graph)):
        for y in range(len(gr.graph[x])):
            gr.graph[y][x].draw_node(win)

    draw_grid(win, grid_dim, block_dim, win_dim)
    win.blit(forward_prompt,(610,10))
    win.blit(cpath_forward,(610,40))
    win.blit(backward_prompt,(610,70))
    win.blit(cpath_backward,(610,100))
    win.blit(adaptive_prompt,(610,130))
    win.blit(cpath_adaptive,(610,160))
    win.blit(start_prompt,(610,190))
    win.blit(goal_prompt,(610,220))
    win.blit(reset_prompt,(610,250))
    win.blit(load_forward,(610,280))
    win.blit(load_backward,(610,310))
    win.blit(load_adaptive,(610,340))
    win.blit(expanded_prompt,(610,370))
    win.blit(expanded_line,(610,375))
    win.blit(fNode,(610,400))
    win.blit(bNode,(610,430))
    win.blit(aNode,(610,460))
    pg.display.update()
    clock.tick(fps)

def draw_grid(win, grid_dim, block_dim, win_dim):
    gap = block_dim
    for i in range(0, grid_dim):
        pg.draw.line(win, GREY, (0, i * gap), (win_dim, i * gap))
        for j in range(0, grid_dim +1):
            pg.draw.line(win, GREY, (j * gap, 0), (j *gap, win_dim))

def main():
    f = open(fileName1,"w")
    f.close()
    f = open(fileName2,"w")
    f.close()
    f = open(fileName3,"w")
    f.close()
    fNodes_expanded = 0
    bNodes_expanded = 0
    aNodes_expanded = 0
    graph = Graph(GRID_DIM,GRID_DIM)
    start = selectRandomNode(graph)
    goal = selectRandomNode(graph)

    init_graph(graph)
    graph.draw_blocks(start, goal)

    run = True
    while run:
        f_expanded = make_prompt(fNodes_expanded, PURPLE)
        b_expanded = make_prompt(bNodes_expanded, ORANGE)
        a_expanded = make_prompt(aNodes_expanded, TURQUOISE)
        draw(WIN, graph, GRID_DIM, BLOCK_DIM, WIN_DIM, FPS, f_expanded, b_expanded, a_expanded)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                resetGraph(graph)
                graph.resetNodes()
                number = 1
                fNodes_expanded = repeatedForwardsAlgo(lambda: draw(WIN, graph, GRID_DIM, BLOCK_DIM, WIN_DIM, FPS, f_expanded, b_expanded, a_expanded), number, graph, start, goal)
                saveGraph(graph, fileName1)

            if event.key == pg.K_2:
                resetGraph(graph)
                graph.resetNodes()
                number = 2
                bNodes_expanded = repeatedBackwardsAlgo(lambda: draw(WIN, graph, GRID_DIM, BLOCK_DIM, WIN_DIM, FPS, f_expanded, b_expanded, a_expanded), number, graph, start, goal)
                saveGraph(graph, fileName2)

            if event.key == pg.K_3:
                resetGraph(graph)
                graph.resetNodes()
                number = 3
                aNodes_expanded = adaptiveAlgorithm(lambda: draw(WIN, graph, GRID_DIM, BLOCK_DIM, WIN_DIM, FPS, f_expanded, b_expanded, a_expanded), number, graph, start, goal)
                saveGraph(graph, fileName3)

            if event.key == pg.K_c:
                resetGraph(graph)

            if event.key == pg.K_f:
                graphFile = 'forward_graph.txt'
                filesize = path.getsize(graphFile)
                if filesize == 0:
                    print('empty file')
                else:
                    loadGraph(graph, graphFile)


            if event.key == pg.K_b:
                graphFile = 'backward_graph.txt'
                filesize = path.getsize(graphFile)
                if filesize == 0:
                    print('empty file')
                else:
                    loadGraph(graph, graphFile)


            if event.key == pg.K_a:
                graphFile = 'adaptive_graph.txt'
                filesize = path.getsize(graphFile)
                if filesize == 0:
                    print('empty file')
                else:
                    loadGraph(graph, graphFile)

    pg.quit()

main()
