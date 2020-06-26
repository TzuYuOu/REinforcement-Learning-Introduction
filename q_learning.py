import gym
import math
import numpy as np
import matplotlib.pyplot as plt


def choose_action(state, q_table, action_space, epsilon):
    if np.random.random_sample() < epsilon: # have ε probability to choose random action
        return action_space.sample()
    else: # Based on policy to choose action，也就是在 Q table 裡目前 state 中，選擇擁有最大 Q value 的 action
        return np.argmax(q_table[state[0], state[1]])


if __name__ == "__main__":
    env = gym.make('MountainCar-v0')

    num_states = (env.observation_space.high - env.observation_space.low)*\
                    np.array([10, 100])
    num_states = np.round(num_states, 0).astype(int) + 1   # num_states shape (19,15)             
    
    # Initialize Q table, Q_table shape (19,15,3)
    q_table = np.random.uniform(low = -1, high = 1, 
                          size = (num_states[0], num_states[1], 
                                  env.action_space.n))
    
    # Initialize variables to track rewards
    reward_list = []
    ave_reward_list = []

    get_epsilon = lambda i: max(0.01, min(1, 1.0 - math.log10((i+1)/25)))  # epsilon-greedy; 隨時間遞減
    get_lr = lambda i: max(0.01, min(0.5, 1.0 - math.log10((i+1)/25))) # learning rate; 隨時間遞減
    discount = 0.9  # reward discount factor
    episodes = 5000
    lr = 0.2
    # Run Q learning algorithm
    for i in range(episodes):
        # Initialize parameters
        tot_reward, reward = 0,0
        epsilon = get_epsilon(i)
        # lr = get_lr(i)
        state = env.reset() 

        # Discretize state
        state_adj = (state - env.observation_space.low)*np.array([10, 100])
        state_adj = np.round(state_adj, 0).astype(int)
    
        for t in range(200):   
            # Render environment for last 3 episodes
            if i >= episodes-3:
                env.render()
                
            # Determine next action - epsilon greedy strategy
            action = choose_action(state=state_adj, q_table=q_table, action_space=env.action_space, epsilon=epsilon)
    
            # Get next state and reward
            next_state, reward, done, info = env.step(action) 
            
            # Discretize next state
            next_state_adj = (next_state - env.observation_space.low)*np.array([10, 100])
            next_state_adj = np.round(next_state_adj, 0).astype(int)
            
            #Allow for terminal states
            if done and next_state[0] >= 0.5:
                q_table[state_adj[0], state_adj[1], action] = reward
                
            # Adjust Q value for current state
            else:
                delta = lr*(reward + 
                                discount*np.max(q_table[next_state_adj[0], next_state_adj[1]]) - 
                                q_table[state_adj[0], state_adj[1],action])

                q_table[state_adj[0], state_adj[1],action] += delta
                                     
            # Update variables
            tot_reward += reward
            state_adj = next_state_adj

            if done:
                break

        # Track rewards
        reward_list.append(tot_reward)
        
        if (i+1) % 100 == 0:
            ave_reward = np.mean(reward_list)
            ave_reward_list.append(ave_reward)
            reward_list = []
            
        if (i+1) % 100 == 0:    
            print('Episode {} Average Reward: {}'.format(i+1, ave_reward))

    env.close()

    
    
    # plot reward and episode graph
    plt.plot(100*(np.arange(len(ave_reward_list)) + 1), ave_reward_list)
    plt.xlabel('Episodes')
    plt.ylabel('Average Reward')
    plt.title('Average Reward vs Episodes')
    plt.savefig('rewards.jpg')
         
    plt.close()  