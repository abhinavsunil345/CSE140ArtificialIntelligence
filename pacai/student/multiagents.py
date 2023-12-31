import random
from pacai.core.distance import manhattan
from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core.directions import Directions

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        legalMoves = gameState.getLegalActions()

        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPosition = successorGameState.getPacmanPosition()
        closestghost = 999999
        closestfood = 9999999
        for ghost in successorGameState.getGhostPositions():
            x = manhattan(newPosition, ghost)
            if (closestghost > x):
                closestghost = x
        for food in currentGameState.getFood().asList():
            y = manhattan(newPosition, food)
            if (closestfood > y):
                closestfood = y
        if (closestfood == 0):
            closestfood = 0.0001
        if closestghost <= 2:
            evaluationScore = -99999999
        else:
            evaluationScore = (1 / closestfood) - (1 / (closestghost))
        # Useful information you can extract.
        # newPosition = successorGameState.getPacmanPosition()
        # oldFood = currentGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***
        return evaluationScore

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def getAction(self, state):
        """
        The BaseAgent will receive an `pacai.core.gamestate.AbstractGameState`,
        and must return an action from `pacai.core.directions.Directions`.
        """
        legalMoves = state.getLegalActions()
        if not legalMoves:
            return Directions.STOP
        turn = 0
        agents = state.getNumAgents()
        bestScore = float('-inf')
        bestAction = Directions.STOP
        for action in legalMoves:
            if action == Directions.STOP:
                continue
            su = state.generatePacmanSuccessor(action)
            score = self.minimax(su, (turn + 1) % agents, self.getTreeDepth() - 1)
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction

    def minimax(self, state, turn, depth):
        if state.isWin() or state.isLose() or depth == 0:
            return self.getEvaluationFunction()(state)
        if (turn == 0):
            depth -= 1
            return self.maxValue(state, turn, depth)
        else:
            return self.minValue(state, turn, depth)

    def maxValue(self, state, turn, depth):
        if state.isWin() or state.isLose() or depth == 0:
            return self.getEvaluationFunction()(state)
        score = float('-inf')
        legalMoves = state.getLegalActions(turn)
        for action in legalMoves:
            if action == Directions.STOP:
                continue
            su = state.generatePacmanSuccessor(action)
            score = max(score, self.minimax(su, (turn + 1) % state.getNumAgents(), depth))
        return score

    def minValue(self, state, turn, depth):
        if state.isWin() or state.isLose() or depth == 0:
            return self.getEvaluationFunction()(state)
        score = float('inf')
        legalMoves = state.getLegalActions(turn)
        for action in legalMoves:
            if action == Directions.STOP:
                continue
            su = state.generateSuccessor(turn, action)
            score = min(score, self.minimax(su, (turn + 1) % state.getNumAgents(), depth))
        return score

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def getAction(self, state):
        """
        The BaseAgent will receive an `pacai.core.gamestate.AbstractGameState`,
        and must return an action from `pacai.core.directions.Directions`.
        """
        legalMoves = state.getLegalActions()

        if not legalMoves:
            return Directions.STOP

        turn = 0
        agents = state.getNumAgents()
        alpha = float('-inf')
        beta = float('inf')
        bestScore = float('-inf')
        bestAction = Directions.STOP

        for action in legalMoves:
            if action == Directions.STOP:
                continue
            su = state.generatePacmanSuccessor(action)
            score = self.minimax(su, (turn + 1) % agents, self.getTreeDepth() - 1, alpha, beta)
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction

    def minimax(self, state, turn, depth, alpha, beta):
        if state.isWin() or state.isLose() or depth == 0:
            return self.getEvaluationFunction()(state)
        if (turn == 0):
            depth -= 1
            return self.maxValue(state, turn, depth, alpha, beta)
        else:
            return self.minValue(state, turn, depth, alpha, beta)

    def maxValue(self, state, turn, depth, alpha, beta):
        if state.isWin() or state.isLose() or depth == 0:
            return self.getEvaluationFunction()(state)
        score = float('-inf')
        legalMoves = state.getLegalActions(turn)
        for action in legalMoves:
            if action == Directions.STOP:
                continue
            su = state.generatePacmanSuccessor(action)
            score = max(score, self.minimax(su, (turn
            + 1) % state.getNumAgents(), depth, alpha, beta))
            if score >= beta:
                return score
            if score > alpha:
                alpha = score
        return score

    def minValue(self, state, turn, depth, alpha, beta):
        if state.isWin() or state.isLose() or depth == 0:
            return self.getEvaluationFunction()(state)
        score = float('inf')
        legalMoves = state.getLegalActions(turn)
        for action in legalMoves:
            if action == Directions.STOP:
                continue
            su = state.generateSuccessor(turn, action)
            score = min(score, self.minimax(su, (turn
            + 1) % state.getNumAgents(), depth, alpha, beta))
            if score <= alpha:
                return score
            if score < beta:
                beta = score
        return score

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """
    def getAction(self, state):
        """
        The BaseAgent will receive an `pacai.core.gamestate.AbstractGameState`,
        and must return an action from `pacai.core.directions.Directions`.
        """
        legalMoves = state.getLegalActions()
        if not legalMoves:
            return Directions.STOP
        turn = 0
        agents = state.getNumAgents()
        bestScore = float('-inf')
        bestAction = Directions.STOP
        for action in legalMoves:
            if action == Directions.STOP:
                continue
            su = state.generatePacmanSuccessor(action)
            score = self.expmax(su, (turn + 1) % agents, self.getTreeDepth() - 1)
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction

    def expmax(self, state, turn, depth):
        if state.isWin() or state.isLose() or depth == 0:
            return self.getEvaluationFunction()(state)
        if (turn == 0):
            depth -= 1
            return self.maxValue(state, turn, depth)
        else:
            return self.expValue(state, turn, depth)

    def maxValue(self, state, turn, depth):
        if state.isWin() or state.isLose() or depth == 0:
            return self.getEvaluationFunction()(state)
        score = float('-inf')
        legalMoves = state.getLegalActions(turn)
        for action in legalMoves:
            if action == Directions.STOP:
                continue
            su = state.generatePacmanSuccessor(action)
            score = max(score, self.expmax(su, (turn
            + 1) % state.getNumAgents(), depth))
        return score

    def expValue(self, state, turn, depth):
        if state.isWin() or state.isLose() or depth == 0:
            return self.getEvaluationFunction()(state)
        score = 0
        legalMoves = state.getLegalActions(turn)
        for action in legalMoves:
            if action == Directions.STOP:
                continue
            su = state.generateSuccessor(turn, action)
            prob = 1.0 / len(legalMoves)
            score += prob * self.expmax(su, (turn + 1) % state.getNumAgents(), depth)
        return score

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """
    newPosition = currentGameState.getPacmanPosition()
    closestscaredghost = float('inf')
    closestfood = float('inf')
    closestghost = float('inf')
    score = currentGameState.getScore()
    remainingFood = currentGameState.getNumFood()
    for ghostState in currentGameState.getGhostStates():
        ghostPosition = ghostState.getPosition()
        x = manhattan(newPosition, ghostPosition)
        if ghostState.getScaredTimer() > 0:
            if x < closestscaredghost:
                closestscaredghost = x
        elif x < closestghost:
            closestghost = x
    for food in currentGameState.getFood().asList():
        y = manhattan(newPosition, food)
        if (closestfood > y):
            closestfood = y
        if currentGameState.getFood()[food[0]][food[1]]:
            remainingFood -= 1
    if (closestfood == 0):
        closestfood = 0.0001
    if closestghost <= 1.5:
        evaluationScore = float('-inf')
    else:
        evaluationScore = (1.5 * score) + (1.0 / closestfood) - (1.0
        / closestghost) - (1.1 / (remainingFood + 0.01))
        if closestscaredghost < 5:
            evaluationScore += 100 / closestscaredghost
    return evaluationScore

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction
    """
    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
