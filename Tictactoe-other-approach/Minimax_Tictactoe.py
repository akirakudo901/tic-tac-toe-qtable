# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 03:23:48 2022

@author: mashi

Trying to implement the minimax algorithm!
Not sure how deep the algorithm is supposed to go before determining its moves;
from definition it seems like it has to go through all the tree before
actually taking actions???

THIS ALGORITHM IS NOT MADE TO BE USED TO PLAY A GAME MIDWAY; FROM NATURE, IT NEEDS TO START
THE GAME FROM THE INITIAL TO WORK (I THINK, FOR NOW)

As minimax;
1) Go deeper into the tree structure.
2) As we go, we keep track of the turn.
-) When making a new node, check if it is terminal by calling "terminal?"
-) Once you find a 
3) If a depth is your turn, maximize reward
4) Otherwise, minimize the enemy reward

    Each node has 1- state; 2- reward; 3- action leading to best reward
    The tree goes deeper and deeper.
    As it goes deep, it creates it's possible children nodes, updating turns.
    Non-terminal nodes have either a reward of +inf (enemy turn) or -inf (our turn).
    Once we reach a terminal node, we assess what it's reward is.
    Then we backpropagate that value back.
    A parent node's reward and action are updated if:
        1) Turn is enemy -> reward is smaller than current. Reward to new, action to new.
        2) turn is us -> reward is bigger. reward & action updated.
"""

from math import inf
from Gym_tailored_Tictactoe_env import Tictactoe
import copy
import json
import random as rd
from time import localtime, time

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


initial = Node([1,1,1,1,1,1,1,1,1], n_inf, [], {})
node1 = Node([o,x,o,
              x,o,x,
              E,E,E], n_inf, [], {})

def state_tree(n0):
    """
    Creates the whole tree of possible moves from the given state, mapping out all the rewards.
    It will then given each node the best action to take next and its reward, so that by following
    the best actions in the nodes, one can take the optmial minimax strategy in that tree.
    
    I will do this in two steps: 1) I create the entire tree without right reward and action.
    2) I readjust the reward and actions to be the right ones.
    """
    
    initial_turn = env.get_turn(n0.state)
    
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
    
    def uncalibrated_tree(n):
        children = children_nodes(n)
        new_node = Node(n.state, n.reward, n.best_action, children)
        return new_node
    #Functions for first part (make uncalibrated tree) until here
    #==============================================================
    
    def best_reward_and_action(n, is_ally):
        reward = n.reward
        action = []
        for act in n.children.keys():
            child = n.children[act]
            if is_terminal(child):
                if is_ally:        #maximize
                    if reward <= child.reward:
                        reward = child.reward
                        action.append(act)
                elif not is_ally: #minimize
                    if reward >= child.reward:
                        reward = child.reward
                        action.append(act)
            else: #not terminal
                calibrated_child = calibrate_tree(child)
                n.children[act] = calibrated_child
                if is_ally:        #maximize
                    if reward <= calibrated_child.reward:
                        reward = calibrated_child.reward
                        action.append(act)
                elif not is_ally: #minimize
                    if reward >= calibrated_child.reward:
                        reward = calibrated_child.reward
                        action.append(act)
            
        return reward, action
    
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
    
    #Functions for second part (calibrate the tree) until here
    #============================================================
    
    #first part; making the tree
    uncal_tree = uncalibrated_tree(n0)
    #second part; calibrating the tree
    result = calibrate_tree(uncal_tree)
    
    return result

def state_to_number(s):
    #Each state will be given a unique number in the following way:
    #starting from the first number in the array, the first one is a 3^8.
    #one less is 3^7, etc.; the nth number (1st is 1) is 3^(9-n)
    #you add all of them to give a unique number:
        #E.g. [0,1,0,2,2,0,0,1,0] = 1(3^7) + 2(3^5) + 2(3^4) + 1(3^1) = 2838
    result = 0
    for i in range(9):
        result += s[i] * (3**(8-i))
    return result

def number_to_state(num):
    result = []
    q = 0
    r = num
    for i in range(9):
        q, r = divmod(r, (3**(8-i)))
        result.append(q)
    return result

def tree_to_dict(tree):
    """
    Takes a state-action tree for Tic tac toe and convert it into a lookup table that is
    a dictionary with state_number as keys and best action as values.
    """
    
    def node_to_dict(n, table):
        state_num = state_to_number(n.state)
        table[state_num] = n.best_action
        for child in n.children.values():
            table = node_to_dict(child, table)
        return table
    
    table = {}
    data = node_to_dict(tree, table)
    
    time_tuple = localtime(time())[0:5]
    acc = str(time_tuple[0]); [acc := acc + "_" + str(x) for x in time_tuple[1:5]]
    name_original = "minimax_lookup_table_Tictactoe" + acc + ".json"
    success = False
    while success == False:
        inp = input("Do you want to keep this data as a JSON file? YES/NO")
        if inp == "YES":
            with open(name_original, "w") as write_file:
                json.dump(data, write_file)
            success = True
        elif inp == "NO":
            success = True
        else:
            print("The input may have been neither YES nor NO.")

#tree designating best move when minimax starts from "o" turn

#tree = state_tree(initial)

#tree = state_tree(node1)
#tree_to_dict(tree)

#list of tree deisignating best move when minimax starts from "x" turn; 0th is when 0 is selected, etc.
"""
first_states = [[o,E,E,
                 E,E,E,
                 E,E,E],
                [E,o,E,
                 E,E,E,
                 E,E,E],
                [E,E,o,
                 E,E,E,
                 E,E,E],
                [E,E,E,
                 o,E,E,
                 E,E,E],
                [E,E,E,
                 E,o,E,
                 E,E,E],
                [E,E,E,
                 E,E,o,
                 E,E,E],
                [E,E,E,
                 E,E,E,
                 o,E,E],
                [E,E,E,
                 E,E,E,
                 E,o,E],
                [E,E,E,
                 E,E,E,
                 E,E,o]]
first_nodes = [Node(state, p_inf, 99, {}) for state in first_states]
cross_tree = [state_tree(n0) for n0 in first_nodes] 
"""

class Minimax_computer:
    def __init__(self, lookup_table="minimax_lookup_table_Tictactoe2022_1_9_22_35.json"):
        success = False
        while success == False:
            if not lookup_table.endswith(".json"):
                lookup_table += ".json"
            with open(lookup_table, "r") as read_file:
                try:
                    self.table = json.load(read_file)
                    success = True
                except:
                    print("Load was unsuccessful. The file should be a json object ending with \".json\".")
                    lookup_table = input("Please input the file you want to use as lookup table.")
            
        print("Load of lookup table successful.")
        
    def action(self, state, p=0):
        """
        Minimax algorithm takes action based on the table, or otherwise a random action with probability
        "probability".
        """
        while p < 0 or p > 1:
            p = input("The given probability is invalid. Please input a value between 0 and 1.")
                
        def random_choice():
            empties = []
            for i in range(9):
                if state[i] == 1:
                    empties.append(i)
            return rd.sample(empties, 1)[0]
        
        def optimal_choice():
            state_number = state_to_number(state)
            a = rd.sample(self.table[str(state_number)], 1)[0]
            return a
        
        random_val = rd.random()
        if p > random_val:
            result = random_choice()
        else:
            result = optimal_choice()
        return result

    def load(self, lookup_table="minimax_lookup_table_Tictactoe2022_1_9_22_35.json"):
        success = False
        while success == False:
            if not lookup_table.endswith(".json"):
                lookup_table += ".json"
            with open(lookup_table, "r") as read_file:
                try:
                    self.table = json.load(read_file)
                    success = True
                except:
                    print("Load was unsuccessful. The file should be a json object ending with \".json\".")
                    lookup_table = input("Please input the file you want to use as lookup table.")
            
        print("Load of lookup table successful.")


"""
with open("minimax_lookup_table_Tictactoe2022_1_9_22_35.json", "r") as read_file:
    table = json.load(read_file)
print(table)
new_table = {}
for key in table.keys():
    state = number_to_state(int(key))
    new_table[key] = (state, table[key])
print(new_table)
"""