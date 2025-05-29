# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 13:56:13 2022

@author: mashi
"""

from Gym_tailored_Tictactoe_env import Tictactoe
from Human_player_Tictactoe import computer

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

games = 1000
env = Tictactoe()

win = 0
loss = 0
draw = 0
error = 0

probability = 0

for i in range(games):
    # Reset environment
    s = env.reset()
    d = False
    j = 0
    #The Q-Table learning algorithm
    while j < 99:
        if j % 2 == 0: #let the AI learn
            print("Computer1 plays.")
            env.render()
            j+=1
            a = computer(s, probability)
            print("The action chosen by the computer1 is", a)
            s1,r,d,_ = env.step(a)
            s1_num = state_to_number(s1)
            print("State:", s1, "State Number:", s1_num, "Reward:", r, " Done:", d)
            s = s1
            if d == True:
                if r == 2:
                    win += 1
                elif r == -1:
                    loss += 1
                elif r == 0.8:
                    draw += 1
                elif r == -5:
                    error += 1
                break
        else:
            print("Computer2 plays.")
            env.render()
            j += 1
            a = computer(s, probability)
            print("The action chosen by the computer2 is", a)
            s1,r,d,_ = env.step(a)
            s1_num = state_to_number(s1)
            print("State:", s1, "State Number:", s1_num, "Reward:", r, " Done:", d)
            s = s1
            if d == True:
                if r == 2:
                    win += 1
                elif r == -1:
                    loss += 1
                elif r == 0.8:
                    draw += 1
                elif r == -5:
                    error += 1
                break
    env.render()
    print("The computer now takes random moves with probability", round(probability,3))
print("Final win rate:", round(win / games,2), "Wins:", win, "Losses:", loss, "Draws:", draw, "Errors:", error)

