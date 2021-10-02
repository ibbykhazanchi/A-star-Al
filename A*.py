import random
import sys
sys.setrecursionlimit(10000)

class Node:
    def __init__(self):
        self.explored = False
        self.blocked = False
        self.g = None
        self.h = None

#initialize graph and call DFS to set nodes to blocked/unblocked, then return graph
def createGraph():
    graph = [[Node() for j in range(101)] for i in range(101)]
    DFS(graph)
    return graph

def DFS(graph):
    for x in range(101):
         for y in range(101):
             if not graph[x][y].explored:
                 graph = explore(graph, x, y) 
    return graph          

def explore(graph, x, y):

    #set current node to explored, set it to blocked with 30% probability and unblocked with 70% probability
    # if it is blocked, return graph without exploring neighbors
    # if it is unblocked, explore neighors
    graph[x][y].explored = True
    if random.random() < .3:
        graph[x][y].blocked = True
        
    #at this point the node is unblocked, so add neighbors to openList
    openList = []
    xOffsets = [1, -1, 0, 0]
    yOffsets = [0,0, -1, 1]

    for i in range(4):
        newX = x + xOffsets[i]
        newY = y + yOffsets[i]

        if newX >= 0 and newX < 101 and newY >= 0 and newY < 101 and (graph[newX][newY].explored == False):
            openList.append([newX, newY])
    
    #explore the items in the open list in random order
    while openList:
        neighbor = random.choice(openList)
        graph = explore(graph, neighbor[0], neighbor[1])
        openList.remove(neighbor)



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



def main():
    create50graphs()

main()



