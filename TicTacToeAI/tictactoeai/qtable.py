# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 10:06:39 2022

@author: mashi
"""

import time
import numpy as np


def log(Q, save_table=False, name=""):
    time_of_creation = time.localtime(time.time())[0:5]
    acc = str(time_of_creation[0])
    [acc := acc + "_" + str(x) for x in time_of_creation[1:5]]
    name_original = "Tictactoe_Q_table_" + acc
    
    if save_table is True:
        if name == "":
            np.save(name_original, Q)
        else:
            np.save(name, Q)
    elif save_table is False:
        pass
    
def state_to_number(s):
    """
    Each state will be given a unique number in the following way:
     Putting the ith number in the state list as ni, a state's unique number
     will be calculated as:
       number = SUM(ni * 3^(9-i)) for (0<i<9)
       E.g. [0,1,0,2,2,0,0,1,0] = 1(3^7) + 2(3^5) + 2(3^4) + 1(3^1) = 2838
    """
    result = 0
    for i in range(9):
        result += s[i] * (3**(8-i))
    return result

def number_to_state(num):
    """
    Converts the unique numbers attributed with the state_to_number method
    back to the corresponding states.
    """
    result = []
    q = 0
    r = num
    for i in range(9):
        q, r = divmod(r, (3**(8-i)))
        result.append(q)
    return result