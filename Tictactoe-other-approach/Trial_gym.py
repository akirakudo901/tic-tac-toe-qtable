# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 16:06:33 2022

@author: mashi
"""

import gym
import numpy as np
#determining what the env is
env = gym.make('FrozenLake8x8-v1')
#making the Q-table
Q = np.zeros([env.observation_space.n,env.action_space.n])

print(Q)

#print("Observation space:", env.observation_space)
#print("Action space:", env.action_space)


"""
#determining how many episodes we want
for i_episode in range(1):
    env.reset()
#determining what to do within each episode
    for t in range(1000):
        env.render() #renders the env state at given time step
        action= env.action_space.sample() #determines which action is taken by AI
        observation, reward, done, info = env.step(action) #returning info by calling .step(action)
        
        #detemining what to do if done == True
        if done:
            print("Episode finished after {} timesteps.".format(t + 1))
            break
"""

env.close()
