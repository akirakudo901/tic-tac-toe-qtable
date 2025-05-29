# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 19:43:49 2022

@author: mashi


LETS THINK SYSTEMATICALLY.

The example seem to treat the Q-table by corresponding numbers to each state,
and then the environment seems to know what the numbers are and how to transition 
from state to state via these 

ONE THING I LEARNED FROM THIS EXPERIENCE: THE AI IS NOT WISE ENOUGH TO LEARN 
SOMETHING FROM SCRATCH THROUGH LIMITED ITERATIONS. IT HAS TO HAVE AT LEAST SOME CLUES
AS TO HOW TO PLAY THE GAME AND WIN IT INITIALLY.

HOW ABOUT I DIVIDE THE TRAINING INTO TWO PHASES:
    1) AI FIGHTS WITH A VERY UNWISE COMPUTER AND LEARNS HOW TO WIN FIRST (FIRST HALF)
    2) ONCE AI WINS 9 GAMES OUT OF 10 IN A CHAIN, COMPUTER BECOMES GRADUALLY GOOD AT THE GAME (SECOND HALF)

"""


#import gym
from .Gym_tailored_Tictactoe_env import Tictactoe
import numpy as np
from .Human_player_Tictactoe import computer
import random
from time import localtime, time
from . import Minimax_Tictactoe

#Define a function that converts states spit out from env into numbers systematically
# so to use those numbers in the Q-table to designate unique states.
"""
ORIGINALLY PLANNED TO DO THIS USING A TERNATY TREE, BUT GOT LAZY. THE AMOUNT OF DATA
DOES NOT REQUIRE THIS EXTRA EFFORT, WHICH WILL BE SKIPPED HERE.


# I will do this using a ternary tree and generating all possible combinations first,
# so that I can treat every unique state as one state and not depending on the sequence
# by which I reach those states.
"""

def state_to_number(s):
    #Each state will be given a unique number in the following way:
    #starting from the first number in the array, the first one is a 3^8.
    #one less is 3^7, etc.; the nth number (1st is 1) is 3^(9-n)
    #you add all of them to give a unique number:
        #E.g. [0,1,0,2,2,0,0,1,0] = 1(3^7) + 2(3^5) + 2(3^4) + 1(3^1) = 2838
    result = 0
    for i in range(9):
        result += s[i] * (3**(8-i))
    return result

# 1. Load Environment and Q-table structure
env = Tictactoe()

#Let's set the strength of the computer to increase gradually from 0.5 to 1.
#probability = 0.5 #probability by which training computer will play a random move (if constant)

#### LAZINESS TOOK OVER ME.
#BASICALLY WAS TRYING TO IMPLEMENT THE ".n" IDEA WITH TUPLE SPACE
#SINCE IM NOT SURE IF THE TUPLE SPACE IS THE RIGHT IDEA HERE, AND
#SINCE I AM NOT SURE HOW TO DO THE ".n" IDEA, I WILL JUST PUT THE RAW
#NUMBER.
#len_tuple_observation_space = env.observation_space.__len__
#Q = np.zeros([len_tuple_observation_space, env.action_space.n])

Q = np.zeros([3**9, env.action_space.n])

# env.observation.n, env.action_space.n gives number of states and action in env loaded
# 2. Parameters of Q-learning
eta = .628
gma = .8  #.9
epis = 10000

initial_epsilon = 0.95
epsilon = 0.95


rev_list = [] # rewards per episode calculate
initial_probability = 0.75 #initial probability by which the comp takes random actions
probability = 0.75 

minimax_comp = Minimax.Minimax_computer()



#BASICALLY: AI goes through one episode, recording state-action pairs and final reward (= only reward)
# then for every state-action pairs, value is updated based on discounted reward

#Version 2.0: AI learns through episodic propagation, rather than through each step
# Result is actually way better!!!
# This AI is 
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
    state_action_nextaction_pairs = [] #[state number, action, next action number]
    
    #The Q-Table learning algorithm
    while j < 20:
        print("AI learns.")
        #env.render()
        s_num = state_to_number(s)
        j+=1
        empty_spots = []
        for i in range(9):
            if s[i] == 1:
                empty_spots.append(i)
                
        # Choose action from Q table
        qtable = Q[s_num,:]
        a1 = np.argmax(qtable)
        a2 = random.sample(empty_spots, 1)[0]
        threshold = random.random()
        if threshold > epsilon:
            a = a1
        else:
            a = a2
        
        #Get new state & reward from environment
        print("The action chosen by the AI is", a)
        s1,r,d,_ = env.step(a)
        s1_num = state_to_number(s1)
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
        s1_num = state_to_number(s1)
        print("State:", s1, "State Number:", s1_num, "Reward:", r, " Done:", d)
        
        rAll += r
        if d == True:
            break
        s = s1
        
    #at the end of each episode
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



"""
==========================================================================
#Learning against growing computer phase; Q-table updated at each steps
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
    #The Q-Table learning algorithm
    while j < 99:
        print("AI learns.")
        #env.render()
        s_num = state_to_number(s)
        j+=1
        empty_spots = []
        for i in range(9):
            if s[i] == 1:
                empty_spots.append(i)
                
        # Choose action from Q table
        qtable = Q[s_num,:]
        a1 = np.argmax(qtable)
        a2 = random.sample(empty_spots, 1)
        threshold = random.random()
        if threshold > epsilon:
            a = a1
        else:
            a = a2[0]
        
        #Get new state & reward from environment
        print("The action chosen by the AI is", a)
        s1,r,d,_ = env.step(a)
        s1_num = state_to_number(s1)
        print("State:", s1, "State Number:", s1_num, "Reward:", r, " Done:", d)
        #Update Q-Table with new knowledge
        if d == True:
            Q[s_num,a] = Q[s_num,a] + eta*(r + gma*np.max(Q[s1_num,:]) - Q[s_num,a])
            rAll += r
            break
        s = s1
        
        #Computer's turn
        print("Computer plays.")
        #env.render()
        a = computer(s, probability)
        print("The action chosen by the computer is", a)
        s1,r,d,_ = env.step(a)
        s1_num = state_to_number(s1)
        print("State:", s1, "State Number:", s1_num, "Reward:", r, " Done:", d)
        
        #Update Q-Table with new knowledge
        Q[s_num,a] = Q[s_num,a] + eta*(r + gma*np.max(Q[s1_num,:]) - Q[s_num,a])
        rAll += r
        s = s1
        if d == True:
            break
    rev_list.append(rAll)
    env.render()
    probability -= (initial_probability / epis)
    epsilon -= (initial_epsilon / epis)
    print("The computer now takes random moves with probability", round(probability,3))
    print("The AI now takes random actions with probability", round(epsilon, 3))
print("Reward Sum on all episodes " + str(sum(rev_list)/epis))
print("Final Values Q-Table")
print(Q)
===============================================================
"""
time_tuple = localtime(time())[0:5]
acc = str(time_tuple[0]); [acc := acc + "_" + str(x) for x in time_tuple[1:5]]
name_original = "Tictactoe_Q_table_" + acc

input_done = False
while input_done == False:
    inp = input("Do you want to save the new Q table?: YES / NO")
    if inp == "YES":
        input_done = True
        name = input("Please name the new file (or leave blank to create a name automatically)")
        if name == "":
            np.save(name_original, Q)
        else:
            np.save(name, Q)
    elif inp == "NO":
        input_done = True
        print("The process is over")
    else:
        print("The input may not have been a YES or NO")
    






"""
==================================================================
THIS WAS FOR FROZEN LAKE. THE ORIGINAL ONE.
# 1. Load Environment and Q-table structure
env = gym.make('FrozenLake8x8-v1')

Q = np.zeros([env.observation_space.n,env.action_space.n])
# env.observation.n, env.action_space.n gives number of states and action in env loaded
# 2. Parameters of Q-learning
eta = .628
gma = .9
epis = 50000
rev_list = [] # rewards per episode calculate
# 3. Q-learning Algorithm
for i in range(epis):
    # Reset environment
    s = env.reset()
    rAll = 0
    d = False
    j = 0
    #The Q-Table learning algorithm
    while j < 99:
        env.render()
        j+=1
        # Choose action from Q table
        a = np.argmax(Q[s,:] + np.random.randn(1,env.action_space.n)*(1./(i+1)))
        #Get new state & reward from environment
        s1,r,d,_ = env.step(a)
        #Update Q-Table with new knowledge
        Q[s,a] = Q[s,a] + eta*(r + gma*np.max(Q[s1,:]) - Q[s,a])
        rAll += r
        s = s1
        if d == True:
            break
    rev_list.append(rAll)
    env.render()
print("Reward Sum on all episodes " + str(sum(rev_list)/epis))
print("Final Values Q-Table")
print(Q)
"""