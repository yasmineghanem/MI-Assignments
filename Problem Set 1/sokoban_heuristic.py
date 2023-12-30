from sokoban import SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance
from helpers.utils import NotImplemented

# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal


def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1


# TODO: Import any modules and write any functions you want to use


def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    # TODO: ADD YOUR CODE HERE
    # IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    # NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function

    # The idea behind my solution was first to focus on the deadlock cases first
    # First by checking if the crate is pushed against a wall that is also a border
    # This could lead to three states:
    # 1. The crate is in a corner
    # 2. The crate is pushed against the wall and another crate
    # 3. The crate is pushed against a wall and there is no goals in the same line
    # This is of course depending on which side of the wall the crate is pushed against
    # Whether the crate is pushed against the up or down walls or the left or right walls
    # If any of these cases occurred then the heuristic function should return infnity indicating a very high cost for this path and the algorithm should not persue it

    for crate in state.crates:
        # If crate is pushed against a left or right border wall
        if crate.x == 1 or crate.x == state.layout.width-2:

            # If the crate is against the wall but already in goal should not be considered deadlock
            if crate in state.layout.goals:
                continue

            # If the crate is pushed against wall and another crate from above
            if crate + Direction.to_vector(Direction.UP) not in state.layout.walkable or crate + Direction.to_vector(Direction.UP) in state.crates:
                return float('inf')

            # If the crate is pushed against wall and another crate from below
            if crate + Direction.to_vector(Direction.DOWN) not in state.layout.walkable or crate + Direction.to_vector(Direction.DOWN) in state.crates:
                return float('inf')

            # if crate is pushed against wall alone but there is no goals with the same x as the crate
            if not any([goal.x == crate.x for goal in state.layout.goals]):
                return float('inf')

        # If crate is pushed against a up or down border wall
        if crate.y == 1 or crate.y == state.layout.height-2:

            # If the crate is against the wall but already in goal should not be considered deadlock
            if crate in state.layout.goals:
                continue

            # If the crate is pushed against wall and another crate from above
            if crate + Direction.to_vector(Direction.LEFT) not in state.layout.walkable or crate + Direction.to_vector(Direction.LEFT) in state.crates:
                return float('inf')

            # If the crate is pushed against wall and another crate from below
            if crate + Direction.to_vector(Direction.RIGHT) not in state.layout.walkable or crate + Direction.to_vector(Direction.RIGHT) in state.crates:
                return float('inf')

            # if crate is pushed against wall alone but there is no goals with the same y as the crate
            if not any([goal.y == crate.y for goal in state.layout.goals]):
                return float('inf')

    # If all deadlocks cases are reviewed and none return from the function with cost = infinity
    # Then we should return the heuristic cost
    # I first wanted to calculate the heuristic as the minimum sum of distances when all crates are in a goal
    # One way or another but this would've required a brute force aproach
    # So instead I calculated the manhattan distance from each crate to the nearest goal even if the (crate, goal) combination
    # Occurred before as it is definitely <= to the actual cost which will make the admissible
    # It is also consistent as the cost of the next stat could never be greater than the current state if all crates
    # Are calculated to the nearest goal.
    min_distance_sum = 0

    for crate in state.crates:
        min_distance = min(manhattan_distance(crate, goal)
                           for goal in state.layout.goals)
        min_distance_sum += min_distance

    return min_distance_sum
