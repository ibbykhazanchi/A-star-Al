from PathFinder import PathFinder
from Algorithms import testAStar, setHValues, printBlocked
import math


path = PathFinder()
path.repeatedForward()


print('\n')
path.graph.resetNodes()
path.repeatedBackward()
print('\n')
path.adaptiveAlgorithm()
