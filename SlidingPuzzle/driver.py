import sys
import time
import resource
import math

from OrderedSet import OrderedSet
from enum import Enum

# determine algo to use
algo = sys.argv[1]
initial_state = sys.argv[2]

# print ("algo and initial state are", algo, initial_state)


class Solution:
    pathToGoal = []
    cost = 0
    nodesExpanded = 0
    searchDepth = 0
    maxSearchDepth = 0
    runningTime = 0.0
    maxRamUsage = 0.0

class Action(Enum):
    Up,Down,Left,Right = range(4)

class Node:
    Problem = []
    Parent = None
    Action = None
    PathCost = None
    ZeroIndex = 0
    Depth = 0

    def __eq__(self, other):
        return (other is not None) & self.Problem.__eq__(other.Problem)

    def __hash__(self):
        return hash((str(self.Problem)))

    def __str__(self):
        return str(self.Problem)

final_solution = Solution()

def is_goal(node):
    for idx, val in enumerate(node.Problem):
        if(idx != int(val)): return False
    return True

def gen_actions(zeroIndex, index_step, index_max):
    actions = []
    if(zeroIndex - index_step >=0): actions.append(Action.Up)
    if(zeroIndex + index_step < index_max): actions.append(Action.Down)
    if(zeroIndex % index_step != 0 & zeroIndex - 1 >=0): actions.append(Action.Left)
    if(zeroIndex % index_step == 0 & zeroIndex + 1 < index_max): actions.append(Action.Right)

    # print ("gen actions for node ", node.Problem, actions)
    return actions


def apply(action, parent):
    # print("applying action to ", action, parent.Problem)
    problem = list(parent.Problem)
    zeroIndex = parent.ZeroIndex
    if(action == Action.Up):
        problem[parent.ZeroIndex], problem[parent.ZeroIndex -index_step] = problem[parent.ZeroIndex - index_step], problem[parent.ZeroIndex]
        zeroIndex = zeroIndex - index_step
    elif(action == Action.Down):
        problem[parent.ZeroIndex], problem[parent.ZeroIndex +index_step] = problem[parent.ZeroIndex + index_step], problem[parent.ZeroIndex]
        zeroIndex = zeroIndex + index_step
    elif(action == Action.Left):
        problem[parent.ZeroIndex], problem[parent.ZeroIndex -1] = problem[parent.ZeroIndex -1], problem[parent.ZeroIndex]
        zeroIndex = zeroIndex -1
    elif(action == Action.Right):
        problem[parent.ZeroIndex], problem[parent.ZeroIndex +1] = problem[parent.ZeroIndex + 1], problem[parent.ZeroIndex]
        zeroIndex = zeroIndex + 1
    return problem, zeroIndex


def find_child(parent, action):
    child = Node()
    child.Problem, child.ZeroIndex = apply(action, parent)
    child.Parent = parent
    child.Action = action
    child.PathCost = parent.PathCost + 1
    child.Depth = parent.Depth + 1
    return child


def bfs(initialNode):
    if(is_goal(initialNode)):
        return initialNode

    frontier = OrderedSet()
    explored = OrderedSet()

    frontier.add(initialNode)
    maxSearchDepth = 1
    while(frontier.__len__() != 0):
        node = frontier.pop(last = False)
        explored.add(node)
        final_solution.nodesExpanded = final_solution.nodesExpanded + 1
        # print("adding to explored", node.Problem, node.Action, node.Parent)
        for action in gen_actions(node.ZeroIndex, index_step, index_max):
            child = find_child(node, action)
            if frontier.__contains__(child) == False | explored.__contains__(child) == False:
                if(is_goal(child)):
                    # print("found solution", child)
                    final_solution.searchDepth = child.Depth
                    final_solution.maxSearchDepth = maxSearchDepth
                    return child
                frontier.add(child)
                if(child.Depth > maxSearchDepth):
                    maxSearchDepth = child.Depth
                # print("adding to frontier", child.Problem, child.Action, child.Parent)


start_time = time.time()
initial_node = Node()
initial_node.Problem = initial_state.split(",")
index_max = initial_node.Problem.__len__()
index_step = int(math.sqrt(initial_node.Problem.__len__()))
initial_node.PathCost = 0
initial_node.ZeroIndex = initial_node.Problem.index("0")
solution = bfs(initial_node)

final_solution.cost = solution.PathCost

if(solution is not None):
    cur_node = solution
    while(cur_node.Parent is not None):
        final_solution.pathToGoal.append(cur_node.Action.name)
        cur_node = cur_node.Parent
        
print("path_to_goal:", final_solution.pathToGoal)
print("cost_of_path:", final_solution.cost)
print("nodes_expanded:", final_solution.nodesExpanded)
print("search_depth:", final_solution.searchDepth)
print("max_search_depth:", final_solution.maxSearchDepth)
print("running_time:", time.time() - start_time)
print("memory_usage:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024))