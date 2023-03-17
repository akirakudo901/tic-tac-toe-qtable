# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 20:10:24 2022

@author: mashi

File which allows the player to play against a tic tac toe agent of their choice on console.
"""

import environment as env
from environment import Tictactoe as ttt
from minimax import Minimax_computer

class TictactoeGame:
    MINIMAX_COMP_NAME = "minimax"
    VALID_TURN_ENTRY = [env.CIRCLE, env.CROSS]

    def __init__(self, player_turn=env.CIRCLE, ai=MINIMAX_COMP_NAME):
        self.set_player_turn(player_turn)
        self.set_ai(ai)
        self.game = env.Tictactoe()
        self.play()

    def set_player_turn(self, turn):
        if turn in TictactoeGame.VALID_TURN_ENTRY:
            self.player_turn = turn
        else:
            self.player_turn = env.CIRCLE
            print("The 'player_turn' paramter was not recognized, and thus set to CIRCLE.\n") 

    def set_ai(self, ai):
        if ai is TictactoeGame.MINIMAX_COMP_NAME:
            self.ai = Minimax_computer()
        else:
            self.ai = Minimax_computer()
            print("The 'ai' parameter was not recognized, and thus set to Minimax.\n")

    def play(self):
        # Players can choose optionally the ai they wanna play against
        ai = self._get_and_validate_input("Please input your computer of choice.")
        self.set_ai(ai)
        # Player chooses which mark they want to play as
        turn = env.CIRCLE if self._get_y_n("Do you want to go first?") else env.CROSS
        self.set_player_turn()
        self._play_loop()
        # The current turn's play is set, prompting an input
        if self.player_turn is env.CIRCLE:
            a = self._take_player_input()
        else:
            a = self.ai.action(self.game.state)
        # Based on input, the game updates itself (through env.step())
        self.game.step(a)
        # We show the new state and everything, and see if the game is over
        self.game.render()

        # - If it is, deal with it accordingly
        # - If not, keep going

    def _take_player_input(self):
        return 0
    
    def _play_loop(self):
        return 0

    def _get_and_validate_input(self, msg):
        got_valid_input = False
        while not got_valid_input:
            inp = input(msg)
            satisfied_with_input = self._get_y_n("Are you satisfied with this input?")
            if satisfied_with_input:
                return inp
    
    def _get_y_n(self, msg):
        got_valid_input = False
        while not got_valid_input:
            inp = input(msg + " y/n\n")
            if inp.casefold() == "y".casefold():
                return True
            elif inp.casefold() == "n".casefold():
                return False
            else:
                print("Input was not valid. Please input again!\n")

