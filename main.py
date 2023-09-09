import numpy as np
import matplotlib.pyplot as plt

# Number of arms
num_arms = 5

# True action values (unknown to the agent)
reward_list = np.random.normal(0, 1, num_arms)

# Number of runs
num_runs = 50

# Number of time steps
num_steps = 1000

# Epsilon values to test
epsilons = [0, 0.1, 0.01]

# Initialize variables to store results
average_rewards = np.zeros((len(epsilons), num_runs, num_steps))

# Run the epsilon-greedy algorithm for each epsilon value
for e, epsilon in enumerate(epsilons):
    for run in range(num_runs):
        # Initialize action-value estimates
        action_values = np.zeros(num_arms)

        # Initialize counts for each action
        num = np.zeros(num_arms)

        # Initialize array to store rewards for each time step
        rewards = np.zeros(num_steps)

        for step in range(num_steps):
            # Epsilon-greedy action selection
            if np.random.random() < epsilon:
                # Explore: Choose a random arm
                arm = np.random.choice(num_arms)
            else:
                # Exploit: Choose the arm with the highest estimated value
                arm = np.argmax(action_values)
            # Get the reward from the selected arm (sample from a normal distribution)
            reward = np.random.normal(reward_list[arm], 1)
            # Update action counts
            num[arm] += 1

            # Update action-value estimate using sample-average method
            action_values[arm] += (reward - action_values[arm]) / num[arm]
            rewards[step] = reward

        # Store the average rewards for this run
        average_rewards[e, run] = np.cumsum(rewards) / (np.arange(num_steps) + 1)

# Calculate and plot the average rewards for each epsilon value
plt.figure(figsize=(10, 6))
for e, epsilon in enumerate(epsilons):
    avg_rewards_overall = np.mean(average_rewards[e], axis=0)
    plt.plot(avg_rewards_overall, label=f"Epsilon = {epsilon}")

plt.xlabel("Time Steps")
plt.ylabel("Average Reward")
plt.title("Epsilon-Greedy Method for K-Armed Bandit (50 Runs)")
plt.legend()
plt.show()
