# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 19:26:19 2022

@author: mashi
"""

from math import inf
import environment as tttenv
from qtable import state_to_number
import copy
import json
import random as rd
from time import localtime, time

P_INF = inf
N_INF = -inf

EMPTY  = E = tttenv.EMPTY
CIRCLE = O = tttenv.CIRCLE
CROSS  = X = tttenv.CROSS

LOOKUP_TABLE_PATH = "tictactoeai/qtable/minimax_lookup_table_Tictactoe2023_2_23_14_49.json"

class Node():
    def __init__(self, state, reward, best_action, children):
        self.state = state
        self.reward = reward
        self.best_action = best_action
        self.children = children
    
    def __str__(self):
        def _child_state_to_string(child):
            acc = "["; [acc := acc + str(x) + ", " for x in child.state]; acc += "]"
            return acc

        def _children_to_string(children):
            acc = "\n"; [acc := acc + str(key) + " : " + _child_state_to_string(children[key]) + "\n" 
                            for key in children.keys()]
            return acc
        
        return ("State:" + _child_state_to_string(self) + "\nreward:" + str(self.reward) + 
                "\nbest action:" + str(self.best_action) + 
                "\nchildren:" + _children_to_string(self.children))
    
    def state_tree(self):
        """
        Creates the whole tree of possible moves from the given state, 
        mapping out all the rewards. It will then given each node the 
        best action to take next and its reward, so that by following
        the best actions in the nodes, one can take the optmial minimax 
        strategy in that tree.
        
        I will do this in two steps: 1) I create the entire tree without 
        right reward and action.
        2) I readjust the reward and actions to be the right ones.
        """
        
        initial_turn = tttenv.get_turn(self.state)
        
        def _is_terminal(n):
            #A state is terminal if it is either: WON, LOST, or DRAW
            s = n.state
            
            #DRAW
            if (EMPTY not in s):
                return True
            else:
                #WON/LOST
                lines = ((0,1,2), (3,4,5), (6,7,8),
                        (0,3,6), (1,4,7), (2,5,8),
                        (0,4,8), (2,4,6))
                for L in lines:
                    first, second, third = L[0], L[1], L[2]
                    if (s[first] == s[second] == s[third] != EMPTY):
                        return True
                    
                return False
        
        def _children_nodes(n):
            empty_spots = tttenv.Tictactoe.get_empty_squares(n.state)
            children = {}
            
            for a in empty_spots:
                n_s, _, _, _ = tttenv.Tictactoe.simulate_step(n.state, a)
                new_node = Node(n_s, Node._get_reward(n, a, initial_turn), 9999, {})
                if not _is_terminal(new_node):
                    new_node.children = _children_nodes(new_node)
                
                children[a] = new_node
            
            return children
        
        def _uncalibrated_tree(n):
            children = _children_nodes(n)
            new_node = Node(n.state, n.reward, n.best_action, children)
            return new_node
        #Functions for first part (make uncalibrated tree) until here
        #==============================================================
        
        def _best_reward_and_action(n, is_ally):
            reward = n.reward
            action = []
            for act in n.children.keys():
                child = n.children[act]
                # if not terminal
                if not _is_terminal(child):
                    #adjust whole tree below node first
                    child = _calibrate_tree(child)
                    n.children[act] = child
                #then update node's reward
                # if action is bigger than before
                if is_ally and reward < child.reward:
                    #maximize
                    reward = child.reward
                    action = [act]
                elif not is_ally and reward > child.reward:
                    #minimize
                    reward = child.reward
                    action = [act]
                elif reward == child.reward: # then reward is the same as our current best
                    action.append(act)
                
            return reward, action
        
        def _calibrate_tree(n):
            """
            Backpropagates the reward & best actions according to tree gained previously
            Go as deep as possible first if nodes are not terminal. Once we find a terminal node,
            backpropagate its value by sending the value and action to the node above.
            The node above takes the values and update its own value accordingly, which is sent higher.
            A parent node's reward and action are updated if:
            1) Turn is enemy -> reward is smaller than current. Reward to new, action to new.
            2) Turn is ally  -> reward is bigger. reward & action updated.
            """

            turn = tttenv.get_turn(n.state)
            if turn == initial_turn:
                is_ally = True
            else:
                is_ally = False
            
            reward, best_action = _best_reward_and_action(n, is_ally)
            calibrated_node = Node(n.state, reward, best_action, n.children)
            return calibrated_node
        
        #Functions for second part (calibrate the tree) until here
        #============================================================
        
        #first part; making the tree
        uncal_tree = _uncalibrated_tree(self)
        #second part; calibrating the tree
        result = _calibrate_tree(uncal_tree)
        
        return result
    
    # Helpers for state_tree
    # Gets the reward as fitting this Node class, given a node, action and initial turn
    def _get_reward(n, a, initial_turn):
            copy_n = Node(n.state, n.reward, n.best_action, n.children)
            win_r  = tttenv.REWARD_FOR_WIN
            loss_r = tttenv.REWARD_FOR_LOSS
            i_t = initial_turn
            
            new_state, g_r, _, _ = tttenv.Tictactoe.simulate_step(n.state, a)
            #WIN & circle / LOSS & cross  ->  1
            #WIN & cross  / LOSS & circle -> -1
            #s is win
            if ((g_r is win_r and i_t is CIRCLE) 
                    or (g_r is loss_r and i_t is CROSS)):
                return 1
            #s is loss
            elif ((g_r is win_r and i_t is CROSS) 
                    or (g_r is loss_r and i_t is CIRCLE)):
                return -1
            #s is draw
            elif (EMPTY not in new_state):
                return 0.5
            #s is not terminal
            else:
                next_turn = tttenv.get_turn(new_state)
                if initial_turn == next_turn: #next is our turn
                    return N_INF
                else:                         #next is enemy's turn
                    return P_INF


    def tree_to_dict(self, tree=None):
        """
        Takes a state-action tree for Tic tac toe and convert it into a lookup table that is
        a dictionary with state_number as keys and best action as values.
        
        If tree is None, generates a state-action tree from this node and stores it.
        """
        
        def _node_to_dict(n, table):
            state_num = state_to_number(n.state)
            table[state_num] = n.best_action
            for child in n.children.values():
                table = _node_to_dict(child, table)
            return table
        
        if tree == None:
            tree = self.state_tree()
        
        table = {}
        data = _node_to_dict(tree, table)
        
        time_tuple = localtime(time())[0:5]
        acc = str(time_tuple[0]); [acc := acc + "_" + str(x) for x in time_tuple[1:5]]
        name_original = "minimax_lookup_table_Tictactoe" + acc + ".json"
        success = False

        while success == False:
            inp = input("Do you want to keep this data as a JSON file? YES/NO \n")
            if inp == "YES":
                with open(name_original, "w") as write_file:
                    json.dump(data, write_file)
                success = True
            elif inp == "NO":
                success = True
            else:
                print("The input may have been neither YES nor NO.")


class Minimax_computer:
    def __init__(self, lookup_table=LOOKUP_TABLE_PATH):
        success = False
        while not success:
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
                
        def _random_choice():
            empties = []
            for i in range(9):
                if state[i] == EMPTY: 
                    empties.append(i)
            return rd.sample(empties, 1)[0]
        
        def _optimal_choice():
            state_number = state_to_number(state)
            a = rd.sample(self.table[str(state_number)], 1)[0]
            return a
        
        random_val = rd.random()
        if p > random_val:
            result = _random_choice()
            is_random_choice = True
        else:
            result = _optimal_choice()
            is_random_choice = False
        return result, is_random_choice

    def load(self, lookup_table="minimax_lookup_table_Tictactoe2022_1_18_11_0.json"):
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
        

# Creating a tree of Q table
# if __name__ == "__main__":
# initial = Node([E]*9, N_INF, [], {})
# node1 = Node([O,X,O,
#               X,O,X,
#               E,E,E], N_INF, [], {})
#     st = state_tree(initial)
#     tree_to_dict(st)