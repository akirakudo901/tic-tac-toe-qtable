# Tic tac toe agent playing optimally using a Q table
This repo implements a Q-table learning agent which learns iteratively to choose the best strategy against a minimax computer (which itself plays optimally), such that it ultimately draws every game!

- ai_training.py - Executes the Q-table agent learning when run.
- environment.py - Specifies the reinforcement learning environment (Tic tac toe game) in which we train the agent.
- minimax.py - Builds a minimax computer algorithm which plays optimally in a game of Tic tac toe.
- play_tictactoe.py - A console version that makes use of environment.py to allow playing a game of Tic tac toe against either a trained q-table agent or a minimax agent.
- qtable.py - A class describing the Q-table used by the Q-learning agent.
