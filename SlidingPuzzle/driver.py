import sys

import math

from OrderedSet import OrderedSet
from enum import Enum

# determine algo to use
algo = sys.argv[1]
initial_state = sys.argv[2]

print ("algo and initial state are", algo, initial_state)


class Action(Enum):
    UP,DOWN,LEFT,RIGHT = range(4)

class Node:
    Problem = []
    Parent = None
    Action = None
    PathCost = None
    ZeroIndex = 0

    def __eq__(self, other):
        return self.Problem.__eq__(other.Problem)

    def __hash__(self):
        return hash((str(self.Problem)))

    def __str__(self):
        return str(self.Problem)

def is_goal(node):
    for idx, val in enumerate(node.Problem):
        if(idx != int(val)): return False
    return True

def gen_actions(zeroIndex, index_step, index_max):
    actions = []
    if(zeroIndex - index_step >=0): actions.append(Action.UP)
    if(zeroIndex + index_step < index_max): actions.append(Action.DOWN)
    if(zeroIndex % index_step != 0 & zeroIndex - 1 >=0): actions.append(Action.LEFT)
    if(zeroIndex % index_step == 0 & zeroIndex + 1 < index_max): actions.append(Action.RIGHT)

    # print ("gen actions for node ", node.Problem, actions)
    return actions


def apply(action, parent):
    # print("applying action to ", action, parent.Problem)
    problem = list(parent.Problem)
    zeroIndex = parent.ZeroIndex
    if(action == Action.UP):
        problem[parent.ZeroIndex], problem[parent.ZeroIndex -index_step] = problem[parent.ZeroIndex - index_step], problem[parent.ZeroIndex]
        zeroIndex = zeroIndex - index_step
    elif(action == Action.DOWN):
        problem[parent.ZeroIndex], problem[parent.ZeroIndex +index_step] = problem[parent.ZeroIndex + index_step], problem[parent.ZeroIndex]
        zeroIndex = zeroIndex + index_step
    elif(action == Action.LEFT):
        problem[parent.ZeroIndex], problem[parent.ZeroIndex -1] = problem[parent.ZeroIndex -1], problem[parent.ZeroIndex]
        zeroIndex = zeroIndex -1
    elif(action == Action.RIGHT):
        problem[parent.ZeroIndex], problem[parent.ZeroIndex +1] = problem[parent.ZeroIndex + 1], problem[parent.ZeroIndex]
        zeroIndex = zeroIndex + 1
    return problem, zeroIndex


def find_child(parent, action):
    child = Node()
    child.Problem, child.ZeroIndex = apply(action, parent)
    child.Parent = parent
    child.Action = action
    child.PathCost = parent.PathCost + 1
    return child


def bfs(initialNode):
    if(is_goal(initialNode)):
        return initialNode

    frontier = OrderedSet()
    explored = OrderedSet()

    frontier.add(initialNode)

    while(frontier.__len__() != 0):
        node = frontier.pop(last = False)
        explored.add(node)
        print("adding to explored", node.Problem, node.Action, node.Parent)
        for action in gen_actions(node.ZeroIndex, index_step, index_max):
            child = find_child(node, action)
            if frontier.__contains__(child) == False | explored.__contains__(child) == False:
                if(is_goal(child)):
                    print("found solution", child)
                    return child
                frontier.add(child)
                print("adding to frontier", child.Problem, child.Action, child.Parent)


initial_node = Node()
initial_node.Problem = initial_state.split(",")
index_max = initial_node.Problem.__len__()
index_step = int(math.sqrt(initial_node.Problem.__len__()))
initial_node.PathCost = 1
initial_node.ZeroIndex = initial_node.Problem.index("0")
solution = bfs(initial_node)
print("solution is ", solution)