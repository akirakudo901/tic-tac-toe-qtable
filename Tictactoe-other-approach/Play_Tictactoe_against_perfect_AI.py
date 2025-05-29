# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 14:03:47 2022

@author: mashi

You can actually play against both perfect and non-perfect AI!
"""

from Gym_tailored_Tictactoe_env import Tictactoe
from Human_player_Tictactoe import computer, qtable_ai
import numpy as np
from Minimax_Tictactoe import Minimax_computer


env = Tictactoe()

Q = np.load("Tictactoe_Q_table_2022_1_9_19_34.npy")
mmcomp = Minimax_computer()

def play_against(type_comp="computer", Q=""):
    env.reset()
    done = False
    
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
        elif r == env.error_r:
            print("YOU MADE A MISTAKE!")
    
    s = env.reset()
    for i in range(20):
        if (i % 2 == 1):
            env.render()
            inp = ask_for_player_input()
            s_next, reward, done, _ = env.step(inp)
            s = s_next
            if done == True:
                determine_win_loss(reward)
                break
        else:
            env.render()
            #part determining which computer plays
            if type_comp == "AI":
                print("Q-table AI plays!")
                a = qtable_ai(s, Q)
            else:
                print("Computer plays!")
                a = mmcomp.action(s, 0)
                #a = computer(s, 0)
            
            s_next, reward, done, _ = env.step(a)
            s = s_next
            if done == True:
                determine_win_loss(reward)
                break
    env.render()

def play():
    play_against("AI", Q)
    

    