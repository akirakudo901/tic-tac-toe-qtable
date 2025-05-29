# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 13:59:29 2021

@author: mashi
"""

from math import exp

o_vector = [1,4,6,3,4,7,2,9]

def softmax(vector):
    sum_exp = 0
    n_vec = []
    result = []
    for val in vector:
        exp_val = round(exp(val), 2)
        n_vec.append(exp_val)
        sum_exp += exp_val
    for val in n_vec:
        result.append(round( (val / sum_exp), 2))
    print("Result:", result, "; Sum_exp:", sum_exp, "; New_vector:", n_vec)

softmax(o_vector)