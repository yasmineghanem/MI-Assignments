from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented
import math

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #TODO: Complete this function

        # value is always 0 for any terminal state
        if self.mdp.is_terminal(state):
            return 0
        
        actions = self.mdp.get_actions(state) # get all mdp possible actions

        maximum_utility = -math.inf # initialize maximum utility

        for action in actions: # loop on all actions 
            successors = self.mdp.get_successor(state, action) # get the successors after applying the current action to the current state
            
            utility_sum = 0
            for successor in successors: # loop on all successors to compute the utility summation for the action applied 
                successor_utility = self.utilities[successor]
                current_reward = self.mdp.get_reward(state, action, successor) # the reward of the current state 
                utility = successors[successor] * (current_reward + self.discount_factor * successor_utility) # update using the value iteration equation

                utility_sum += utility

            if utility_sum > maximum_utility: # update the maximum utility
                maximum_utility = utility_sum
        
        return maximum_utility
    
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        #TODO: Complete this function

        updated_utilities = {} # empty dictionary to fill with the updated utilities 

        maximum_utility_change = -math.inf # initialize maximum utility

        states = self.mdp.get_states() # get all possible states of the MDP

        for state in states: # loop on all states
            computed_utility = self.compute_bellman(state) # compute the bellman utility
            updated_utilities[state] = computed_utility # update the utility of the current state with the utility computed from the bellman equation
            if abs(self.utilities[state] - computed_utility) > maximum_utility_change: # if the change in both utilities is greater than the maximum utility change 
                maximum_utility_change = abs(self.utilities[state] - computed_utility) # update the maximum utility
        
        self.utilities = updated_utilities # update the problem's utility with the updated bellman utilities
        
        if maximum_utility_change > tolerance:
            return False
        return True
    
    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        #TODO: Complete this function to apply value iteration for the given number of iterations
        iteration = 0
        while iterations == 0 or iteration < iterations: # loop on all iterations (if iterations is 0) then we update once
            iteration += 1
            if self.update(tolerance): # check if tolerance is greater the the maximum utility change after the update
                break

        return iteration # return the value the iteration when the tolerance is greater than the maximum utility
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function

        # if the state is terminal then no action should be taken
        if self.mdp.is_terminal(state):
            return None
        
        actions = env.actions() # get all possible environment actions

        maximum_utility = -math.inf # initialize maximum utility

        optimal_action = None # the action with the maximum utility 

        for action in actions: # loop on all actions
            successors = self.mdp.get_successor(state, action) # get all state's successors 
            
            utility_sum = 0
            for successor in successors:
                successor_utility = self.utilities[successor]
                current_reward = self.mdp.get_reward(state, action, successor) # get the reward for the current action and the successor state
                utility = successors[successor] * (current_reward + self.discount_factor * successor_utility) # compute using the value iteration equantion

                utility_sum += utility

            if utility_sum > maximum_utility: # update the maximum utility
                maximum_utility = utility_sum
                optimal_action = action 
        
        return optimal_action 
    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
