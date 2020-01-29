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
    return [s, s, w, s, w, w, s, w]


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
    frontier = util.Stack()
    parents = {}
    explored = []

    frontier.push(problem.getStartState())
    # For the parents dict: False if the item not in explored
    # Store parents of the nodes along with the action
    parents[problem.getStartState()] = [0, 0, False]

    while not frontier.isEmpty():
        curr_state = frontier.pop()  # extract the node from the frontier
        if problem.isGoalState(curr_state):
            result = []  # create the list to store the result
            # backtrace the route from the startingstate to the goal state

            result.insert(0, parents[curr_state][1])
            # set the parent of the node as the current element
            element = parents[curr_state][0]

            while (element != problem.getStartState()):
                # insert it at the start of the list
                result.insert(0, parents[element][1])
                # replace the current element with it's parent
                element = parents[element][0]
            return result

        # add the current state to the explored set
        explored.append(curr_state)
        parents[curr_state][2] = True  # Set it as explored

        for child in problem.getSuccessors(curr_state):
            state = child[0]
            if state not in parents:  # which translates to: neither in frontier nor in explored
                frontier.push(state)  # push it to the frontier
                # set its information in the dict
                parents[state] = [curr_state, child[1], False]


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    explored = []
    parents = {}

    frontier.push(problem.getStartState())
    # format: (parent_state, action, Bool_isExplored)
    parents[problem.getStartState()] = [0, 0, False]

    # need to check if the starting node is also the goal node
    if problem.isGoalState(problem.getStartState()):
        return []

    while not frontier.isEmpty():
        curr_state = frontier.pop()

        explored.append(curr_state)
        parents[curr_state][2] = True

        for child in problem.getSuccessors(curr_state):
            if child[0] not in parents:  # neither in explored nor in frontier
                if problem.isGoalState(child[0]):
                    result = []

                    result.insert(0, child[1])
                    element = curr_state  # parent of the child

                    while (element != problem.getStartState()):
                        # insert the action at the start
                        result.insert(0, parents[element][1])
                        # set element as the parent of the curr element
                        element = parents[element][0]
                    return result

                frontier.push(child[0])  # push child state in the frontier
                # add its info to the dict
                parents[child[0]] = [curr_state, child[1], False]

    return None


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    explored = []
    parents = {}

    frontier.push(problem.getStartState(), 0)
    "Node: [Parent, Action, CostOfPath, True] True if in explored"
    parents[problem.getStartState()] = [0, 0, 0, False]

    while not frontier.isEmpty():
        curr_state = frontier.pop()

        if problem.isGoalState(curr_state):
            result = []
            parent = parents[curr_state][0]
            result.insert(0, parents[curr_state][1])

            while parent != problem.getStartState():
                temp = parents[parent][0]
                result.insert(0, parents[parent][1])
                parent = temp
            return result

        explored.append(curr_state)
        "Update dictionary value to true for expanded"
        parents[curr_state][3] = True
        for child in problem.getSuccessors(curr_state):
            child_pathcost = parents[curr_state][2]+child[2]
            if child[0] not in parents:  # neither in frontier nor in explored
                frontier.push(child[0], child_pathcost)
                parents[child[0]] = [curr_state,
                                     child[1], child_pathcost, False]
            elif child[0] in parents and parents[child[0]][3] is False:  # if in frontier
                # if the cost of the node already in frontier is bigger
                if parents[child[0]][2] > child_pathcost and parents[child[0]][3] is False:
                    # update it with the new cost
                    frontier.update(child[0], child_pathcost)
                    # update parents dict
                    parents[child[0]] = [curr_state,
                                         child[1], child_pathcost, False]
    return None


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    explored = []
    parents = {}

    frontier.push(problem.getStartState(), 0)
    "Node: [Parent, Action, CostOfPath, True] True if in explored"
    parents[problem.getStartState()] = [0, 0, 0, False]

    while not frontier.isEmpty():
        curr_state = frontier.pop()

        if problem.isGoalState(curr_state):
            result = []
            parent = parents[curr_state][0]
            result.insert(0, parents[curr_state][1])

            while parent != problem.getStartState():
                temp = parents[parent][0]
                result.insert(0, parents[parent][1])
                parent = temp

            return result

        explored.append(curr_state)  # add to the explored
        "Update dictionary value to true for expanded"
        parents[curr_state][3] = True
        for child in problem.getSuccessors(curr_state):
            child_pathcost = parents[curr_state][2]+child[2]
            if child[0] not in [node[2] for node in frontier.heap] and child[0] not in explored:
                frontier.push(child[0], child_pathcost +
                              heuristic(child[0], problem))
                parents[child[0]] = [curr_state,
                                     child[1], child_pathcost, False]
            elif child[0] in [node[2] for node in frontier.heap]:
                # if the cost of the node already in frontier is bigger
                if parents[child[0]][2] > child_pathcost and parents[child[0]][3] is False:
                    # update frontier node with the new cost
                    frontier.update(
                        child[0], child_pathcost + heuristic(child[0], problem))
                    # update the dict entries
                    parents[child[0]] = [curr_state,
                                         child[1], child_pathcost, False]
    return None


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
