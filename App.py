from Algorithms import setHValues, consistencyTest
from PathFinder import PathFinder
from Graph import Graph, create50graphs

#Question 2
def q2():
    graphs = create50graphs()
    greaterThanValues = []
    lessThanValues = []
    for graph in graphs:
        path = PathFinder(graph)
        gt = path.repeatedForward()
        if gt is not None:
            greaterThanValues.append(gt)

        path.graph.resetNodes()
        path.graph.setGFlags()
        lt = path.repeatedForward()
        if lt is not None:
            lessThanValues.append(lt)

    #calculate and print averages
    greaterThanAverage = sum(greaterThanValues) / len(greaterThanValues)
    lessThanAverage = sum(lessThanValues) / len(lessThanValues)

    print("Greater Than Average Expanded Nodes = {:.2f}".format(greaterThanAverage))
    print("Less Than Average Expanded Nodes = {:.2f}".format(lessThanAverage))

#question3
def q3():
    graphs = create50graphs()
    forwardsValues = []
    backwardsValues = []
    
    for graph in graphs:
        path = PathFinder(graph)
        backwards = path.repeatedBackward()
        if backwards is not None:
            backwardsValues.append(backwards)

        path.graph.resetNodes()
        forwards = path.repeatedForward()
        if forwards is not None:
            forwardsValues.append(forwards)

    #calculate and print averages
    forwardsAverage = sum(forwardsValues) / len(forwardsValues)
    backwardsAverage = sum(backwardsValues) / len(backwardsValues)

    print("Forwards Average Expanded Nodes = {:.2f}".format(forwardsAverage))
    print("Backwards Average Expanded Nodes = {:.2f}".format(backwardsAverage))

def q4():
    pathFinder = PathFinder()
    pathFinder.adaptiveAlgorithm()
    print("running consistency test")
    print(consistencyTest(pathFinder.graph.graph))

def q5():
    graphs = create50graphs()
    forwardValues = []
    adaptiveValues= []

    for graph in graphs:
        path = PathFinder(graph)
        adaptive = path.adaptiveAlgorithm()

        if adaptive is not None:
            adaptiveValues.append(adaptive)
        
        path.graph.resetNodes()
        
        forward = path.repeatedForward()
        if forward is not None:
            forwardValues.append(forward)

    forwardAverage = sum(forwardValues) / 50
    adaptiveAverage = sum(adaptiveValues) / 50

    print("Forwards Average Expanded Nodes = {:.2f}".format(forwardAverage))
    print("Adaptive Average Expanded Nodes = {:.2f}".format(adaptiveAverage))

q5()
