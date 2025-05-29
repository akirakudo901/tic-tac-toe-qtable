# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 13:25:02 2021

@author: mashi

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

Draw = 0.2; Loss = -1; Win = 1  ???
"""

class Tictactoe:
    def __init__(self):
        self.board = [1]*9
        self.end_condition = False # can be "o", "x", False and Error.
        self.turn = 0
        self.action_space = [0,1,2,3,4,5,6,7,8]
        self.observation_size = 9

    def reset(self):
        self.board = [1]*9
        self.end_condition = False # can be "o", "x", False and Error.
        self.turn = 0

    def step(self, inp):
        def screen_board():
            self.board[inp] != 1
            
        def update_board():
            self.board[inp] = self.turn

        def check_if_three_are_same(mark):
            list_three_are_same = ((0,1,2), (3,4,5), (6,7,8),
                                   (0,3,6), (1,4,7), (2,5,8),
                                   (0,4,8), (2,4,6))
            result = False
            
            for three_are_same in list_three_are_same:
                are_three_the_same = True
                for pos in three_are_same:
                    if self.board[pos] != mark:
                        are_three_the_same = False
                if are_three_the_same == True:
                    result = True
                    break
            return result
        
        def update_end_condition():
            if check_if_three_are_same(self.turn):
                self.end_condition = self.turn  
        
        def switch_turn():
            if self.turn == "o":
                self.turn = "x"
            else:
                self.turn = "o"
        
        #main
        if screen_board():
            update_board()
            update_end_condition()
            switch_turn()
            
        else:
            self.end_condition = "Error"
        
    def observation(self):
        return [self.turn] + [self.end_condition] + self.board