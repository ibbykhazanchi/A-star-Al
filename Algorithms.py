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

def setHValues(graph, goal):
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            manhattanDist = abs(i - goal.x) + abs(j - goal.y)
            graph[i][j].h = manhattanDist
            graph[i][j].x = i
            graph[i][j].y = j

#this method checks for duplicate nodes on a path. If it finds them, it deletes one of them as well as all of the nodes between them.
def removePathDuplicates(path):
    for i in range(len(path)):
        for j in range((i + 1), len(path)): 
            if path[i] == path[j] and i != j:
                del path[i:j]
                removePathDuplicates(path)
                return

#test method used to ensure a path is valid, ie no nodes along it are blocked
def printBlocked(path, graph):
    for i in range(len(path)):
        if graph[path[i][0]][path[i][1]].blocked:
            print('BLOCKED')

#main A* algo, used by both repeatedForwards and repeatedBackwards
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

#test A-star algo that does not repeat and has full knowledge of the environment from the get-go
def testAStar(graph, goal, openList, visited, counter, start):
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

            if x >= 0 and x < len(graph) and y >= 0 and y < len(graph) and not graph[x][y].blocked and not graph[x][y] in visited:
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

def repeatedForwardsAlgo(graph, start, goal):
    counter = 0
    #initialize finalPath List, add start to it
    finalPath = []
    finalPath.append((start.x, start.y))

    #initialize hValues
    setHValues(graph.graph, goal)

    nodesExpanded = 0

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
        #check if goal is unreachable by checking if goal is on the path
        if (goal.x, goal.y) not in path:
            print('UNREACHABLE')
            return
        #move start along the computed path, ensure that there are no blocked nodes
        # if there are blocked nodes, compute a new path with start set to the furthest unblocked node
        for i in range(len(path)):
            start = graph.graph[path[i][0]][path[i][1]]
            if start.blocked:
                start = graph.graph[path[i - 1][0]][path[i - 1][1]]
                break
            setNeighborsToVisiblyBlocked(start, graph.graph)
            finalPath.append((start.x, start.y))
        
        nodesExpanded += len(visited)
    #remove any duplicates, print the length, print the final path
    return nodesExpanded
def repeatedBackwardsAlgo(graph, start, goal):
    counter = 0
    #initialize finalPath List, add start to it
    finalPath = []
    finalPath.append((start.x, start.y))

    nodesExpanded = 0

    while start != goal:
        #initialize (or recompute) hValues
        setHValues(graph.graph, start)

        setNeighborsToVisiblyBlocked(start, graph.graph)
        counter = counter + 1
        goal.g = 0
        start.search = counter
        goal.search = counter
        start.g = math.inf
        openList = []
        visited = set()
        openList.append(goal)
        path = computePath(graph.graph, start, openList, visited, counter, goal)
        #check if goal is unreachable by checking if start is on the path
        if (start.x, start.y) not in path:
            print('UNREACHABLE')
            return
        #reverse path, add goal node to the end, remove first node (start)
        path.reverse()
        path.append((goal.x, goal.y))
        path.pop(0)
        #move start along the computed path, ensure that there are no blocked nodes
        # if there are blocked nodes, compute a new path with start set to the furthest unblocked node
        for i in range(len(path)):
            start = graph.graph[path[i][0]][path[i][1]]
            if start.blocked:
                start = graph.graph[path[i - 1][0]][path[i - 1][1]]
                break
            setNeighborsToVisiblyBlocked(start, graph.graph)
            finalPath.append((start.x, start.y))

        nodesExpanded += len(visited)
    return nodesExpanded

def adaptiveAlgo(graph, start, goal):
    counter = 0
    #initialize finalPath List, add start to it
    finalPath = []
    finalPath.append((start.x, start.y))

    #initialize hValues
    setHValues(graph.graph, goal)

    nodesExpanded = 0

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
        #check if goal is unreachable by checking if goal is on the path
        if (goal.x, goal.y) not in path:
            print('UNREACHABLE')
            return
        #update the expanded nodes' heuristics
        for node in visited:
            node.h = goal.g - node.g

        #move start along the computed path, ensure that there are no blocked nodes
        # if there are blocked nodes, compute a new path with start set to the furthest unblocked node
        for i in range(len(path)):
            start = graph.graph[path[i][0]][path[i][1]]
            if start.blocked:
                start = graph.graph[path[i - 1][0]][path[i - 1][1]]
                break
            setNeighborsToVisiblyBlocked(start, graph.graph)
            finalPath.append((start.x, start.y))
        
        nodesExpanded += len(visited)
    return nodesExpanded

def consistencyTest(graph):
    # iterate through entire grid
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            # mark current node
            curr = graph[i][j]

            xOffsets = [1, -1, 0, 0]
            yOffsets = [0, 0, 1, -1]
            for i in range(4):
                x = curr.x + xOffsets[i]
                y = curr.y + yOffsets[i]

                if x >= 0 and x < len(graph) and y >= 0 and y < len(graph):
                    # mark neighboring node
                    neighbor = graph[x][y]

                    # check if triangle inequality doesn't hold
                    if curr.h > neighbor.h + 1:
                        return False
    
    # triangle inequality holds
    return True

