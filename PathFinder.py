import math
from Graph import Graph
from Algorithms import selectRandomNode, repeatedForwardsAlgo, repeatedBackwardsAlgo, testAStar, setHValues, printBlocked

class PathFinder:

    def __init__(self):
        self.graph = Graph(101,101)
        self.start = selectRandomNode(self.graph)
        self.goal = selectRandomNode(self.graph)

    def repeatedForward(self):
        repeatedForwardsAlgo(self.graph, self.start, self.goal)
    
    def repeatedBackward(self):
        repeatedBackwardsAlgo(self.graph, self.start, self.goal)


#testing, first find the true shortest path using singular test A*
path = PathFinder()
setHValues(path.graph.graph, path.goal)
path.start.g = 0
path.start.search = 1
path.goal.search = 1
path.goal.g = math.inf
a = testAStar(path.graph.graph, path.goal, [path.start], set(), 1, path.start)
print(len(a))
print(a)
printBlocked(a, path.graph.graph)
print('\n')

#next test repeated forwards
path.graph.resetNodes
path.repeatedForward()

#lastly test repeated backwards
print('\n')
path.graph.resetNodes()
path.repeatedBackward()



