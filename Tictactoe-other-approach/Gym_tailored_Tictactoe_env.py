# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 20:28:31 2022

@author: mashi

THIS IS THE VERSION THAT I TRIED MY BEST TO TAILOR TO THE GYM FORMAT. HOPEFULLY IT'S WORKING.

I will again teach computers how to play Tic tac toe. Hopefully this time, the agent
will learn the best strategy available.

Flow:
    1) Create Tic tac toe world made to interact with AI.
    2) Create AI that interact with world.
    3) Teach AI to play it and see if it works.
    
Currently in stage:
    -1-
"""

"""
Conception of game:
    1) Each game board states will be shown as a list of "o", "-" and "x". These would be respectively
    expressed as either 0, 1 or 2.
    2) The AI is given the current state of the board. It will learn which case that is still
    open to put its own mark in order to win.
    3) Thus, the game will have to:
        1 - Take an input of which mark to put where 
        (the AI and the board will always know which mark they are, and when they will have to
         put their mark)
        2 - Update the board accordingly
        3 - Check for end condition; if ending, output the result. Otherwise, take the next input
        for the AI to play.
        
*The first player is 0 ("o"), second is 2 ("x")

As a conception, I want to make sure that output is the only way information gets out of the game.
The other things will be dedicated to updating the game itself, not outputting anything.

Draw = 0.3; Loss = -1; Win = 1  ???
"""

from gym import spaces
import numpy as np

circle = 0
empty = 1
cross = 2

class Tictactoe:
    def __init__(self):
        self.action_space = spaces.Discrete(9)
        #Each of the 9 squares the agent can pick to put their mark in
        self.observation_space = spaces.Tuple((spaces.Discrete(3), 
                                              spaces.Discrete(3), 
                                              spaces.Discrete(3), 
                                              spaces.Discrete(3), 
                                              spaces.Discrete(3), 
                                              spaces.Discrete(3), 
                                              spaces.Discrete(3), 
                                              spaces.Discrete(3), 
                                              spaces.Discrete(3)))
        #Each spaces.Discrete(3) corresponds to the 9 squares in the game
        # with each square filled with one of the 3 mark possible in the 
        # squares of the board; 0 for "o", 1 for empty and 2 for "x"
        self.turn = circle
        self.end_condition = 999 # can be circle(0), cross(2), "draw", 999 (for still 
                                 # ongoing) and "Error".
        self.state = np.array([1,1,1,1,1,1,1,1,1])
        #reward values
        self.win_r = 1
        self.loss_r = -1
        self.draw_r = 0.75
        self.error_r = 5
        self.not_done_r = 0

    def reset(self):
        self.turn = circle
        self.end_condition = 999 # can be circle(0), cross(2), "draw", 999 (for still 
                                 # ongoing) and "Error".
        self.state = np.array([1,1,1,1,1,1,1,1,1]) #0 for circle
        return self.state

    def step(self, inp):
        def screen_board():
            return (self.state[inp] == empty)
        
        def update_board():
            self.state[inp] = self.turn 
        
        def check_if_three_are_same(mark):
            list_three_are_same = ((0,1,2), (3,4,5), (6,7,8),
                                   (0,3,6), (1,4,7), (2,5,8),
                                   (0,4,8), (2,4,6))
            result = False
            
            for three_are_same in list_three_are_same:
                are_three_the_same = True
                for pos in three_are_same:
                    if self.state[pos] != mark:
                        are_three_the_same = False
                if are_three_the_same == True:
                    result = True
                    break
            return result
        
        def update_end_condition():
            if check_if_three_are_same(self.turn):
                self.end_condition = self.turn
            elif 1 not in self.state:
                self.end_condition = "draw"
        
        def switch_turn():
            if self.turn == circle:
                self.turn = cross
            else:
                self.turn = circle
        
        def reward():
            if self.end_condition == circle:
                return self.win_r
            elif self.end_condition == cross:
                return self.loss_r
            elif self.end_condition == "draw":
                return self.draw_r
            elif self.end_condition == 999:
                return self.not_done_r
            ##Never gonna be called but just to make it clear
            elif self.end_condition == "Error":
                return self.error_r
            ##

        #main
        if screen_board():
            update_board()
            update_end_condition()
            switch_turn()
            done = (self.end_condition != 999)
            return self.state, reward(), done, "NOTHING FOR NOW" #observation; reward; done; info.
        else:
            self.end_condition = "Error"
            return self.state, -5, True, "NOTHING FOR NOW"
        
    def render(self):
        def number_to_symbol(n):
            if n == 0:
                return "o"
            elif n == 1:
                return " "
            elif n == 2:
                return "x"
            
        def print_board(b):
            print("_______")
            print("|" + b[0] + "|" + b[1] + "|" + b[2] + "|")
            print("|" + b[3] + "|" + b[4] + "|" + b[5] + "|")
            print("|" + b[6] + "|" + b[7] + "|" + b[8] + "|")
            print("-------")
            
        print_board(list(map(number_to_symbol, self.state)))
    
    #On an arbitrary state:
    def obtain_empty_spots(self, state=""):
        if state == "":
            state = self.state
        result = []
        for i in range(9):
            if state[i] == 1:
                result.append(i)
        return result
    
    def get_turn(self, state=""):
        if state == "":
            state = self.turn
        else:
            if len(self.obtain_empty_spots(state)) % 2 == 0:
                return cross
            else:
                return circle
    
    def set_state(self, state):
        self.reset()
        self.state = state
        self.turn = self.get_turn(state)