import random,sys,math
sys.setrecursionlimit(10000)

class Node:
    def __init__(self):
        self.explored = False
        self.blocked = False
        self.g = math.inf
        self.h = None
        self.x = None
        self.y = None
        self.prev = None

    def __lt__(self, other):

        if self.g + self.h == other.g + other.h:
            return self.g < other.g
        else:
            return self.g + self.h < other.g + other.h

    def __str__(self):
        return "Node: { g value : " + str(self.g) + " }, { h value : " + str(self.h) + " }"

class Graph:
    def __init__(self, x, y):
        self.graph = [[Node() for j in range(x)] for i in range(y)]
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

def create50graphs():
    #loop x50
    #for each iteration, call createGraph() and append the result to a file
    file = open('graph.txt', 'a')
    for x in range(5):
        graph = Graph(10, 10)
        file.write(graph.__str__(None))
        file.write('\n')
    file.close()

create50graphs()