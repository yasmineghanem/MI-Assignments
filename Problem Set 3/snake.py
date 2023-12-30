from typing import Dict, List, Optional, Set, Tuple
from mdp import MarkovDecisionProcess
from environment import Environment
from mathutils import Point, Direction
from helpers.mt19937 import RandomGenerator
from helpers.utils import NotImplemented
import json
from dataclasses import dataclass
import math

"""
Environment Description:
    The snake is a 2D grid world where the snake can move in 4 directions.
    The snake always starts at the center of the level (floor(W/2), floor(H/2)) having a length of 1 and moving LEFT.
    The snake can wrap around the grid.
    The snake can eat apples which will grow the snake by 1.
    The snake can not eat itself.
    You win if the snake body covers all of the level (there is no cell that is not occupied by the snake).
    You lose if the snake bites itself (the snake head enters a cell occupied by its body).
    The action can not move the snake in the opposite direction of its current direction.
    The action can not move the snake in the same direction 
        i.e. (if moving right don't give an action saying move right).
    Eating an apple increases the reward by 1.
    Winning the game increases the reward by 100.
    Losing the game decreases the reward by 100.
"""

# IMPORTANT: This class will be used to store an observation of the snake environment
@dataclass(frozen=True)
class SnakeObservation:
    snake: Tuple[Point]     # The points occupied by the snake body 
                            # where the head is the first point and the tail is the last  
    direction: Direction    # The direction that the snake is moving towards
    apple: Optional[Point]  # The location of the apple. If the game was already won, apple will be None


class SnakeEnv(Environment[SnakeObservation, Direction]):

    rng: RandomGenerator  # A random generator which will be used to sample apple locations

    snake: List[Point]
    direction: Direction
    apple: Optional[Point]

    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        assert width > 1 or height > 1, "The world must be larger than 1x1"
        self.rng = RandomGenerator()
        self.width = width
        self.height = height
        self.snake = []
        self.direction = Direction.LEFT
        self.apple = None

    def generate_random_apple(self) -> Point:
        """
        Generates and returns a random apple position which is not on a cell occupied 
        by the snake's body.
        """
        snake_positions = set(self.snake)
        possible_points = [Point(x, y) 
            for x in range(self.width) 
            for y in range(self.height) 
            if Point(x, y) not in snake_positions
        ]
        return self.rng.choice(possible_points)

    def reset(self, seed: Optional[int] = None) -> Point:
        """
        Resets the Snake environment to its initial state and returns the starting state.
        Args:
            seed (Optional[int]): An optional integer seed for the random
            number generator used to generate the game's initial state.

        Returns:
            The starting state of the game, represented as a Point object.
        """
        if seed is not None:
            self.rng.seed(seed) # Initialize the random generator using the seed
        # TODO add your code here
        # IMPORTANT NOTE: Define the snake before calling generate_random_apple

        self.snake = [Point(math.floor(self.width//2), math.floor(self.height//2))] # initial snake position and length

        self.direction = Direction.LEFT # initial snake direction

        self.apple = self.generate_random_apple() # initial random apple position

        return SnakeObservation(tuple(self.snake), self.direction, self.apple)

    def actions(self) -> List[Direction]:
        """
        Returns a list of the possible actions that can be taken from the current state of the Snake game.
        Returns:
            A list of Directions, representing the possible actions that can be taken from the current state.

        """
        # TODO add your code here
        # a snake can wrap around the grid
        # NOTE: The action order does not matter
        possible_actions = []
        
        # the conditions are simple:
        # if the snake is moving up or down then it can only go right or left or keep moving in the same direction (NONE)
        # if the snake is moving right or left then it can only go up or down or keep moving in the same direction (NONE)
        possible_actions.extend([Direction.LEFT, Direction.RIGHT, Direction.NONE]) if self.direction == Direction.DOWN or self.direction == Direction.UP else possible_actions.extend([Direction.UP, Direction.DOWN, Direction.NONE])         
        
        return possible_actions

    def step(self, action: Direction) -> \
            Tuple[SnakeObservation, float, bool, Dict]:
        """
        Updates the state of the Snake game by applying the given action.

        Args:
            action (Direction): The action to apply to the current state.

        Returns:
            A tuple containing four elements:
            - next_state (SnakeObservation): The state of the game after taking the given action.
            - reward (float): The reward obtained by taking the given action.
            - done (bool): A boolean indicating whether the episode is over.
            - info (Dict): A dictionary containing any extra information. You can keep it empty.
        """
        # TODO Complete the following function

        action = self.direction if action == Direction.NONE else action # if the action in NONE then the snake should keep moving in the same direction

        done = False
        reward = 0
        self.direction = action # assign the direction of the snake with the action just taken
        
        winning_reward = 100 # the reward if the snake occupied all the grid
        losing_reward = -100 # the reward if the snak bit itself
        apple_reward = 1 # the reward if the snake ate an apple

        next_snake_head_position = self.snake[0] + action.to_vector() # move the snake's head according to the action taken

        # check the position after updating the head for wrapping around the grid
        # if the updated snake's head is out of the grid then it should wrap around 
        if next_snake_head_position.x >= self.width or next_snake_head_position.x < 0: 
            next_snake_head_position = Point(next_snake_head_position.x % self.width, next_snake_head_position.y)
        
        if next_snake_head_position.y >= self.height or next_snake_head_position.y < 0:
            next_snake_head_position = Point(next_snake_head_position.x, next_snake_head_position.y % self.height)
        
        snake_positions = set(self.snake) # get all the points in the grid that the snake occupies
        possible_positions = [Point(x, y) for x in range(self.width) for y in range(self.height)] # all possible points in the grid

        # cehck for losing condition => if the snake bit itself (snake's head == on of its body positions)
        if next_snake_head_position in snake_positions:
            done = True
            return SnakeObservation(tuple(self.snake), self.direction, self.apple), losing_reward, done, {} # return the current state and the losing reward and that the game is done (terminal state)    
        
        # check for winning condition => if the snake occupied all the grid cells
        self.snake.insert(0, next_snake_head_position) # insert the new snake's head at the beginning of the snake update positions in grid
        
        if len(self.snake) == len(possible_positions): # if the length of the snake is same as the length of all possible points in the grid length 
            done = True # winning terminal state
            if next_snake_head_position != self.apple: # check for final reward
                return SnakeObservation(tuple(self.snake), self.direction, self.apple), winning_reward, done, {} # if the last occupied grid didn't have an apple then just return the winning reward
            return SnakeObservation(tuple(self.snake), self.direction, self.apple), winning_reward + apple_reward, done, {} # the last occupied grid had an apple then increment and return thr winning reward
        
        # if the state is not terminal 
        if next_snake_head_position == self.apple: # if the snake ate an apple then we should leave the last the point => the snake grows by 1
            self.apple = self.generate_random_apple() # generate another random apple 
            reward = apple_reward # update the reward with the reward for eating an apple
        else:
            self.snake.pop() # if the snake didn't eat an apple then the length of the snake should stay the same so we pop the last point from the snak 
            reward = 0 # no reward is given


        # for the non terminal state
        done = False
        observation = SnakeObservation(tuple(self.snake), self.direction, self.apple)

        return observation, reward, done, {} 

    ###########################
    #### Utility Functions ####
    ###########################

    def render(self) -> None:
        # render the snake as * (where the head is an arrow < ^ > v) and the apple as $ and empty space as .
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if p == self.snake[0]:
                    char = ">^<v"[self.direction]
                    print(char, end='')
                elif p in self.snake:
                    print('*', end='')
                elif p == self.apple:
                    print('$', end='')
                else:
                    print('.', end='')
            print()
        print()

    # Converts a string to an observation
    def parse_state(self, string: str) -> SnakeObservation:
        snake, direction, apple = eval(str)
        return SnakeObservation(
            tuple(Point(x, y) for x, y in snake), 
            self.parse_action(direction), 
            Point(*apple)
        )
    
    # Converts an observation to a string
    def format_state(self, state: SnakeObservation) -> str:
        snake = tuple(tuple(p) for p in state.snake)
        direction = self.format_action(state.direction)
        apple = tuple(state.apple)
        return str((snake, direction, apple))
    
    # Converts a string to an action
    def parse_action(self, string: str) -> Direction:
        return {
            'R': Direction.RIGHT,
            'U': Direction.UP,
            'L': Direction.LEFT,
            'D': Direction.DOWN,
            '.': Direction.NONE,
        }[string.upper()]
    
    # Converts an action to a string
    def format_action(self, action: Direction) -> str:
        return {
            Direction.RIGHT: 'R',
            Direction.UP:    'U',
            Direction.LEFT:  'L',
            Direction.DOWN:  'D',
            Direction.NONE:  '.',
        }[action]