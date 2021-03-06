# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import searchAgents
finalPath = []

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def dfsHelper(problem, visited, currPath, currState):
    # immidiately return path if we are in the goal state
    if(problem.isGoalState(currState)):
        return currPath[:]
    path = []
    for x in problem.getSuccessors(currState):
        if(x[0] in visited):
            continue
        # append the node to current path before exploring
        # further in the graph
        currPath.append(x[1])
        visited.add(x[0])

        result = dfsHelper(problem, visited, currPath, x[0])
        if (result != []):
            path = result
            break
        # remove the current node from the path
        # so that other children of the current
        # parent may be considered
        currPath.pop()
        visited.remove(x[0])
    return path

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    currState = problem.getStartState()
    visited = set()
    visited.add(currState)
    currPath = []
   
    result = dfsHelper(problem, visited, currPath, currState)

    return result

def bfsHelper(startCoordinate, finalCoordinate, parentDictionary, directionDictionary):
    path = util.Stack()
    while True:
        path.push(directionDictionary[finalCoordinate])
        finalCoordinate = parentDictionary[finalCoordinate]
        if(finalCoordinate == startCoordinate):
            break
    result = []
    while(not path.isEmpty()):
        result.append(path.pop())
    return result

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    currState = problem.getStartState()
    startCoordinate = currState

    frontier = util.Queue()
    frontier.push(currState)

    visited = set()
    visited.add(currState)

    finalCoordinate = (0,0)
    # Dictionary of parent-child coordinate pairs
    # Dictionary of coordinates and the preceding
    # action that was taken to reach it
    parentDictionary = {}
    directionDictionary = {}
    isDone = False

    # Keep exploring while a path has not been found and frontier is not empty
    while(not isDone and not frontier.isEmpty()):

        currState = frontier.pop()
        ## when we find the goal state, set a flag 
        # so the helper function may be called
        if(problem.isGoalState(currState)):
            finalCoordinate = currState
            break
        # for each successor we haven't yet visited,
        # add the coordinates to the parentDictionary
        # so a path can be built.
        for x in problem.getSuccessors(currState):
            if(x[0] not in visited):
                parentDictionary[x[0]] = currState
                directionDictionary[x[0]] = x[1]
                visited.add(x[0])
                frontier.push(x[0])
                
    return bfsHelper(startCoordinate, finalCoordinate, parentDictionary, directionDictionary)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    # holds current state, current path, and 
    # prioritizes based on cost
    frontier = util.PriorityQueue()
    visited = set()
    
    
    frontier.push([problem.getStartState(), []], 0)

    while(not frontier.isEmpty()):
        coor, currPath = frontier.pop()

        # return current path back up recursive tree    
        if problem.isGoalState(coor):
            return currPath
        
        successors = problem.getSuccessors(coor)
        costOfPath = problem.getCostOfActions(currPath)
        for x in successors:
            cost = 0
            skip = False

            # for each successor, compare cost of path to existing
            # cost and see if the cost to explore that way is better
            for y in frontier.heap:
                # do not add the value to the frontier if the
                # state in the priority queue is the same.
                if x[0] == y[2][0]:
                    cost = y[0] - costOfPath
                    skip = True
            if x[0] not in visited and (x[2] < cost or not skip):
                frontier.push([x[0], currPath + [x[1]]], costOfPath + x[2])  
        visited.add(coor)
    return []
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

              
def aStarSearch(problem, heuristic=nullHeuristic):

    frontier = util.PriorityQueue()
    visited = set()
    
    
    frontier.push([problem.getStartState(), []], 0)

    while(not frontier.isEmpty()):
        coor, currPath = frontier.pop()
        
        if problem.isGoalState(coor):
            return currPath
        
        successors = problem.getSuccessors(coor)
        costOfPath = problem.getCostOfActions(currPath)
        # for each successor, compare cost of path to existing
        # cost and see if the cost to explore that way is better
        for x in successors:
            cost = 0
            skip = False
            
            for y in frontier.heap:
                # do not add the value to the frontier if the
                # state in the priority queue is the same.                
                if x[0] == y[2][0]:
                    cost = y[0] - costOfPath - heuristic(coor, problem)
                    skip = True
            if x[0] not in visited and (x[2] < cost or not skip):
                frontier.push([x[0], currPath + [x[1]]], costOfPath + x[2] + heuristic(x[0], problem))  
        visited.add(coor)
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
