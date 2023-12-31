from sim_api import AgentHost
import numpy as np

base_path = r"/Users/arivf/PycharmProjects/pythonProject/Eklavya_ctRL/ctrl-sim/"
host = AgentHost(base_path + r"shr/obs", base_path + r"shr/act")

# Use host.get_action_from_sim and host.pass_observation_to_sum to interact
# with the simulator. Write your code below.


MAX_ANGLE = 180  # Maximum turning angle
MAX_PWM = 1  # Maximum PWM value
l1, l2, l3, l4, l5 = 5, 5, 5, 5, 5
# Assigning Rewards
q_values = np.zeros((5, 5, 5, 5, 5, 36))
reward_list = np.full((l1, l2, l3, l4, l5), -100)


actions = [x for x in range(-90,91) if x % 5 == 0]
# Number of runs
num_runs = 4000


# epsilon greedy algorithm to choose next action
def get_next_action(cl1, cl2, cl3, cl4, cl5, eps):
    if np.random.random() < eps:  # best action
        return np.argmax(q_values[cl1, cl2, cl3, cl4, cl5])
    else:
        return np.random.randint(35)  # random action


def get_observation_from_sim():
    lsa_readings = host.get_observation_from_sim()
    lsa_readings //= 52
    return int(lsa_readings[0]), int(lsa_readings[1]), int(lsa_readings[2]), int(lsa_readings[3]), int(lsa_readings[4])


def pass_action_to_sim(angle):


    # Calculate the PWM values based on the linear mapping
    pwm_scale = MAX_PWM / MAX_ANGLE
    pwm_left = 1-angle * pwm_scale
    pwm_right = 1+angle * pwm_scale  # Assuming opposite direction for the right wheel
    pwm = np.array((pwm_left, pwm_right), dtype=np.float64)
    host.pass_action_to_sim(-pwm)





# next location based on previous action
def get_next_location(cl1, cl2, cl3, cl4, cl5, action_index):
    if actions[action_index] == 90 and cl2 == 0 and cl3 == 0 and cl5 == 0:
        pass_action_to_sim(actions[action_index])
    elif 90 < actions[action_index] <= 180 and cl2 == 0 and cl3 == 0 and cl4 == 0:
        pass_action_to_sim(actions[action_index])
    if 90 > actions[action_index] >= 0 == cl1 and cl2 == 0 and cl3 == 0:
        pass_action_to_sim(actions[action_index])
    return get_observation_from_sim()




# define training parameters
epsilon = 0.9  # the percentage of time when we should take the best action (instead of a random action)
discount_factor = 0.9  # discount factor for future rewards
learning_rate = 0.9  # the rate at which the AI agent should learn

# run through 4000 training episodes
for episode in range(num_runs):
    # get the starting location for this episode
    # row_index, column_index = get_starting_location()

    # continue taking actions (i.e., moving) until we reach a terminal state

    # choose which action to take (i.e., where to move next)
    l1, l2, l3, l4, l5 = get_observation_from_sim()
    if (l2 == 0 and l3 == 0) and (l5 == 0 or l1 == 0 or l4 == 0):
        reward_list[l1, l2, l3, l4, l5] = -1

    action_index = get_next_action(l1, l2, l3, l4, l5, epsilon)
    ol1, ol2, ol3, ol4, ol5 = l1, l2, l3, l4, l5
    pass_action_to_sim(actions[action_index])
    # perform the chosen action, and transition to the next state (i.e., move to the next location)
      # store the old LSA readings


    # receive the reward for moving to the new state, and calculate the temporal difference
    reward = reward_list[l1, l2, l3, l4, l5]
    old_q_value = q_values[ol1, ol2, ol3, ol4, ol5, action_index]
    temporal_difference = reward + (discount_factor * np.max(q_values[l1, l2, l3, l4, l5])) - old_q_value

    # update the Q-value for the previous state and action pair
    new_q_value = old_q_value + (learning_rate * temporal_difference)
    q_values[ol1, ol2, ol3, ol4, ol5, action_index] = new_q_value

print('Training complete!')
