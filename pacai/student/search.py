"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """

    # *** Your Code Here ***
    frontier = [(problem.startingState(), [])]
    visited = set()
    while frontier:
        a, b = frontier.pop()
        if (problem.isGoal(a)):
            return b
        if a not in visited:
            visited.add(a)
            for x in problem.successorStates(a):
                if x[0] not in visited:
                    frontier.append((x[0], b + [x[1]]))
    return []
    # raise NotImplementedError()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    frontier = [(problem.startingState(), [])]
    visited = set()
    while frontier:
        a, b = frontier.pop(0)
        if (problem.isGoal(a)):
            return b
        if a not in visited:
            visited.add(a)
            for x in problem.successorStates(a):
                if x[0] not in visited:
                    frontier.append((x[0], b + [x[1]]))
    return []
    # raise NotImplementedError()

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    frontier = [(problem.startingState(), [], 0)]
    visited = set()
    while frontier:
        a, b, c = frontier.pop(0)
        if (problem.isGoal(a)):
            return b
        if a not in visited:
            visited.add(a)
            for x in problem.successorStates(a):
                if x[0] not in visited:
                    frontier.append((x[0], b + [x[1]], c + x[2]))
                    frontier = sorted(frontier, key=lambda x: x[2])
    return []
    # raise NotImplementedError()

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    frontier = [(problem.startingState(), [], 0, 0)]
    visited = set()
    while frontier:
        a, b, c, d = frontier.pop()
        if (problem.isGoal(a)):
            return b
        if a not in visited:
            visited.add(a)
            for x in problem.successorStates(a):
                if x[0] not in visited:
                    frontier.append((x[0], b + [x[1]], d + x[2] + heuristic(x[0], problem),
                    d + x[2]))
                    frontier = sorted(frontier, key=lambda x: x[2], reverse=True)
    return []
    # raise NotImplementedError()
