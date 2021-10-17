from Graph import Graph
from Algorithms import selectRandomNode, repeatedForwardsAlgo, repeatedBackwardsAlgo, adaptiveAlgo, setHValues
import math

class PathFinder:

    def __init__(self):
        self.graph = Graph(101,101)
        self.start = selectRandomNode(self.graph)
        self.goal = selectRandomNode(self.graph)
    
    '''''
    def __init__(self, graph):
       self.graph = graph
       self.start = selectRandomNode(self.graph)
       self.goal = selectRandomNode(self.graph)
    '''''
    
    def setHeuristics(self):
        setHValues(self.graph.graph, self.goal)

    def repeatedForward(self):
        return repeatedForwardsAlgo(self.graph, self.start, self.goal)
    
    def repeatedBackward(self):
        return repeatedBackwardsAlgo(self.graph, self.start, self.goal)

    def adaptiveAlgorithm(self):
        return adaptiveAlgo(self.graph, self.start, self.goal)



