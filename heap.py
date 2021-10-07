from setUp import Node
import heapq

node1 = Node()
node2 = Node()
node3 = Node()

node1.g = 2
node1.h = 2

node2.g = 10
node2.h = 11

node3.g = 5
node3.h = 7

nodes = [node1, node2, node3]
heapq.heapify(nodes)

while nodes:
    print(heapq.heappop(nodes))
