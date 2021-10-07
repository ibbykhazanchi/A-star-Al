from Graph import Node
import heapq, math

def printGraph(graph):
        string = ''
        for x in range(len(graph)):
            for y in range(len(graph[x])):
                if graph[x][y] == curr:
                    string = string + " * "
                elif graph[x][y].blocked == False:
                    string = string + ' 1 '
                else:
                    string = string + ' 0 '
            string = string + '\n'
        print(string)

def print50Lines():
    for i in range(5):
        print("\n")

graph = [[Node() for j in range(5)] for i in range(5)]
graph[4][3].blocked = True
graph[3][2].blocked = True
graph[3][3].blocked = True
graph[2][2].blocked = True
graph[2][3].blocked = True
graph[1][2].blocked = True


#initialize hValues
for i in range(len(graph)):
    for j in range(len(graph[i])):
        manhattanDist = abs(i - 4) + abs(j - 4)
        graph[i][j].h = manhattanDist
        graph[i][j].g = math.inf
        graph[i][j].x = i
        graph[i][j].y = j


#start algo
curr = graph[4][2]
curr.g = 0
end = graph[4][4]
pq = []
pq.append(curr)
visited = set()

printGraph(graph)

while pq:
    curr = heapq.heappop(pq)
    visited.add(curr)

    if(curr == end):
        break


    #find neighbors and compute g cost
    xOffsets = [1, -1, 0, 0]
    yOffsets = [0, 0, 1, -1]
    for i in range(4):
        x = curr.x + xOffsets[i]
        y = curr.y + yOffsets[i]

        if x >= 0 and x < 5 and y >= 0 and y < 5 and not graph[x][y].blocked and not graph[x][y] in visited:
            neighbor = graph[x][y]
            if neighbor in pq:
                # figure out if you need to update the f score
                newG = curr.g + 1
                if (newG) < (neighbor.g):
                    neighbor.g = newG
                    neighbor.prev = curr
                    heapq.heapify(pq)
            else:
                neighbor.g = curr.g + 1
                neighbor.prev = curr
                heapq.heappush(pq, neighbor)

path = []
while(curr.prev):
    path.append((curr.x, curr.y))
    curr = curr.prev

print(path)

        


