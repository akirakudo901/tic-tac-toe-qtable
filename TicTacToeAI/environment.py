# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 01:20:46 2022

@author: mashi

Code rewritten based on Gym_tailored_Tictactoe_environment
"""


EMPTY   = E = 0
CIRCLE  = O = 1
CROSS   = X = 2
DRAW    = 3
ERROR   = 4
ONGOING = 999

ACTION_SPACE_SIZE = 9
OBSERVATION_SPACE_SIZE = 3**9

REWARD_FOR_WIN = 1
REWARD_FOR_LOSS = -1
REWARD_FOR_DRAW = 0.75
REWARD_FOR_ERROR = -5
REWARD_FOR_ONGOING = 0


class Tictactoe:
    
    def __init__(self, r_win=REWARD_FOR_WIN, r_loss=REWARD_FOR_LOSS, 
                 r_draw=REWARD_FOR_DRAW, r_error=REWARD_FOR_ERROR, 
                 r_ongoing=REWARD_FOR_ONGOING, ai_turn=CIRCLE):
        
        self.end_condition = ONGOING # can be circle(1), cross(2), draw(3), 
                                     #  error(4) or 999 for ongoing game.
        self.state = [E]*9
        self.ai_turn = ai_turn
        #reward values
        self.reward_for_win   = r_win
        self.reward_for_loss  = r_loss
        self.reward_for_draw  = r_draw
        self.reward_for_error = r_error
        self.reward_when_not_done = r_ongoing
    
    def reset(self):
        self.end_condition = ONGOING
        self.state = [E]*9
        return self.state
    
    @staticmethod
    def simulate_step(state, action, 
                      r_win=REWARD_FOR_WIN, r_loss=REWARD_FOR_LOSS, 
                      r_draw=REWARD_FOR_DRAW, r_error=REWARD_FOR_ERROR, 
                      r_ongoing=REWARD_FOR_ONGOING):
        def _chosen_square_is_empty():
            return (state[action] == EMPTY)
        
        def _update_state():
            new_state = []
            for i in state:
                new_state.append(i) 
            new_state[action] = Tictactoe.get_turn(state) 
            return new_state
        
        def _get_end_condition(s):
            _, end_condition = Tictactoe.is_terminal(s)
            return end_condition
        
        def _get_reward(turn, end_condition):
            opponent_turn = CROSS if turn is CIRCLE else CIRCLE
            
            if end_condition is turn:
                return r_win
            elif end_condition is opponent_turn:
                return r_loss
            elif end_condition is DRAW:
                return r_draw
            elif end_condition is ONGOING:
                return r_ongoing
            
        turn = Tictactoe.get_turn(state)

        if _chosen_square_is_empty():
            new_state = _update_state()
            end_condition = _get_end_condition(new_state)
            reward = _get_reward(turn, end_condition)
            done = (end_condition != ONGOING)
            return new_state, reward, done, end_condition 
            #observation; reward; done; end condition.
        else:
            end_condition = ERROR
            return state, r_error, True, end_condition


    def step(self, action):
        n_s, r, d, e_c = Tictactoe.simulate_step(self.state, action,
                                                r_win=self.reward_for_win,   r_loss=self.reward_for_loss, 
                                                r_draw=self.reward_for_draw, r_error=self.reward_for_error, 
                                                r_ongoing=self.reward_when_not_done)
        self.state = n_s
        self.end_condition = e_c
        return n_s, r, d, e_c
        #observation; reward; done; end condition.

    def render(self):
        def _convert_number_to_mark(n):
            if n == EMPTY:
                return " "
            elif n == CIRCLE:
                return "o"
            elif n == CROSS:
                return "x"
            
        Tictactoe.print_board(list(map(_convert_number_to_mark, self.state)))
    
    def set_state(self, state):
        self.reset()
        self.state = state

    #Other functions useful on tic tac toe board states
    @staticmethod
    def get_empty_squares(state):
        result = []
        for i in range(9):
            if state[i] is EMPTY:
                result.append(i)
        return result

    @staticmethod
    def get_turn(state):
        if len(Tictactoe.get_empty_squares(state)) % 2 == 0:
            return CROSS
        else:
            return CIRCLE

    @staticmethod    
    def print_board(b):
        print("_______")
        print("|" + b[0] + "|" + b[1] + "|" + b[2] + "|")
        print("|" + b[3] + "|" + b[4] + "|" + b[5] + "|")
        print("|" + b[6] + "|" + b[7] + "|" + b[8] + "|")
        print("-------")

    @staticmethod
    def is_terminal(state):
        def _at_least_one_line_is_full_with(s, mark):
            lines = ((0,1,2), (3,4,5), (6,7,8),
                     (0,3,6), (1,4,7), (2,5,8),
                     (0,4,8), (2,4,6))
            
            for L in lines:
                first, second, third = L[0], L[1], L[2]
                if s[first] == s[second] == s[third] == mark:
                    return True
    
            return False
        
        is_terminal = False
        
        if _at_least_one_line_is_full_with(state, CIRCLE):
            end_condition = CIRCLE
            is_terminal = True
        elif _at_least_one_line_is_full_with(state, CROSS):
            end_condition = CROSS
            is_terminal = True
        elif EMPTY not in state:
            end_condition = DRAW
            is_terminal = True
        else:
            end_condition = ONGOING
        
        return is_terminal, end_condition
