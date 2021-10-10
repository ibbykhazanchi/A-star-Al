from Graph import Graph
from Algorithms import selectRandomNode, repeatedAlgo

class PathFinder:

    def __init__(self):
        self.graph = Graph(101,101)
        self.start = selectRandomNode(self.graph)
        self.goal = selectRandomNode(self.graph)

    def repeatedForward(self):
        repeatedAlgo(self.graph, self.start, self.goal)
    
    def repeatedBackward(self):
        repeatedAlgo(self.graph, self.goal, self.start)





