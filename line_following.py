import numpy as np

l1, l2, l3, l4, l5 = 255, 255, 255, 255, 255
# Assigning Rewards
q_values = np.zeros((l1, l2, l3, l4, l5, 3))
reward_list = np.full((l1, l2, l3, l4, l5), -100)
reward_list[177, 177, 177, 177, 177] = 100
if (l2 == 0 and l3 == 0) and (l5 == 0 or l1 == 0 or l4 == 0):
    reward_list[l1, l2, l3, l4, l5] = -1
actions = ["straight", "left", "right"]
# Number of runs
num_runs = 4000
# Number of time step
num_steps = 1000


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
        return np.random.randint(3)  # random action


# next location based on previous action
def get_next_location(cl1, cl2, cl3, cl4, cl5, action_index):
    nl1, nl2, nl3, nl4, nl5 = cl1, cl2, cl3, cl4, cl5
    if actions[action_index] == 'straight' and cl2 == 0 and cl3 == 0 and cl5 == 0:
        # t.forward(5)
        pass
    elif actions[action_index] == 'right' and cl2 == 0 and cl3 == 0 and cl4 == 0:
        # t.right(90)
        # t.forward(5)
        pass
    if actions[action_index] == 'left' and cl1 == 0 and cl2 == 0 and cl3 == 0:
        # t.left(90)
        # t.forward(5)
        pass
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


# define training parameters
epsilon = 0.9  # the percentage of time when we should take the best action (instead of a random action)
discount_factor = 0.9  # discount factor for future rewards
learning_rate = 0.9  # the rate at which the AI agent should learn

# run through 4000 training episodes
for episode in range(num_runs):
    # get the starting location for this episode
    # row_index, column_index = get_starting_location()

    # continue taking actions (i.e., moving) until we reach a terminal state
    while not if_terminal_state(l1, l2, l3, l4, l5):
        # choose which action to take (i.e., where to move next)
        action_index = get_next_action(l1, l2, l3, l4, l5, epsilon)

        # perform the chosen action, and transition to the next state (i.e., move to the next location)
        ol1, ol2, ol3, ol4, ol5 = l1, l2, l3, l4, l5  # store the old LSA readings
        l1, l2, l3, l4, l5 = get_next_location(l1, l2, l3, l4, l5, action_index)

        # receive the reward for moving to the new state, and calculate the temporal difference
        reward = reward_list[l1, l2, l3, l4, l5]
        old_q_value = q_values[ol1, ol2, ol3, ol4, ol5, action_index]
        temporal_difference = reward + (discount_factor * np.max(q_values[l1, l2, l3, l4, l5])) - old_q_value

        # update the Q-value for the previous state and action pair
        new_q_value = old_q_value + (learning_rate * temporal_difference)
        q_values[ol1, ol2, ol3, ol4, ol5, action_index] = new_q_value

print('Training complete!')
