from Graph import Graph
from Algorithms import selectRandomNode, repeatedForwardsAlgo, repeatedBackwardsAlgo, adaptiveAlgorithm
import math

class PathFinder:

    def __init__(self):
        self.graph = Graph(101,101)
        self.start = selectRandomNode(self.graph)
        self.goal = selectRandomNode(self.graph)

    def repeatedForward(self):
        repeatedForwardsAlgo(self.graph, self.start, self.goal)
    
    def repeatedBackward(self):
        repeatedBackwardsAlgo(self.graph, self.start, self.goal)

    def adaptiveAlgorithm(self):
        adaptiveAlgorithm(self.graph, self.start, self.goal)



