import pygame as pg
import heapq, math
import random
import sys
sys.setrecursionlimit(10000)
#PYGAME SETTINGS
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
ROWS = 21
COLS = 21
WIDTH, HEIGHT = 588, 588 #606
GAP = WIDTH // ROWS
#Iitialize PG Window
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()


class Node:
    def __init__(self, width):
        self.explored = False
        self.blocked = False
        self.visiblyBlocked = False
        self.g = math.inf
        self.h = None
        self.x = None
        self.y = None
        self.prev = None
        self.search = 0
        self.width = width
        self.color = None

    def color_open(self):
        self.color = TURQUOISE

    def color_finalpath(self):
        self.color = PURPLE

    def color_unblocked(self):
        self.color = WHITE

    def color_goal(self):
        self.color = RED

    def color_start(self):
        self.color = GREEN

    def color_blocked(self):
        self.color = BLACK

    def draw(self, win):
        pg.draw.rect(win, self.color, ((self.x)*(self.width), (self.y)*(self.width), self.width, self.width))

    def __lt__(self, other):

        if self.g + self.h == other.g + other.h:
            return self.g < other.g
        else:
            return self.g + self.h < other.g + other.h

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

class Graph:
    def __init__(self, x, y):
        self.graph = [[Node(GAP) for j in range(x)] for i in range(y)]
        self.DFS()

    def DFS(self):
        for x in range(len(self.graph)):
            for y in range(len(self.graph[x])):
                if not self.graph[x][y].explored:
                    self.explore(x,y)

    def explore(self, x, y):
        #set current node to explored, set it to blocked with 30% probability and unblocked with 70% probability
        # if it is blocked, return graph without exploring neighbors
        # if it is unblocked, explore neighors
        if self.graph[x][y].explored:
            return

        self.graph[x][y].explored = True
        if random.random() < .3:
            self.graph[x][y].blocked = True
            return
        #at this point the node is unblocked, so add neighbors to openList
        openList = []
        # check y+1
        if (y+1) < len(self.graph[0]):
            if not self.graph[x][y+1].explored:
                openList.append([x, y+1])
        #check y-1
        if (y-1) >= 0:
            if not self.graph[x][y-1].explored:
                openList.append([x, y-1])
        #check x+1
        if (x+1) < len(self.graph):
            if not self.graph[x+1][y].explored:
                openList.append([x+1, y])
        #check x-1
        if (x-1) >= 0:
            if not self.graph[x-1][y].explored:
                openList.append([x-1, y])
        #explore the items in the open list in random order
        while openList:
            neighbor = random.choice(openList)
            graph = self.explore(neighbor[0], neighbor[1])
            openList.remove(neighbor)

    def __str__(self, curr):
        string = ''
        for x in range(len(self.graph)):
            for y in range(len(self.graph[x])):
                if self.graph[x][y] == curr:
                    string = string + " * "
                elif self.graph[x][y].blocked == False:
                    string = string + ' 1 '
                else:
                    string = string + ' 0 '
            string = string + '\n'
        return string

    def draw_blocks(self, s, g): #curr
        for x in range(len(self.graph)):
            for y in range(len(self.graph[x])):
                if self.graph[x][y] == s:
                    self.graph[x][y].color_start()
                    self.graph[x][y].draw(WIN)
                elif self.graph[x][y] == g:
                    self.graph[x][y].color_goal()
                    self.graph[x][y].draw(WIN)
                # if self.graph[x][y] == curr:
                #     self.graph[x][y].color_curr()
                #     self.graph[x][y].draw(WIN)
                elif self.graph[x][y].blocked == True:
                    self.graph[x][y].color_blocked()
                    self.graph[x][y].draw(WIN)
                # else:
                #     self.graph[x][y].color_blocked()
                #     self.graph[x][y].draw(WIN)

    def draw_final_path(self, fpath):
        pass


#returns a random unblocked node in the graph
def selectRandomNode(graph):
    x = random.randint(0, ROWS-1) #100
    y = random.randint(0, COLS-1) #100
    start = graph.graph[x][y]
    start.x = x
    start.y = y
    if start.blocked:
        start = selectRandomNode(graph)
    return start

#checks all neighbors of the given node. If they are blocked, sets them to visiblyBlocked = True
def setNeighborsToVisiblyBlocked(node, graph):
    xOffsets = [1, -1, 0, 0]
    yOffsets = [0, 0, 1, -1]
    for i in range(4):
        x = node.x + xOffsets[i]
        y = node.y + yOffsets[i]
        if x >= 0 and x < ROWS and y >= 0 and y < COLS and graph[x][y].blocked:
            graph[x][y].visiblyBlocked = True

def computePath(graph, goal, openList, visited, counter, start):
    while openList:
        curr = heapq.heappop(openList)
        visited.add(curr)

        if(curr == goal):
            break

        #find neighbors and compute g cost
        xOffsets = [1, -1, 0, 0]
        yOffsets = [0, 0, 1, -1]
        for i in range(4):
            x = curr.x + xOffsets[i]
            y = curr.y + yOffsets[i]

            if x >= 0 and x < len(graph) and y >= 0 and y < len(graph) and not graph[x][y].visiblyBlocked and not graph[x][y] in visited:
                neighbor = graph[x][y]
                if neighbor.search < counter:
                    neighbor.search = counter
                    neighbor.g = math.inf
                if neighbor in openList:
                    # figure out if you need to update the f score
                    newG = curr.g + 1
                    if (newG) < (neighbor.g):
                        neighbor.g = newG
                        neighbor.prev = curr
                        heapq.heapify(openList)
                        neighbor.color_open()
                else:
                    neighbor.g = curr.g + 1
                    neighbor.prev = curr
                    heapq.heappush(openList, neighbor)
    path = []
    while(curr != start):
        path.insert(0, (curr.x, curr.y))
        curr = curr.prev
    return path

def draw_final_path(win, graph, fpath):
    for x in range(len(graph.graph)):
        for y in range(len(graph.graph[x])):
            for i, j in fpath:
                if i == x and j == y:
                    graph.graph[x][y].color_finalpath()
                    graph.graph[x][y].draw(win)



def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows+1):
        pg.draw.line(win, GREY, (0, i * gap), (width, i *gap))
        for j in range(rows+1):
            pg.draw.line(win, GREY, (j * gap, 0), (j *gap, width))

def draw(win, rows, width, graph, s, g): #curr
    #fill screen
    win.fill(WHITE)
    #draw a rect with color
    graph.draw_blocks(s, g) #curr
    #draw grid lines
    draw_grid(win, rows, width)
    pg.display.update()

def main(win, width):

    counter = 0
    graph = Graph(ROWS, COLS)
    #Select start node randomly
    start = selectRandomNode(graph)
    #Select goal node randomly
    goal = selectRandomNode(graph)
    #initialize finalPath List, add start to it
    finalPath = []
    finalPath.append((start.x, start.y))

    #print start and goal coordinates
    print('start = (' + str(start.x) + ', ' + str(start.y) + ')')
    print('goal = (' + str(goal.x) + ', ' + str(goal.y) + ')')

    for i in range(len(graph.graph)):
        for j in range(len(graph.graph[i])):
            manhattanDist = abs(i - goal.x) + abs(j - goal.y)
            graph.graph[i][j].h = manhattanDist
            graph.graph[i][j].x = i
            graph.graph[i][j].y = j

    draw(win, ROWS, width, graph, start, goal) #start
    pg.event.clear()
    run = True
    while run:
        draw(win, ROWS, width, graph, start, goal) #start
        clock.tick(1)

        #pg.display.update() // take this out of draw funtction
        event = pg.event.wait()
        if event.type == pg.QUIT:
            run = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                while start != goal:
                    setNeighborsToVisiblyBlocked(start, graph.graph)
                    counter = counter + 1
                    start.g = 0
                    start.search = counter
                    goal.search = counter
                    goal.g = math.inf
                    openList = []
                    visited = set()
                    openList.append(start)
                    path = computePath(graph.graph, goal, openList, visited, counter, start)
                    #move start along the computed path, ensure that there are no blocked nodes
                    # if there are blocked nodes, compute a new path with start set to the furthest unblocked node
                    for i in range(len(path)):
                        start = graph.graph[path[i][0]][path[i][1]]
                        #draw final path to pygame window
                        graph.graph[path[i][0]][path[i][1]].color_finalpath()
                        graph.graph[path[i][0]][path[i][1]].draw(win)
                        pg.display.update()
                        if start.blocked:
                            start = graph.graph[path[i - 1][0]][path[i - 1][1]]
                            break
                        setNeighborsToVisiblyBlocked(start, graph.graph)
                        finalPath.append((start.x, start.y))


    pg.quit()

    print(graph.__str__(start))
    print('\n')
    print(finalPath)

main(WIN, WIDTH)
