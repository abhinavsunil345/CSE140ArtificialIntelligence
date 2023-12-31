from pacai.agents.capture.capture import CaptureAgent

import random

from pacai.core.directions import Directions

import logging
import random
import time

from pacai.util import util

class DummyAgent(CaptureAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at `pacai.core.baselineTeam` for more details about how to create an agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the agent and populates useful fields,
        such as the team the agent is on and the `pacai.core.distanceCalculator.Distancer`.

        IMPORTANT: If this method runs for more than 15 seconds, your agent will time out.
        """

        super().registerInitialState(gameState)

        # Your initialization code goes here, if you need any.

    def chooseAction(self, gameState):
        """
        Randomly pick an action.
        """

        actions = gameState.getLegalActions(self.index)
        return random.choice(actions)
        



class OffensiveReflexAgent(CaptureAgent):
    """
    A reflex agent that seeks food.
    This agent will give you an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """
    
    
    def __init__(self, index, **kwargs):
        super().__init__(index)
        self.Qvals = {}
        self.alpha = 0.3  # Learning rate
        self.gamma = 0.8  # Discount factor
          
    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest return from `ReflexCaptureAgent.evaluate`.
        """
        
        enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        friends = [gameState.getAgentState(i) for i in self.getTeam(gameState)]
        invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]
        invadees = [a for a in friends if a.isPacman() and a.getPosition() is not None]
        score = self.getScore(gameState)
        mindist = 9999
        if (len(invaders) > 0):
            myPos = gameState.getAgentState(self.index).getPosition()
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            mindist = min(dists)
        
        if (((len(invaders) == 0) or (len(invadees) > 0)) and (score < 7 or (len(invadees) > 0))):
            actions = gameState.getLegalActions(self.index)
            if "Stop" in actions:
                actions.remove("Stop")

            start = time.time()
            values = [self.evaluate(gameState, a) for a in actions]
            logging.debug('evaluate() time for agent %d: %.4f' % (self.index, time.time() - start))
            
            

            maxValue = max(values)
            bestActions = [a for a, v in zip(actions, values) if v == maxValue]
            

           # print(actions)
           # print(values)
            return random.choice(bestActions)
        else:
            actions = gameState.getLegalActions(self.index)

            start = time.time()
            values = [self.evaluate1(gameState, a) for a in actions]
            logging.debug('evaluate() time for agent %d: %.4f' % (self.index, time.time() - start))

            maxValue = max(values)
            bestActions = [a for a, v in zip(actions, values) if v == maxValue]
            action = random.choice(bestActions)
            
            #features = self.getFeatures(gameState, action)
            # distanceinvader = features.get('invaderDistance', 99)
            # print(distanceinvader)
            # if 'invaderDistance' in features and features['invaderDistance'] <= 1:
                # print('Stop')
                # return 'Stop'
                # print('????')
            
            return action
        
        
    def getSuccessor(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """

        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()

        if (pos != util.nearestPoint(pos)):
            # Only half a grid position was covered.
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights.
        """
        
        
        features = self.getFeatures(gameState, action)
        distancecapsule = features.get('distanceToCapsule', 0)
        distanceghost = features.get('distanceToGhost', 0)
        distancescared = features.get('scared', 0)
        distancefood = features.get('distanceToFood', 0)
        distancefriend = features.get('friendDistance', 0)
        succScore = features.get('successorScore', 0)
        oscil = features.get('oscilate', 0)
        stateEval = 152 * succScore + -9 * distancefood + (8 * distanceghost * distancescared) + -4 * distancecapsule + 1 * distancefriend + -30 * oscil
            

        return stateEval

    def getFeatures(self, gameState, action):
        features = {}
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)
       # print('score')
       # print(self.getScore(successor))

        # Compute distance to the nearest food.
        foodList = self.getFood(successor).asList()
        
        CapsuleList = self.getCapsules(successor)
        CapsuleList1 = self.getCapsules(gameState)

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance
            
            
            
        if (len(CapsuleList) > 0):
        #    print('Capsules')
        #    print(len(CapsuleList))
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, capsule) for capsule in CapsuleList])
            #print('min')
            #print(minDistance)
            features['distanceToCapsule'] = minDistance
            
            
        elif (len(CapsuleList1) > 0):
            features['distanceToCapsule'] = -999
            
        opponents = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        ghosts = [opponent for opponent in opponents if opponent.getPosition() is not None and not opponent.isPacman()]
        
        if len(ghosts) > 0:
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, ghost.getPosition()) for ghost in ghosts])
         #   print('GhostDist')
         #   print(minDistance)
            if minDistance > 22:
                features['distanceToGhost'] = 0
            else:   
                features['distanceToGhost'] = minDistance
            
            
            
        friends = [gameState.getAgentState(i) for i in self.getTeam(gameState)]
        friendlyghosts = [a for a in friends if a.isGhost() and a.getPosition() is not None]
        friendlypacman = [a for a in friends if a.isPacman() and a.getPosition() is not None]
        
        if (len(friendlyghosts) > 0):
            dists = max([self.getMazeDistance(myPos, a.getPosition()) for a in friendlyghosts])
            if dists > 22:
                features['friendDistance'] = 0
            else:   
                features['friendDistance'] = dists
            
            
        for ghost in ghosts:
            if ghost.getScaredTimer() > 0:
                features['scared'] = 0
                features['ateCapsule'] = 1
            else:
                features['scared'] = 1
                features['ateCapsule'] = 0
        if (len(friendlypacman) > 0):
            prevState = self.getPreviousObservation()
            nextPos = successor.getAgentState(self.index).getPosition()
            prevPos = prevState.getAgentState(self.index).getPosition()
            if prevPos == nextPos:
                features['oscilate'] = 1
        else:
            features['oscilate'] = 0
        

        return features
        
        
    def getSuccessor1(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """

        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()

        if (pos != util.nearestPoint(pos)):
            # Only half a grid position was covered.
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def evaluate1(self, gameState, action):
        """
        Computes a linear combination of features and feature weights.
        """

        features = self.getFeatures1(gameState, action)
        weights = self.getWeights(gameState, action)
        stateEval = sum(features.get(feature, 0) * weights[feature] for feature in features)

        return stateEval

    def getFeatures1(self, gameState, action):
        features = {}

        successor = self.getSuccessor1(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0).
        features['onDefense'] = 1
        if (myState.isPacman()):
            features['onDefense'] = 0

        # Computes distance to invaders we can see.
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]
        ghosts = [a for a in enemies if a.isGhost() and a.getPosition() is not None]
        features['numInvaders'] = len(invaders)

        if (len(invaders) > 0):
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)
            features['ghostDistance'] = 0
            
        if (len(invaders) == 0):
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in ghosts]
            features['ghostDistance'] = min(dists)

        if (action == Directions.STOP):
            features['stop'] = 1
            

        rev = Directions.REVERSE[gameState.getAgentState(self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1
            
        foodList = self.getFoodYouAreDefending(successor).asList()
        
        CapsuleList = self.getCapsulesYouAreDefending(successor)
        CapsuleList1 = self.getCapsulesYouAreDefending(gameState)

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance
            
            
        if (len(CapsuleList) > 0):
        #    print('Capsules')
        #    print(len(CapsuleList))
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, capsule) for capsule in CapsuleList])
            #print('min')
            #print(minDistance)
            features['distanceToCapsule'] = minDistance

        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistance': -25,
            'ghostDistance': -6,
            'stop': -100,
            'reverse': -2,
            'distanceToFood': -4,
            'distanceToCapsule': -10
        }




class DefensiveReflexAgent(CaptureAgent):
    """
    A reflex agent that tries to keep its side Pacman-free.
    This is to give you an idea of what a defensive agent could be like.
    It is not the best or only way to make such an agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest return from `ReflexCaptureAgent.evaluate`.
        """

        actions = gameState.getLegalActions(self.index)

        start = time.time()
        values = [self.evaluate(gameState, a) for a in actions]
        logging.debug('evaluate() time for agent %d: %.4f' % (self.index, time.time() - start))

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]
        action = random.choice(bestActions)
        
        features = self.getFeatures(gameState, action)
        # distanceinvader = features.get('invaderDistance', 99)
        # print(distanceinvader)
        # if 'invaderDistance' in features and features['invaderDistance'] <= 1:
            # print('Stop')
            # return 'Stop'
            # print('????')
        
        return action

    def getSuccessor(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """

        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()

        if (pos != util.nearestPoint(pos)):
            # Only half a grid position was covered.
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights.
        """

        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        stateEval = sum(features.get(feature, 0) * weights[feature] for feature in features)

        return stateEval

    def getFeatures(self, gameState, action):
        features = {}

        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0).
        features['onDefense'] = 1
        if (myState.isPacman()):
            features['onDefense'] = 0

        # Computes distance to invaders we can see.
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]
        ghosts = [a for a in enemies if a.isGhost() and a.getPosition() is not None]
        features['numInvaders'] = len(invaders)

        if (len(invaders) > 0):
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)
            features['ghostDistance'] = 0
            
        if (len(invaders) == 0):
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in ghosts]
            features['ghostDistance'] = min(dists)

        if (action == Directions.STOP):
            features['stop'] = 1

        rev = Directions.REVERSE[gameState.getAgentState(self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1
            
        foodList = self.getFoodYouAreDefending(successor).asList()
        
        CapsuleList = self.getCapsulesYouAreDefending(successor)
        CapsuleList1 = self.getCapsulesYouAreDefending(gameState)

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance
            
            
        if (len(CapsuleList) > 0):
        #    print('Capsules')
        #    print(len(CapsuleList))
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, capsule) for capsule in CapsuleList])
            #print('min')
            #print(minDistance)
            features['distanceToCapsule'] = minDistance

        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistance': -90,
            'ghostDistance': -12,
            'stop': -100,
            'reverse': -2,
            'distanceToFood': -9,
            'distanceToCapsule': -3
        }

def createTeam(firstIndex, secondIndex, isRed):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    firstAgent = OffensiveReflexAgent
    secondAgent = DefensiveReflexAgent
    turn = 0

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]