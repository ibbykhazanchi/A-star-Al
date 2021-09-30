import random
import sys
sys.setrecursionlimit(10000)

class Node:
    def __init__(self):
        self.explored = False
        self.blocked = None
        self.g = None
        self.h = None

#initialize graph and call DFS to set nodes to blocked/unblocked, then return graph
def createGraph():
    graph = [[Node() for j in range(101)] for i in range(101)]
    graph = DFS(graph)
    return graph

def DFS(graph):
    for x in range(101):
         for y in range(101):
             if graph[x][y].explored == True:
                 continue
             else:
                 graph = explore(graph, x, y) 
    return graph          

def explore(graph, x, y):

    #set current node to explored, set it to blocked with 30% probability and unblocked with 70% probability
    # if it is blocked, return graph without exploring neighbors
    # if it is unblocked, explore neighors
    if graph[x][y].explored:
        return graph

    graph[x][y].explored = True
    if random.random() < .7:
        graph[x][y].blocked = False
    else:
        graph[x][y].blocked = True
        return graph
    #at this point the node is unblocked, so add neighbors to openList
    openList = []
    # check y+1
    if (y+1) <= 100:
        if not graph[x][y+1].explored:
            openList.append([x, y+1])
    #check y-1
    if (y-1) >= 0:
        if not graph[x][y-1].explored:
            openList.append([x, y-1])
    #check x+1
    if (x+1) <= 100:
        if not graph[x+1][y].explored:
            openList.append([x+1, y])
    #check x-1
    if (x-1) >= 0:
        if not graph[x-1][y].explored:
            openList.append([x-1, y])
    #explore the items in the open list in random order
    while openList:
        neighbor = random.choice(openList)
        graph = explore(graph, neighbor[0], neighbor[1])
        openList.remove(neighbor)
    #finally, return graph once all neighbors have been explored
    return graph


def create50graphs():
    #loop x50
    #for each iteration, call createGraph() and append the result to a file
    file = open('graph.txt', 'a')
    for x in range(50):
        graph = createGraph()
        file.write(graphAsString(graph))
        file.write('\n')
    file.close()

#returns string representation of the graph, used to append to file
def graphAsString(graph):
    string = ''
    for x in range(101):
        for y in range(101):
            if graph[x][y].blocked == False:
                string = string + '_'
            else:
                string = string + 'X'
        string = string + '\n'
    return string

#prints graph for testing purposes
def printGraph(graph):
    for x in range(101):
        for y in range(101):
            if graph[x][y].blocked == False:
                print('_', end='')
            else:
                print('X', end='')
        print('')

def main():
    create50graphs()

main()



