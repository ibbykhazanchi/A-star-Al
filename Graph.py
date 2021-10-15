import random,sys,math
sys.setrecursionlimit(10000)

class Node:
    def __init__(self):
        self.explored = False
        self.blocked = False
        self.visiblyBlocked = False
        self.g = math.inf
        self.h = None
        self.x = None
        self.y = None
        self.prev = None
        self.search = 0
        self.gFlag = False

    def __lt__(self, other):

        if self.g + self.h == other.g + other.h:
            #if g value is equal, break tie randomly
            if self.g == other.g:
                if random.random() < 0.5:
                    return True
                else:
                    return False
            if not self.gFlag:
                return self.g > other.g
            else:
                return self.g < other.g
        else:
            return self.g + self.h < other.g + other.h

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

class Graph:
    def __init__(self, x, y):
        self.graph = [[Node() for j in range(x)] for i in range(y)]
        self.DFS()

    #Sets all visibly blocked to false, and all search values to 0
    #necessary to cleanse the graph between calling different algorithms
    def resetNodes(self):
        for i in range(len(self.graph)):
            for j in range(len(self.graph[i])):
                self.graph[i][j].visiblyBlocked = False
                self.graph[i][j].search = 0
    
    #
    def setGFlags(self):
        for i in range(len(self.graph)):
            for j in range(len(self.graph[i])):
                self.graph[i][j].gFlag = True

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

def create50graphs():
    #loop x50
    #for each iteration, call createGraph() and append the result to a file
    graphs = []
    for x in range(50):
        graph = Graph(101, 101)
        graphs.append(graph)
    return graphs

create50graphs()