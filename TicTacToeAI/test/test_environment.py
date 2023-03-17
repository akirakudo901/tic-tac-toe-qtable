"""
Tests functionalities in the environment.py file related to TicTacToe.
VERY NOT FINISHED!
"""

import unittest
import environment
from environment import Tictactoe

E = environment.EMPTY
O = environment.CIRCLE
X = environment.CROSS

class TestTictactoe(unittest.TestCase):

    def setUp(self):
        self.s1 = [E, E, E,
              E, E, E,
              E, E, E]
    
    def test_simulate_step(self):
        return

    def test_step(self):
        return

    # render() is an ui function

    def test_get_empty_squares(self):
        actual = Tictactoe.get_empty_squares(self.s1)
        self.assertEquals(list(range(9)), actual)
        return

    def test_get_turn(self):
        return

    def test_is_terminal(self):
        return


if __name__ == "__main__":
    unittest.main()