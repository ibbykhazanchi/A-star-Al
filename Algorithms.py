from Graph import Node, Graph
import heapq, math
import random

#returns a random unblocked node in the graph
def selectRandomNode(graph):
    x = random.randint(0, 100)
    y = random.randint(0, 100)
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
        if x >= 0 and x < 101 and y >= 0 and y < 101 and graph[x][y].blocked: 
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
                else:
                    neighbor.g = curr.g + 1
                    neighbor.prev = curr
                    heapq.heappush(openList, neighbor)
    path = []
    while(curr != start):
        path.insert(0, (curr.x, curr.y))
        curr = curr.prev
    return path

def repeatedAlgo(graph, start, goal):
    counter = 0
    #initialize finalPath List, add start to it
    finalPath = []
    finalPath.append((start.x, start.y))

    #print start and goal coordinates
    print('start = (' + str(start.x) + ', ' + str(start.y) + ')')
    print('goal = (' + str(goal.x) + ', ' + str(goal.y) + ')')

    #initialize hValues
    for i in range(len(graph.graph)):
        for j in range(len(graph.graph[i])):
            manhattanDist = abs(i - goal.x) + abs(j - goal.y)
            graph.graph[i][j].h = manhattanDist
            graph.graph[i][j].x = i
            graph.graph[i][j].y = j

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
            if start.blocked:
                start = graph.graph[path[i - 1][0]][path[i - 1][1]]
                break
            setNeighborsToVisiblyBlocked(start, graph.graph)
            finalPath.append((start.x, start.y))
    print(graph.__str__(start))
    print('\n')
    print(finalPath)