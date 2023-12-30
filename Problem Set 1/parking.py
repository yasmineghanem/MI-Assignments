from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

# TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Any

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem


class ParkingProblem(Problem[ParkingState, ParkingAction]):
    # A set of points which indicate where a car can be (in other words, every position except walls).
    passages: Set[Point]
    # A tuple of points where state[i] is the position of car 'i'.
    cars: Tuple[Point]
    # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
    slots: Dict[Point, int]
    # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        # TODO: ADD YOUR CODE HERE
        # the initial state is the positions of the cars at the beginning
        return self.cars

    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        # TODO: ADD YOUR CODE HERE
        # loop on all locations of cars in a given state with their indices
        for index, location in enumerate(state):
            # checks that all states are present in slots for all car locations in the given state
            if [state[i] in list(self.slots.keys()) for i in range(len(state))]:
                if location in list(self.slots.keys()):  # if the location in slots
                    # checks that each car in the state is in the same spot as in slots
                    if self.slots[location] == index:
                        return True  # goal reached
        return False

    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        # TODO: ADD YOUR CODE HERE
        actions = []
        # loops on all points in a given state and assign correct index to it
        for index, location in enumerate(state):
            for direction in Direction:  # check if car can move up, down, left and right
                # converts the direction into point vector and adds it to current location
                new_location = location + direction.to_vector()
                # if new location is not a wall and not already present in state
                if new_location in self.passages and new_location not in state:
                    # add this direction as a possible action to the given state
                    actions.append((index, direction))
        return actions

    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        # TODO: ADD YOUR CODE HERE
        successor_state = []  # a list of all locations in a given index that represent next state
        for index, location in enumerate(state):
            # if the car index is the same as the given car index in nest action
            if index == action[0]:
                # move car to new location
                new_location = location + action[1].to_vector()
                # add the new location to the next state
                successor_state.append(new_location)
            else:
                # add the current location as is
                successor_state.append(location)
        return successor_state

    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        # TODO: ADD YOUR CODE HERE
        # action[0] -> car index
        # action[1] -> direction

        cost = 0
        location = state[action[0]]  # location of the current given state
        # apply the given action to the given state
        new_location = location + action[1].to_vector()

        # check if car moved moved in another car's slot
        if new_location in self.slots.keys() and self.slots[new_location] != action[0]:
            cost = 100 + (26 - action[0])
        else:
            cost = 26 - action[0]

        return cost

     # Read a parking problem from text containing a grid of tiles

    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages = set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip()
                                   for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position: index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
