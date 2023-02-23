# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 09:45:59 2022

@author: mashi

Executes the actual training loop for the q table.
"""

import environment, minimax, qtable
import numpy as np
import random


EMPTY  = e = 0
CIRCLE = o = 1
CROSS  = x = 2


# 1. Load Environment and Q-table structure
env = environment.TicTacToe()
minimax_comp = minimax.Minimax_computer()

Q = np.zeros([3**9, env.action_space.n])

# 2. Parameters of Q-learning
eta = .628
gma = .8  #.9
epis = 100000

initial_epsilon = 0.95
epsilon = 0.95
initial_probability = 0.75 #probability by which the comp takes random actions
probability = 0.75 

rev_list = [] # rewards per episode calculate

#BASICALLY: AI goes through one episode, recording state-action pairs and 
# final reward (= only reward); then for every state-action pairs, value is 
# updated based on discounted reward

#Version 2.0: AI learns by propagating reward after every episodes
# Result is actually way better!!!

for i in range(epis):
    if i % 1000 == 0:
        print("+++++++++++++++++++++++++++++++++")
        print("=================================")
        print("We are at episode", i, "!!!!!!!")
        print("=================================")
        print("+++++++++++++++++++++++++++++++++")
    
    # Reset environment
    s = env.reset()
    rAll = 0
    d = False
    j = 0
    state_action_nextaction_pairs = [] #[state num, action, next action num]
    
    #The Q-Table learning algorithm
    while j < 11:
        print("AI learns.")
        #env.render()
        qtable.log(Q)
        s_num = qtable.state_to_number(s)
        j+=1
        empty_spots = environment.get_empty_squares(s)
        print("empty_spots", empty_spots)
                
        # Choose action from Q table
        state_wise_qtable = Q[s_num,:]
        a1 = np.argmax(state_wise_qtable)
        a2 = random.sample(empty_spots, 1)[0]
        threshold = random.random()
        if threshold > epsilon:
            a = a1
        else:
            a = a2
        
        #Get new state & reward from environment
        print("The action chosen by the AI is", a)
        s1,r,d,_ = env.step(a)
        s1_num = qtable.state_to_number(s1)
        print("State:", s1, "State Number:", s1_num, "Reward:", r, " Done:", d)
        
        #Add current state-action pair and reward into list
        state_action_nextaction_pairs.append([s_num, a, s1_num])
        
        rAll += r
        if d == True:
            break
        s = s1
        
        #Computer's turn
        print("Computer plays.")
        #env.render()
        #a = computer(s, probability)
        a = minimax_comp.action(s, probability)
        print("The action chosen by the computer is", a)
        s1,r,d,_ = env.step(a)
        s1_num = qtable.state_to_number(s1)
        print("State:", s1, "State Number:", s1_num, "Reward:", r, " Done:", d)
        
        rAll += r
        if d == True:
            break
        s = s1
        
    #At the end of each episode
    #Update Q-table
    state_action_nextaction_pairs.reverse()
    for pair in state_action_nextaction_pairs:
        s_num = pair[0]
        a = pair[1]
        s1_num = pair[2]
        Q[s_num,a] = Q[s_num,a] + eta*(r + gma*np.max(Q[s1_num,:]) - Q[s_num,a])
    
    #Other visualization & updating stuff
    rev_list.append(rAll)
    env.render()
    probability -= (initial_probability / epis)
    epsilon -= (initial_epsilon / epis)
    print("The computer now takes random moves with probability", round(probability,3))
    print("The AI now takes random actions with probability", round(epsilon, 3))

#at the end of training
print("Reward Sum on all episodes " + str(sum(rev_list)/epis))
print("Final Values Q-Table")
print(Q)

qtable.log(Q)