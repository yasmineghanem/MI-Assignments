from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented
import math

# TODO: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state)

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.


def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)

    terminal, values = game.is_terminal(state)
    if terminal:
        return values[agent], None

    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action)
                           for index, (action, state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].


def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: Complete this function
    agent = game.get_turn(state)

    terminal, values = game.is_terminal(state)
    if terminal:
        return values[0], None
    if max_depth == 0:
        return heuristic(game, state, 0), None
    
    actions = game.get_actions(state)

    if agent == 0:
        max_value = -math.inf
        max_action = None
        for action in actions:
            successor_state = game.get_successor(state, action)
            value, _ = minimax(game, successor_state, heuristic, max_depth-1)

            if value > max_value: max_value = value; max_action = action
        return max_value, max_action
    else:
        min_value = math.inf
        min_action = None
        for action in actions:
            successor_state = game.get_successor(state, action)
            value, _ = minimax(game, successor_state, heuristic, max_depth-1)

            if value < min_value: min_value = value; min_action = action
        return min_value, min_action

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.

def minmax_alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth : int, alpha : float, beta : float):
    
    agent = game.get_turn(state)

    terminal, values = game.is_terminal(state)
    if terminal:
        return values[0], None
    if max_depth == 0:
        return heuristic(game, state, 0), None
    
    actions = game.get_actions(state)

    if agent == 0:
        max_value = -math.inf
        max_action = None
        for action in actions:
            successor_state = game.get_successor(state, action)
            value, _ = minmax_alphabeta(game, successor_state, heuristic, max_depth-1, alpha, beta)

            if value > max_value: max_value = value; max_action = action
            
            if max_value >= beta:
                return max_value, max_action
            
            alpha = max(alpha, max_value)

        return max_value, max_action
    else:
        min_value = math.inf
        min_action = None
        for action in actions:
            successor_state = game.get_successor(state, action)
            value, _ = minmax_alphabeta(game, successor_state, heuristic, max_depth-1, alpha, beta)

            if value < min_value: min_value = value; min_action = action

            if min_value <= alpha:
                return min_value, min_action
            
            beta = min(beta, min_value)
            
        return min_value, min_action



def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: Complete this function
    # initialize alpha and beta
    alpha = -math.inf
    beta = math.inf
    return minmax_alphabeta(game, state, heuristic, max_depth, alpha, beta)


# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.

def minmax_alphabeta_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth : int, alpha : float, beta : float):
    
    agent = game.get_turn(state)

    terminal, values = game.is_terminal(state)
    if terminal:
        return values[0], None
    if max_depth == 0:
        return heuristic(game, state, 0), None
    
    states_actions = [(game.get_successor(state, action), action) for action in game.get_actions(state)]
    states_actions.sort(key=lambda state_action: heuristic(game, state_action[0], agent), reverse=True)

    if agent == 0:
        max_value = -math.inf
        max_action = None
        for state_action in states_actions:
            action = state_action[1]
            successor_state = state_action[0]
            value, _ = minmax_alphabeta_ordering(game, successor_state, heuristic, max_depth-1, alpha, beta)

            if value > max_value: max_value = value; max_action = action
            
            if max_value >= beta:
                return max_value, max_action
            
            alpha = max(alpha, max_value)

        return max_value, max_action
    else:
        min_value = math.inf
        min_action = None
        for state_action in states_actions:
            action = state_action[1]
            successor_state = state_action[0]
            value, _ = minmax_alphabeta_ordering(game, successor_state, heuristic, max_depth-1, alpha, beta)

            if value < min_value: min_value = value; min_action = action

            if min_value <= alpha:
                return min_value, min_action
            
            beta = min(beta, min_value)
            
        return min_value, min_action 

def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: Complete this function
    alpha = -math.inf
    beta = math.inf
    return minmax_alphabeta_ordering(game, state, heuristic, max_depth, alpha, beta)

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).


def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: Complete this function
    agent = game.get_turn(state)

    terminal, values = game.is_terminal(state)
    if terminal:
        return values[0], None
    if max_depth == 0:
        return heuristic(game, state, 0), None

    if agent == 0:
        actions = game.get_actions(state)
        max_value = -math.inf
        max_action = None
        for action in actions:
            successor_state = game.get_successor(state, action)
            value, _ = expectimax(game, successor_state, heuristic, max_depth-1)

            if value > max_value: max_value = value; max_action = action
        return max_value, max_action
    else:
        actions = game.get_actions(state)
        min_value = 0
        for action in actions:
            successor_state = game.get_successor(state, action)
            value, _ = expectimax(game, successor_state, heuristic, max_depth-1)

            min_value += value
        min_value = min_value / len(actions)
        return min_value, None
