# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 14:30:41 2021

@author: mashi

The AI side file.
"""

import Tictactoe as ttt

from rl.agents.dqn import DQNAgent
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory


#|
env = ttt.Tictactoe()
# Training parameters.
max_eps_steps = 10000 # define maximal episode steps

time_limit = True
buffer_size = 200000  # observation history size
batch_size = 25  # mini batch size sampled from history at each update step
nb_actions = len(env.action_space)
window_length = 1

# construct a MLP
model = Sequential()
model.add(Dense(4, input_shape=(env.observation_size, ), activation='relu')) # input layer?? made it myself
model.add(Dense(32, activation='relu'))  # hidden layer 1
#model.add(Dense(32, activation='relu'))  # hidden layer 2; if we need it
model.add(Dense(nb_actions, activation='linear'))  # output layer

memory = SequentialMemory(limit=200000, window_length=window_length)
policy = LinearAnnealedPolicy(EpsGreedyQPolicy(eps=0.2), 'eps', 1, 0.05, 0, 50000)
#||

dqn = DQNAgent(model=model,
               policy=policy,
               nb_actions=nb_actions,
               memory=memory,
               gamma=0.99,
               batch_size=25,
               train_interval=1,
               memory_interval=1,
               target_model_update=1000,
               nb_steps_warmup=10000,
               enable_double_dqn=True)

dqn.compile(Adam(lr=1e-4),
            metrics=['mse'])

history = dqn.fit(
    env,
    nb_steps=100000,
    action_repetition=1,
    verbose=2,
    visualize=True,
    nb_max_episode_steps=10000,
    log_interval=1000
    )

env.reset()
test_history = dqn.test(env,
                        nb_episodes=5,
                        nb_max_episode_steps=100000,
                        visualize=True
                        )

def comp1(inp, turn):
    result = dqn(inp, turn)
    return result

def play(ai_type):
    def ai(inp, turn, ai_type):
        if ai_type == "comp1":
            result = comp1(inp, turn)
        return result

    game = ttt.Tictactoe()
    while game.end_condition == False:
        next_step = ai(game.observation(), game.turn, ai_type)
        game.step(next_step)
    return game.state()


play("comp1")