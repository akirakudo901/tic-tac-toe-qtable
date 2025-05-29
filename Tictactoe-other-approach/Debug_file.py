# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 13:36:50 2022

@author: mashi
"""

def my_assert(exp1, exp2):
    if exp1 == exp2:
        print("Test passed.")
    else:
        print("Actual value, {}, was different from expected value, {}.".format(exp1, exp2))
    

from math import inf
from Gym_tailored_Tictactoe_env import Tictactoe
import copy

p_inf = inf
n_inf = -inf

circle = o = 0
empty  = E = 1
cross  = x = 2

env = Tictactoe()


class Node():
    def __init__(self, state, reward, best_action, children):
        self.state = state
        self.reward = reward
        self.best_action = best_action
        self.children = children
    
    def props(self):
        print("State:{}, reward:{}, best_action:{}, children:{}".format(self.state, self.reward, self.best_action, self.children))

initial = Node([E]*9, n_inf, 99, {}) #0
node1 = Node([o,x,o,
              x,o,x,
              E,E,E], n_inf, 99, {}) #1
node2 = Node([o,x,o,
              x,o,E,
              E,E,E], p_inf, 99, {}) #0
node3 = Node([o,x,o,
              o,x,E,
              E,E,E], p_inf, 99, {}) #-1
node4 = Node([x,x,o,
              o,o,x,
              x,o,E], n_inf, 99, {}) #draw

node_t_1 = Node([o,x,o,
                 x,o,x,
                 o,E,E], 1, 99, {}) #1
node_t_2 = Node([o,x,o,
                 x,o,E,
                 x,E,E], n_inf, 99, {}) #0
node_t_3 = Node([o,x,o,
                 o,x,E,
                 E,x,E], -1, 99, {}) #-1
node_t_4 = Node([x,x,o,
                 o,o,x,
                 x,o,o], 0.5, 99, {}) #draw


initial_turn = o


def get_reward(n, a):
    copy_n = copy.deepcopy(n)    #making a copy so that old node is not updated through step()
    env.set_state(copy_n.state)  #update env so that we can then apply env.step()
    win_r  = env.win_r
    loss_r = env.loss_r
    i_t = initial_turn
    
    new_state, g_r, _, _ = env.step(a)
    #WIN & circle / LOSS & cross  ->  1
    #WIN & cross  / LOSS & circle -> -1
    #s is win
    if   ((g_r == win_r) and (i_t == circle)) or ((g_r == loss_r) and (i_t ==  cross)):
        return 1
    #s is loss
    elif ((g_r == win_r) and (i_t ==  cross)) or ((g_r == loss_r) and (i_t == circle)):
        return -1
    #s is draw
    elif (empty not in new_state):
        return 0.5
    #s is not terminal
    else:
        next_turn = env.get_turn(new_state)
        if initial_turn == next_turn: #next is our turn
            return n_inf
        else:                         #next is enemy's turn
            return p_inf
"""
my_assert(get_reward(initial, 1), p_inf) #not done
my_assert(get_reward(node1, 6), 1) #win
my_assert(get_reward(node2, 5), n_inf) #not done
my_assert(get_reward(node3, 7), -1) #loss
my_assert(get_reward(node4, 8), 0.5) #draw
"""

def is_terminal(n):
    #A state is terminal if it is either: WON, LOST, or DRAW
    s = n.state
    
    #DRAW
    if (empty not in s):
        return True
    #WON/LOST
    result = False
    lines = ((0,1,2), (3,4,5), (6,7,8),
             (0,3,6), (1,4,7), (2,5,8),
             (0,4,8), (2,4,6))
    for l in lines:
        if (s[l[0]] == s[l[1]] == s[l[2]]) and (s[l[0]] != empty):
            result = True
            break
    return result

"""
my_assert(is_terminal(initial), False) #not done
my_assert(is_terminal(node_t_1), True) #win
my_assert(is_terminal(node_t_2), False) #not done
my_assert(is_terminal(node_t_3), True) #loss
my_assert(is_terminal(node_t_4), True) #draw
"""
#!!!
#This is not working;;
#Am still not sure about what shallow & deep copy means and how we should deal with that
def children_nodes(n):
    empty_spots = env.obtain_empty_spots(n.state)
    children = {}
    
    for a in empty_spots:
        s = copy.deepcopy(n.state)
        env.set_state(s)
        n_s, _, _, _ = env.step(a)
        new_node = Node(n_s, get_reward(n, a), 99, {})
        if not (is_terminal(new_node)):
            new_node.children = children_nodes(new_node)
        
        children[a] = new_node
    
    return children
    """
    1) obtain empty spots
    2) for each, obtain new state using env.step
    3) make the new nodes based on info from env.step and return a list of that
    """
"""
children1 = children_nodes(initial)
children2 = children_nodes(node1)

print("Children 1:")
for child in children1:
    child.props()
print("Children 2:")
for child in children2:
    child.props()
"""

def uncalibrated_tree(n):
    children = children_nodes(n)
    new_node = Node(n.state, n.reward, n.best_action, children)
    return new_node

"""
u_tree = uncalibrated_tree(node1)
u_tree.props()
for child in u_tree.children.values():
    child.props()
    for child2 in child.children.values():
        child2.props()
        for child3 in child2.children.values():
            child3.props()
"""

def best_reward_and_action(n, is_ally):
    reward = n.reward
    action = 0
    for act in n.children.keys():
        child = n.children[act]
        if is_terminal(child):
            if is_ally:        #maximize
                if reward <= child.reward:
                    reward = child.reward
                    action = act
            elif not is_ally: #minimize
                if reward >= child.reward:
                    reward = child.reward
                    action = act
        else: #not terminal
            calibrated_child = calibrate_tree(child)
            n.children[act] = calibrated_child
            if is_ally:        #maximize
                if reward <= calibrated_child.reward:
                    reward = calibrated_child.reward
                    action = act
            elif not is_ally: #minimize
                if reward >= calibrated_child.reward:
                    reward = calibrated_child.reward
                    action = act
        
    return reward, action

"""
new_node = uncalibrated_tree(initial)
print(best_reward_and_action(new_node, True))
"""

def calibrate_tree(n):
    """
    Backpropagates the reward & best actions according to tree gained previously
    Go as deep as possible first if nodes are not terminal. Once we find a terminal node,
    backpropagate its value by sending the value and action to the node above.
    The node above takes the values and update its own value accordingly, which is sent higher.
    A parent node's reward and action are updated if:
    1) Turn is enemy -> reward is smaller than current. Reward to new, action to new.
    2) Turn is ally  -> reward is bigger. reward & action updated.
    """
    
    turn = env.get_turn(n.state)
    if turn == initial_turn:
        is_ally = True
    else:
        is_ally = False
    
    reward, best_action = best_reward_and_action(n, is_ally)
    calibrated_node = Node(n.state, reward, best_action, n.children)
    return calibrated_node

"""
new_node = uncalibrated_tree(node1)
calibrate_tree(new_node).props()

u_tree = uncalibrated_tree(node3)
u_tree = calibrate_tree(u_tree)
u_tree.props()
for child in u_tree.children.values():
    child.props()
    for child2 in child.children.values():
        child2.props()
        for child3 in child2.children.values():
            child3.props()
"""