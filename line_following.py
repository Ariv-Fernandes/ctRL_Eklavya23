import numpy as np

MAX_ANGLE = 180  # Maximum turning angle
MAX_PWM = 10  # Maximum PWM value
l1, l2, l3, l4, l5 = 5, 5, 5, 5, 5
# Assigning Rewards
q_values = np.zeros((l1, l2, l3, l4, l5, 36))
reward_list = np.full((l1, l2, l3, l4, l5), -100)

if (l2 == 0 and l3 == 0) and (l5 == 0 or l1 == 0 or l4 == 0):
    reward_list[l1, l2, l3, l4, l5] = -1
actions = [x for x in range(181) if x % 5 == 0]
# Number of runs
num_runs = 4000
# Number of time steps
# num_steps = 1000


# function for terminal state:
def if_terminal_state(cl1, cl2, cl3, cl4, cl5):
    if reward_list[cl1, cl2, cl3, cl4, cl5] != -1:
        return True
    else:
        return False


# # function to choose a random non-terminal starting location:
# def get_starting_location():
#     # current_row_index = np.random.randint(envi_rows)
#     # current_colomn_index = np.random.randint(envi_colomns)
#     # while if_terminal_state(current_row_index, current_colomn_index):
#     #     current_row_index = np.random.randint(envi_rows)
#     #     current_colomn_index = np.random.randint(envi_colomns)
#     # return current_row_index, current_colomn_index
#     pass


# epsilon greedy algorithm to choose next action
def get_next_action(cl1, cl2, cl3, cl4, cl5, eps):
    if np.random.random() < eps:  # best action
        return np.argmax(q_values[cl1, cl2, cl3, cl4, cl5])
    else:
        return np.random.randint(35)  # random action


def pass_action_to_sim(angle):
    angle = max(0, min(angle, MAX_ANGLE))

    # Calculate the PWM values based on the linear mapping
    pwm_scale = MAX_PWM / MAX_ANGLE
    pwm_left = angle * pwm_scale
    pwm_right = -angle * pwm_scale  # Assuming opposite direction for the right wheel

    return pwm_left, pwm_right


def get_observation_from_sim():
    # the 5 LSA readings are divided into buckets of 51 values for readings [0,255]
    pass


# next location based on previous action
def get_next_location(cl1, cl2, cl3, cl4, cl5, action_index):
    if actions[action_index] == 90 and cl2 == 0 and cl3 == 0 and cl5 == 0:
        pass_action_to_sim(actions[action_index])
    elif 90 < actions[action_index] <= 180 and cl2 == 0 and cl3 == 0 and cl4 == 0:
        pass_action_to_sim(actions[action_index])
    if 90 > actions[action_index] >= 0 == cl1 and cl2 == 0 and cl3 == 0:
        pass_action_to_sim(actions[action_index])
    return get_observation_from_sim()


# function for shortest path:
# def get_shortest_path(sl1, sl2, sl3, sl4, sl5):
#     if if_terminal_state(sl1, sl2, sl3, sl4, sl5):
#         return []
#     else:  # if legal starting location
#         cl1, cl2, cl3, cl4, cl5 = sl1, sl2, sl3, sl4, sl5
#         shortest_path = [[cl1, cl2, cl3, cl4, cl5]]
#         while not if_terminal_state(cl1, cl2, cl3, cl4, cl5):
#             # take the best action
#             action_index = get_next_action(cl1, cl2, cl3, cl4, cl5, 1)
#             # move to the next location on the path, and add the new location to the list
#             cl1, cl2, cl3, cl4, cl5 = get_next_location(cl1, cl2, cl3, cl4, cl5, action_index)
#             shortest_path.append([cl1, cl2, cl3, cl4, cl5])
#         return shortest_path


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
# pygame.init()
# screen = pygame.display.set_mode((800, 500))
# pygame.display.set_caption("Line Following Bot")
# clock = pygame.time.Clock()
# surface = pygame.Surface((800, 500))
# surface.fill((52, 52, 52))
# ellipse_center = (400, 250)
# ellipse_radius_x = 300
# ellipse_radius_y = 200
# bot = pygame.image.load("bott.png").convert()
# bot_rect = bot.get_rect(midbottom=(400, 475))
# angle,speed=0,2
# bot_rect.centerx, bot_rect.centery = ellipse_center[0] + ellipse_radius_x, ellipse_center[1]
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()
#
#     screen.blit(surface, (0, 0))
#
#     pygame.draw.ellipse(screen, 'White', (ellipse_center[0] - ellipse_radius_x, ellipse_center[1] - ellipse_radius_y,
#                                           ellipse_radius_x * 2, ellipse_radius_y * 2), 10)
#     # angle -= 1*speed
#     # if angle <= -360:
#     #     angle = 0
#     # bot_rect.centerx = ellipse_center[0] + ellipse_radius_x * math.cos(math.radians(angle))
#     # bot_rect.centery = ellipse_center[1] + ellipse_radius_y * math.sin(math.radians(angle))
#
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_UP]:
#         bot_rect.centery -= 10 * speed
#
#     if keys[pygame.K_DOWN]:
#         bot_rect.centery += 10 * speed
#
#     if keys[pygame.K_LEFT]:
#         angle -= 1 * speed
#         bot_rect.centerx = ellipse_center[0] + ellipse_radius_x * math.cos(math.radians(angle))
#         bot_rect.centery = ellipse_center[1] + ellipse_radius_y * math.sin(math.radians(angle))
#     if keys[pygame.K_RIGHT]:
#         angle += 1 * speed
#         bot_rect.centerx = ellipse_center[0] + ellipse_radius_x * math.cos(math.radians(angle))
#         bot_rect.centery = ellipse_center[1] + ellipse_radius_y * math.sin(math.radians(angle))
#     if pygame.key.get_pressed():
#         screen.blit(pygame.transform.rotate(bot, 90 - angle), bot_rect)
#     else:
#         screen.blit(bot,bot_rect)
#     pwm_1 = bot_rect.topleft
#     pwm_2 = bot_rect.bottomleft
#     pygame.display.update()
#     clock.tick(60)
