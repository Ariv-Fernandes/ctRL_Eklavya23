import numpy as np
from turtle import *

t = Turtle()
l1, l2, l3, l4, l5 = 0, 0, 0, 0, 0
# Assigning Rewards
q_values = np.zeros((l1, l2, l3, l4, l5, 3))
reward_list = np.full((l1, l2, l3, l4, l5), -100)
reward_list[177, 177, 177, 177, 177] = 100
if (l2 == 0 and l3 == 0) and (l5 == 0 or l1 == 0 or l4 == 0):
    reward_list[l1, l2, l3, l4, l5] = -1
actions = ["straight", "left", "right"]
# Number of runs
num_runs = 4000
# Number of time steps
num_steps = 1000
# Epsilon value to test
epsilon = 0.9
learning_factor = 0.9
discount_factor = 0.9


# function for terminal state:
def if_terminal_state(cl1, cl2, cl3, cl4, cl5):
    if reward_list[cl1, cl2, cl3, cl4, cl5] != -1:
        return True
    else:
        return False


# function to choose a random non-terminal starting location:
def get_starting_location():
    # current_row_index = np.random.randint(envi_rows)
    # current_colomn_index = np.random.randint(envi_colomns)
    # while if_terminal_state(current_row_index, current_colomn_index):
    #     current_row_index = np.random.randint(envi_rows)
    #     current_colomn_index = np.random.randint(envi_colomns)
    # return current_row_index, current_colomn_index
    pass


# epsilon greedy algorithm to choose next action
def get_next_action(cl1, cl2, cl3, cl4, cl5, eps):
    if np.random.random() < eps:  # best action
        return np.argmax(q_values[cl1, cl2, cl3, cl4, cl5])
    else:
        return np.random.randint(4)  # random action


# next location based on previous action
def get_next_location(cl1, cl2, cl3, cl4, cl5, action_index):
    nl1, nl2, nl3, nl4, nl5 = cl1, cl2, cl3, cl4, cl5
    if actions[action_index] == 'straight' and cl2 == 0 and cl3 == 0 and cl5 == 0:
        t.forward(5)
    elif actions[action_index] == 'right' and cl2 == 0 and cl3 == 0 and cl4 == 0:
        t.right(90)
        t.forward(5)
    if actions[action_index] == 'left' and cl1 == 0 and cl2 == 0 and cl3 == 0:
        t.left(90)
        t.forward(5)
    return nl1, nl2, nl3, nl4, nl5


# function for shortest path:
def get_shortest_path(sl1, sl2, sl3, sl4, sl5):
    if if_terminal_state(sl1, sl2, sl3, sl4, sl5):
        return []
    else:  # if legal starting location
        cl1, cl2, cl3, cl4, cl5 = sl1, sl2, sl3, sl4, sl5
        shortest_path = [[cl1, cl2, cl3, cl4, cl5]]
        while not if_terminal_state(cl1, cl2, cl3, cl4, cl5):
            # take the best action
            action_index = get_next_action(cl1, cl2, cl3, cl4, cl5, 1)
            # move to the next location on the path, and add the new location to the list
            cl1, cl2, cl3, cl4, cl5 = get_next_location(cl1, cl2, cl3, cl4, cl5, action_index)
            shortest_path.append([cl1, cl2, cl3, cl4, cl5])
        return shortest_path
