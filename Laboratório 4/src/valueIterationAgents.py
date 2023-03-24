# valueIterationAgents.py
# -----------------------
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


import util
from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take a mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0

        # Write value iteration code here
        # > Os valores iniciais dos estados são zero, considerando o comportamento da classe Counter em relação a
        # valores não inicializados.
        # > O estado (0, 0) é o inferior esquerdo. (x=0, y=0)
        # > O método mdp.getReward() não utiliza os parâmetros 'action' e 'nextState', ou seja, ele apenas retorna a
        # recompensa por estar no estado 'state'.
        # > O cálculo dos valores da iteração 'k' utiliza uma cópia dos valores da iteração 'k-1' para que os valores
        # calculados na iteração 'k' não sejam interiram no processo.

        # > O estado 'TERMINAL_STATE' é utilizado internamente nos estados de saída (os terminais), então pode ser
        # removido da lista de estados que serão analisados.
        states: list = mdp.getStates()
        states.remove('TERMINAL_STATE')

        for i in range(iterations):
            values = util.Counter()

            for state in states:
                state_reward = mdp.getReward(state, None, None)
                actions: list = mdp.getPossibleActions(state)

                actions_values = [self.computeValues(state, action) for action in actions]
                best_action_value = max(actions_values)
                values[state] = state_reward + discount * best_action_value

            self.values = values

    def computeValues(self, state, action):
        transitions: list = self.mdp.getTransitionStatesAndProbs(state, action)
        transitions_values = []

        for next_state, prob in transitions:
            next_state_value = self.values[next_state]
            transitions_values.append(next_state_value * prob)

        return sum(transitions_values)

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        state_reward = self.mdp.getReward(state, None, None)
        transitions: list = self.mdp.getTransitionStatesAndProbs(state, action)
        transitions_values = []

        for next_state, prob in transitions:
            next_state_value = self.values[next_state]
            transitions_values.append(next_state_value * prob * self.discount)

        return state_reward + sum(transitions_values)

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        actions: list = self.mdp.getPossibleActions(state)
        if len(actions) == 0:
            return None

        options = []
        for action in actions:
            options.append((action, self.computeValues(state, action)))

        best_action, _ = max(options, key=lambda x: x[1])
        return best_action


def getPolicy(self, state):
    return self.computeActionFromValues(state)


def getAction(self, state):
    """Returns the policy at the state (no exploration)."""
    return self.computeActionFromValues(state)


def getQValue(self, state, action):
    return self.computeQValueFromValues(state, action)
