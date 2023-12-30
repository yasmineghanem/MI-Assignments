from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented
from dataclasses import dataclass

# TODO: Import any modules you want to use
import heapq
from queue import PriorityQueue
# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution


def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE

    @dataclass
    class Node:
        state: S
        path: list

    if problem.is_goal(initial_state):
        return []

    # create an initial node with the initial state of the graph
    node = Node(initial_state, [])

    frontier = deque()  # regular queue to add all the nodes to be visited
    frontier.append(node)   # add the initial node to the frontier
    explored = set()    # a set to add all the already visited nodes

    frontier_set = set()

    while frontier:  # while the frontier contains any node

        node = frontier.popleft()   # pop the first node in the queue
        if node.state in frontier_set:
            frontier_set.remove(node.state)
        
        explored.add(node.state)    # add then node to the explored set
        frontier_set.add(node.state)

        # get the list of possible actions from the current state
        actions = problem.get_actions(node.state)

        # loop on all possible actions
        for action in actions:
            # get the next state of the current state given an action
            child_state = problem.get_successor(node.state, action)
            # add the action to the node's list of actions to create the child's path
            child_path = node.path + [action]
            # create a new node for the child with the new state and actions
            child_node = Node(child_state, child_path)

            # check whether the child's node is already explored or in the frontier
            # if not then process the node
            if child_state not in explored and child_state not in frontier_set:
                # check whether the child's state is the goal state
                # if so return the actions list
                if problem.is_goal(child_state):
                    return child_path
                # append the child node to the rear of the frontier
                frontier.append(child_node)
                frontier_set.add(child_state)

    # if the frontier is empty then there are no solutions
    return None


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    @dataclass
    class Node:
        state: S
        path: list

    # if the initial state is the goal then return empty list
    if problem.is_goal(initial_state):
        return []

    frontier = deque()  # use the dequeue as stack
    frontier_set = set()    # use to search in it for smaller search complexity
    explored = set()    # set of the explored and processed nodes

    # create a node with the initial state -> start node
    node = Node(initial_state, [])

    frontier.append(node)   # add initial node to the stack
    frontier_set.add(node.state)    # add the state to the stack set for search

    # loop on stack until empty or a goal is reached
    while frontier:
        node = frontier.pop()   # pop the last inserted node into the stack to process it

        # remove the node state from the frontier set if present
        if node.state in frontier_set:
            frontier_set.remove(node.state)

        explored.add(node.state)    # add the popped node into the visited set

        # check if current node state is the goal
        if problem.is_goal(node.state):
            return node.path

        # get and loop on all possible actions of the current node
        actions = problem.get_actions(node.state)
        for action in actions:
            # for each action get the next node state and path and create a new node
            child_state = problem.get_successor(node.state, action)
            child_path = node.path + [action]
            child_node = Node(child_state, child_path)

            # if the created node is not explored yet or in frontier
            # then add it to the list to be processed
            if child_state not in explored and child_state not in frontier_set:
                frontier.append(child_node)
                frontier_set.add(child_state)

    # return None if there is no solution -> empty frontier
    return None


def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    @dataclass
    class Node:
        state: S
        path: list
        cost: int
        order = 0

        def __lt__(self, other):
            if self.cost < other.cost:
                return True
            if self.cost == other.cost:
                return self.order < other.order
            return False

    # checks if the initial state is the goal
    if problem.is_goal(initial_state):
        return []

    order = 0   # the order of which the node is inserted in in case if the costs of both nodes are equal
    node = Node(initial_state, [], 0)  # create initial node with initial state

    frontier = PriorityQueue()  # the frontier is a priority queue ordered by the cost
    frontier_set = set()    # a set to search in
    frontier.put(node)  # add the initial node to the frontier
    frontier_set.add(node.state)    # add the initial state to the frontier set

    explored = set()    # explored set for the processed nodes

    # loop on priority queue until empty or a goal is reached
    while frontier.queue:
        node = frontier.get()

        if node.state in frontier_set:
            frontier_set.remove(node.state)

        # check whether the node's state is the goal state
        # if so return the actions list to reach this state
        if problem.is_goal(node.state):
            return node.path

        explored.add(node.state)    # add the state to the processed set

        # get and loop on all possible actions of the current node
        actions = problem.get_actions(node.state)
        for action in actions:
            # get the next state of the current state given an action
            child_state = problem.get_successor(node.state, action)
            # add the action to the node's list of actions to create the child's path
            child_path = node.path + [action]
            # the cost of the child node in addition to that of the node's cost
            child_cost = node.cost + problem.get_cost(node.state, action)
            # create a new node with all calculated parameters
            child_node = Node(child_state, child_path, child_cost)

            child_node.order = order    # add the order of the node to be processed
            order += 1  # increment order for next node

            # if the node is not explored yet or in the frontier
            # then add the node to the frontier and frontier set
            if child_state not in explored and child_state not in frontier_set:
                frontier.put(child_node)
                frontier_set.add(child_state)
            # the child is already added before
            # replace the node in frontier with child node if the cost of child is smaller than the cost of the node in frontier
            elif child_state in frontier_set:
                current_node_index = frontier.queue.index(child_node.state)
                if child_node < frontier.queue[current_node_index]:
                    frontier.queue[current_node_index] = child_node
    return None

# gets the best out of the path cost anf the heuristic cost


def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # TODO: ADD YOUR CODE HERE
    @dataclass
    class Node:
        state: S
        path: list
        path_cost: int  # actual path cost
        # the estimated cost (heuristic) + the path cost -> actual cost
        heuristic_cost: int
        order = 0

        def __lt__(self, other):
            if self.heuristic_cost < other.heuristic_cost:
                return True
            if self.heuristic_cost == other.heuristic_cost:
                return self.order < other.order
            return False

    # checks if the initial state is the goal
    if problem.is_goal(initial_state):
        return []

    order = 0   # the order of which the node is inserted in in case if the costs of both nodes are equal
    # create initial node with initial state
    node = Node(initial_state, [], 0, 0)

    frontier = PriorityQueue()  # the frontier is a priority queue ordered by the cost
    frontier_set = set()    # a set to search in
    frontier.put(node)  # add the initial node to the frontier
    frontier_set.add(node.state)    # add the initial state to the frontier set

    explored = set()    # explored set for the processed nodes

    # loop on priority queue until empty or a goal is reached
    while frontier.queue:
        node = frontier.get()

        if node.state in frontier_set:
            frontier_set.remove(node.state)

        # check whether the node's state is the goal state
        # if so return the actions list to reach this state
        if problem.is_goal(node.state):
            return node.path

        explored.add(node.state)    # add the state to the processed set

        # get and loop on all possible actions of the current node
        actions = problem.get_actions(node.state)
        for action in actions:
            # get the next state of the current state given an action
            child_state = problem.get_successor(node.state, action)
            # add the action to the node's list of actions to create the child's path
            child_path = node.path + [action]
            # the cost of the actual path of the child node
            child_path_cost = node.path_cost + \
                problem.get_cost(node.state, action)
            # the cost of the path + heuristic cost
            heuristic_cost = heuristic(problem, child_state) + child_path_cost
            # create a new node with all calculated parameters
            child_node = Node(child_state, child_path,
                              child_path_cost, heuristic_cost)

            child_node.order = order    # add the order of the node to be processed
            order += 1  # increment order for next node

            # if the node is not explored yet or in the frontier
            # then add the node to the frontier and frontier set
            if child_state not in explored and child_state not in frontier_set:
                frontier.put(child_node)
                frontier_set.add(child_state)
            # the child is already added before
            # replace the node in frontier with child node if the cost of child is smaller than the cost of the node in frontier
            elif child_state in frontier_set:
                current_node_index = frontier.queue.index(child_node.state)
                if child_node < frontier.queue[current_node_index]:
                    frontier.queue[current_node_index] = child_node
    return None


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # TODO: ADD YOUR CODE HERE
    @dataclass
    class Node:
        state: S
        path: list
        cost: int
        order = 0

        def __lt__(self, other):
            if self.cost < other.cost:
                return True
            if self.cost == other.cost:
                return self.order < other.order
            return False

    # checks if the initial state is the goal
    if problem.is_goal(initial_state):
        return []

    order = 0   # the order of which the node is inserted in in case if the costs of both nodes are equal
    node = Node(initial_state, [], 0)  # create initial node with initial state

    # the frontier is a priority queue ordered by the heuristic cost
    frontier = PriorityQueue()
    frontier_set = set()    # a set to search in
    frontier.put(node)  # add the initial node to the frontier
    frontier_set.add(node.state)    # add the initial state to the frontier set

    explored = set()    # explored set for the processed nodes

    # loop on priority queue until empty or a goal is reached
    while frontier.queue:
        node = frontier.get()

        if node.state in frontier_set:
            frontier_set.remove(node.state)

        # check whether the node's state is the goal state
        # if so return the actions list to reach this state
        if problem.is_goal(node.state):
            return node.path

        explored.add(node.state)    # add the state to the processed set

        # get and loop on all possible actions of the current node
        actions = problem.get_actions(node.state)
        for action in actions:
            # get the next state of the current state given an action
            child_state = problem.get_successor(node.state, action)
            # add the action to the node's list of actions to create the child's path
            child_path = node.path + [action]
            # the cost of the child node is based on the heuristic function
            child_cost = heuristic(problem, child_state)
            # create a new node with all calculated parameters
            child_node = Node(child_state, child_path, child_cost)

            child_node.order = order    # add the order of the node to be processed
            order += 1  # increment order for next node

            # if the node is not explored yet or in the frontier
            # then add the node to the frontier and frontier set
            if child_state not in explored and child_state not in frontier_set:
                frontier.put(child_node)
                frontier_set.add(child_state)
            # the child is already added before
            # replace the node in frontier with child node if the cost of child is smaller than the cost of the node in frontier
            elif child_state in frontier_set:
                current_node_index = frontier.queue.index(child_node.state)
                if child_node < frontier.queue[current_node_index]:
                    frontier.queue[current_node_index] = child_node
    return None
