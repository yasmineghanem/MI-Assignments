# This file contains the options that you should modify to solve Question 2


# we want the policy to seek the near terminal state (reward +1) via the short dangerous path (moving besides the row of -10 state).
def question2_1():
    #TODO: Choose options that would lead to the desired results 
    return {
        "noise": 0.001,         # noise should be small as we are very close to the negative terminal state
        "discount_factor": 0.1, # the discount factor should be small to reach the near positive terminal state
        "living_reward": -7.5   # should be smaller than the negative termainal state
    }


# we want the policy to seek the near terminal state (reward +1) via the long safe path (moving away from the row of -10 state)
def question2_2():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.01,          # as we are moving away from the negative terminal states row then the noise can be increased a bit
        "discount_factor": 0.1, # the discount factor should be small to reach the near positive terminal state
        "living_reward": -0.1   # the living reward should be compensated in the end by the terminal reward so should be less than the 1/(number of states to terminal state) 
    }

# we want the policy to seek the far terminal state (reward +10) via the short dangerous path (moving besides the row of -10 state)
def question2_3():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.001,         # as we are moving cloaser to the negative terminal states row then the noise can be decreased to avoid going to a negative terminal state
        "discount_factor": 1,
        "living_reward": -1.0
    }

# we want the policy to seek the far terminal state (reward +10) via the long safe path (moving away from the row of -10 state)
def question2_4():
    #TODO: Choose options that would lead to the desired results
        return {
        "noise": 0.2,               # as we are moving further away from the negative terminal states row then the noise can be increased a bit
        "discount_factor": 1.0,     # maximum to reach the highest positive reward possible state
        "living_reward": -0.125     # the living reward should be compensated in the end by the terminal reward so should be less than the 1/(number of states to terminal state)       
    }

# For question2_5, we want the policy to avoid any terminal state and keep the episode going on forever
def question2_5():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": 20     # should be larger than any terminal state to ensure that never ends and keeps moving to non-termainal states
    }

# we want the policy to seek any terminal state (even ones with the -10 penalty) and try to end the episode in the shortest time possible
def question2_6():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -20    # should be smaller than any terminal state to ensure that it immediately goes to the nearest terminal state even if it's negative
    }