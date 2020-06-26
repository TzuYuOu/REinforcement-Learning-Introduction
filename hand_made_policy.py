import gym


def choose_action(state):
    pos, vel = state

    if pos*vel > 0:
        return 2    # push right
    else:
        return 0    # push left
    

if __name__ == "__main__":
    env = gym.make('MountainCar-v0')
    for i_episode in range(200):
        state = env.reset() # reset environment to initial state for each episode
        rewards = 0 # accumulate rewards for each episode
        for t in range(250):
            env.render()

            action = choose_action(state) # choose an action based on hand-made rule 
            next_state, reward, done, info = env.step(action) # do the action, get the reward
            rewards += reward
            state = next_state

            if done:
                print('Episode finished after {} timesteps, total rewards {}'.format(t+1, rewards))
                break

    env.close() # need to close, or errors will be reported