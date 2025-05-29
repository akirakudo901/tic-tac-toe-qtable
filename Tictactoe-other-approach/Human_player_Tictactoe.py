# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 00:50:16 2022

@author: mashi
"""

#Tictactoe interface for human players

from Gym_tailored_Tictactoe_env import Tictactoe
import random as rd
from numpy import argmax

circle = 0
empty = 1
cross = 2

env = Tictactoe()

def play():
    s = env.reset()
    done = False
    while done == False:
        env.render()
        action = human_player(s, env)
        s_next, reward, done, _ = env.step(action)
    env.render()
    
def human_player(obs, env):
    """
    An interface that, given the observation and environment, asks the player for input
    and produces the result too.
    """
    def ask_for_player_input():
        success = False
        while success == False:
            print("Please choose the square of your choice, as number between 0 and 8")
            inp = input()
            try: 
                inp = int(inp)
            except:
                raise TypeError("This is not an integer")
            if 0 > inp or 8 < inp:
                print("The value isn't within valid range.")
            elif inp not in env.obtain_empty_spots():
                print("That square is already filled!")
            else:
                success = True
        return inp
    
    def determine_win_loss(r):
        if r == env.win_r:
            print("YOU WON!")
        elif r == env.loss_r:
            print("YOU LOST...")
        elif r == env.draw_r:
            print("It's a draw!")
        elif r == env.not_done_r:
            pass
        #Not gonna be called but keeping as reminder
        elif r == env.error_r:
            print("YOU MADE A MISTAKE!")        
            
    #main
    env.render()
    action = ask_for_player_input()
    _, reward, _, _ = env.step(action)
    determine_win_loss(reward)
    return action


def computer(obs, p):
    #a computer that is optimal, but plays a random hand with probability p
    
    while p < 0 or p > 1:
        p = input("The given probability is invalid. Please input a value between 0 and 1.")
    
    #Checking for turn - checked!
    def get_turn(empties):
        if len(empties) % 2 == 1:
            return circle
        else:
            return cross
    
    def two_one(two, one):
        two_list = []
        one_list = []
        lines = ((0,1), (0,2), (1,2), 
                 (3,4), (3,5), (4,5),
                 (6,7), (6,8), (7,8),
                 (0,3), (0,6), (3,6), 
                 (1,4), (1,7), (4,7),
                 (2,5), (2,8), (5,8),
                 (0,4), (0,8), (4,8), 
                 (2,4), (2,6), (4,6))
        open_spot = (2,1,0, 5,4,3, 8,7,6, 6,3,0, 7,4,1, 8,5,2, 8,4,0, 6,4,2)
        for i in range(24):
            l = lines[i]
            two_cond = obs[l[0]] == obs[l[1]] == two
            one_cond = obs[open_spot[i]] == one
            if two_cond and one_cond:
                two_list = two_list + [l[0], l[1]]
                one_list.append(open_spot[i])
        return two_list, one_list
    
    def spots_in_reach(turn):
        _, result = two_one(turn, empty)
        #print("reach called, result:", result)
        return result
    
    def ten_points(turn):
        result, _ = two_one(empty, turn)
        return result
        
    def one_point(turn):
        r1, r2 = two_one(empty, empty)
        return (r1 + r2)

    def optimal_choice(turn, circles, crosses):
        #print("optimal chocie called")
        wins = spots_in_reach(turn)
        losses = spots_in_reach(2 - turn)
        if len(wins) != 0:
            return rd.sample(wins, 1)
        elif len(losses) != 0:
            return rd.sample(losses, 1)
        else:
            scores = [0]*9
            ten = ten_points(turn)
            for spot in ten:
                scores[spot] += 10
            one = one_point(turn)
            for spot in one:
                scores[spot] += 1
            for spot in (circles + crosses):
                scores[spot] = 0
            #print("Scores is:", scores)
            return argmax(scores)
    #I think checked?
    def random_choice(turn):
        return rd.sample(empties, 1)
    
    circles = []
    crosses = []
    empties = []
    for i in range(9):
        if obs[i] == 0:
            circles.append(i)
        elif obs[i] == 1:
            empties.append(i)
        elif obs[i] == 2:
            crosses.append(i)
    
    turn = get_turn(empties)
    
    random_val = rd.random()
    if p > random_val:
        result = random_choice(turn)[0]
    else:
        result = optimal_choice(turn, circles, crosses)
    return result
    
"""
    2) Define and use the optimal choice
    3) Define the random choice
    4) Combine the two through p
    5) output
    

    o  10  22
    x  999 10 
    1  10  o
    -> places where two turns are empty and last one is circle -> 10
    Otherwise, if one all over, it's gonna be 1.
    
    for i in range(9):
    1) run a scan over all squares to see which one are:
    in a row where already one of yours is and the other is empty -> 10
    in a row where nobody is still -> 1
    For each of such values, you add those values to the list's values.
    Then you finally pick the one with biggest value, or if two or more exist, random pick.'
"""
   

"""
#Let's see if it is actually optimal:
1)
oxo         oxx       oxo
xox         o--       -x-
--- o   OR  --- o OR  --o x
2)
oxo
xo-
--- x   OR 
    

o = 0
E = 1
x = 2
obss = [[o, x, o, 
         x, o, x, 
         E, E, E],
        [o, x, x, 
         o, E, E, 
         E, E, E],
        [o, x, o, 
         E, x, E, 
         E, E, o],
        [o, x, o, 
         x, o, E, 
         E, E, E]]

for i in range(len(obss)):
    obs = obss[i]
    print(computer(obs, 0))
"""

def qtable_ai(obs, qtable):
    """
    The Q-table need to be defined in a way that is compatible with the way I defined
    it in the Frozen_lake_thing.py code.
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
    
    s_num = state_to_number(obs)
    action = argmax(qtable[s_num,:])
    return action