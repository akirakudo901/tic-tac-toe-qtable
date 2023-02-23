# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 01:20:46 2022

@author: mashi

Code rewritten based on Gym_tailored_Tictactoe_environment
"""

import gym

EMPTY   = E = 0
CIRCLE  = O = 1
CROSS   = X = 2
DRAW    = 3
ERROR   = 4
ONGOING = 999


class TicTacToe:
    
    def __init__(self, r_win=1, r_loss=-1, r_draw=0.75, 
                 r_error=-5, r_not_done=0, ai_turn=CIRCLE):
        self.action_space = gym.spaces.Discrete(9)
        #Each of the 9 squares the agent can pick to put their mark in
        self.observation_space = gym.spaces.Tuple((gym.spaces.Discrete(3), 
                                              gym.spaces.Discrete(3), 
                                              gym.spaces.Discrete(3), 
                                              gym.spaces.Discrete(3), 
                                              gym.spaces.Discrete(3), 
                                              gym.spaces.Discrete(3), 
                                              gym.spaces.Discrete(3), 
                                              gym.spaces.Discrete(3), 
                                              gym.spaces.Discrete(3)))
        #Each gym.spaces.Discrete(3) corresponds to the 9 squares in the game
        # with each square filled with one of the 3 mark possible in the 
        # squares of the board; 0 for empty, 1 for circle and 2 for cross
        
        self.end_condition = ONGOING # can be circle(1), cross(2), draw(3), 
                                     #  error(4) or 999 for ongoing game.
        self.state = [E]*9
        self.ai_turn = ai_turn
        #reward values
        self.reward_for_win   = r_win
        self.reward_for_loss  = r_loss
        self.reward_for_draw  = r_draw
        self.reward_for_error = r_error
        self.reward_when_not_done = r_not_done
    
    def reset(self):
        self.end_condition = ONGOING
        self.state = [E]*9
        return self.state
    
    def step(self, action):
        def _chosen_square_is_empty():
            return (self.state[action] == EMPTY)
        
        def _update_state():
            self.state[action] = get_turn(self.state) 
        
        def _at_least_one_line_is_full_with(mark):
            s = self.state
            lines = ((0,1,2), (3,4,5), (6,7,8),
                     (0,3,6), (1,4,7), (2,5,8),
                     (0,4,8), (2,4,6))
            
            for L in lines:
                first, second, third = L[0], L[1], L[2]
                if s[first] == s[second] == s[third] == mark:
                    return True
    
            return False
        
        def _update_end_condition():
            if _at_least_one_line_is_full_with(CIRCLE):
                self.end_condition = CIRCLE
            elif _at_least_one_line_is_full_with(CROSS):
                self.end_condition = CROSS
            elif EMPTY not in self.state:
                self.end_condition = DRAW
        
        def _get_reward():
            ai_opponent_turn = CROSS if self.ai_turn is CIRCLE else CIRCLE
            
            if self.end_condition is self.ai_turn:
                return self.reward_for_win
            elif self.end_condition is ai_opponent_turn:
                return self.reward_for_loss
            elif self.end_condition is DRAW:
                return self.reward_for_draw
            elif self.end_condition is ONGOING:
                return self.reward_when_not_done

        if _chosen_square_is_empty():
            _update_state()
            _update_end_condition()
            reward = _get_reward()
            done = (self.end_condition != ONGOING)
            return self.state, reward, done, "NOTHING FOR NOW" 
            #observation; reward; done; info.
        else:
            self.end_condition = ERROR
            return self.state, self.reward_for_error, True, "NOTHING FOR NOW"

    def render(self):
        def _convert_number_to_mark(n):
            if n == EMPTY:
                return " "
            elif n == CIRCLE:
                return "o"
            elif n == CROSS:
                return "x"
            
        print_board(list(map(_convert_number_to_mark, self.state)))
    
    def _set_state(self, state):
        self.reset()
        self.state = state


#Other functions useful on tic tac toe board states
def get_empty_squares(state):
    result = []
    for i in range(9):
        if state[i] is EMPTY:
            result.append(i)
    return result

def get_turn(state):
    if len(get_empty_squares(state)) % 2 == 0:
        return CROSS
    else:
        return CIRCLE
    
def print_board(b):
    print("_______")
    print("|" + b[0] + "|" + b[1] + "|" + b[2] + "|")
    print("|" + b[3] + "|" + b[4] + "|" + b[5] + "|")
    print("|" + b[6] + "|" + b[7] + "|" + b[8] + "|")
    print("-------")