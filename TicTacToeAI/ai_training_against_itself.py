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

Q = np.zeros([environment.OBSERVATION_SPACE_SIZE, environment.ACTION_SPACE_SIZE])

# 2. Parameters of Q-learning
eta = .628    #learning rate
gma = .8  #.9 #discount rate for future actions
epis = 50001 #number of episodes
print_every_n_episodes = epis // 10

#probability by which the ai agent explores a new action; epsilon-greedy 
initial_epsilon = 0.95 
epsilon = 0.95
#probability by which the comp takes random actions
initial_probability = 0.75 
probability = 0.75 

rev_list = [] # rewards per episode calculate

#BASICALLY: AI goes through one episode, recording state-action pairs and 
# final reward (= only reward); then for every state-action pairs, value is 
# updated based on discounted reward

#Version 2.0: AI learns by propagating reward after every episodes
# Result is actually way better!!!

for i in range(epis):
    in_printed_episode = (i % print_every_n_episodes == 0)

    if in_printed_episode:
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
    while j < 11: #for each 9 step of the tic tac toe game
        if in_printed_episode: print("+++++++++++Next step+++++++++++")
        #env.render()
        qtable.log(Q)
        s_num = qtable.state_to_number(s)
        j+=1
        empty_spots = environment.get_empty_squares(s)
        if in_printed_episode: print("empty_spots", empty_spots)
                
        # Choose action from Q table
        state_wise_qtable = Q[s_num,:]
        a1 = np.argmax(state_wise_qtable)
        a2 = random.sample(empty_spots, 1)[0]
        threshold = random.random()
        if threshold > epsilon:
            if in_printed_episode: print("The AI chose to exploit.")
            a = a1
        else:
            if in_printed_episode: print("The AI chose to explore.")
            a = a2
        
        #Get new state & reward from environment
        if in_printed_episode: print("The action chosen by the AI is", a)
        s1,r,d,_ = env.step(a)
        s1_num = qtable.state_to_number(s1)
        if in_printed_episode: print("State:", s1, "State Number:", s1_num, "Reward:", r, " Done:", d)
        
        #Add current state-action pair and reward into list
        state_action_nextaction_pairs.append([s_num, a, s1_num])
        
        rAll += r
        if d == True:
            break
        s = s1
        
        #Computer's turn
        if in_printed_episode: print("Computer plays.")
        #env.render()
        #a = computer(s, probability)
        a, is_random_choice = minimax_comp.action(s, probability)
        if in_printed_episode: 
            print("The action chosen by the computer is", a)
            print("Was this a random choice? ", is_random_choice)
        s1,r,d,_ = env.step(a)
        s1_num = qtable.state_to_number(s1)
        if in_printed_episode: print("State:", s1, "State Number:", s1_num, "Reward:", r, " Done:", d)
        
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
    # env.render()
    probability -= (initial_probability / epis)
    epsilon -= (initial_epsilon / epis)
    if in_printed_episode: print("The computer now takes random moves with probability", round(probability,3))
    if in_printed_episode: print("The AI now takes random actions with probability", round(epsilon, 3))

#at the end of training
print("Reward Sum on all episodes " + str(sum(rev_list)/epis))
print("Final Values Q-Table")
print(Q)

qtable.log(Q)