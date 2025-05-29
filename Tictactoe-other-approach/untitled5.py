# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 12:39:18 2022

@author: mashi
"""

o = 0
x = 2
E = 1

obs = [o,x,o, 
       x,o,x, 
       E,E,E]

def two_one(two, one):
        two_list = []
        one_list = []
        lines = ((0,1), (0,2), (1,2), 
                 (3,4), (3,5), (4,5),
                 (6,7), (6,8), (7,8),
                 (0,3), (0,6), (3,6), 
                 (1,4), (1,7), (4,7),
                 (2,5), (2,8), (5,8),
                 (0,4), (0,8), (4,8), 
                 (2,4), (2,6), (4,6))
        open_spot = (2,1,0, 5,4,3, 8,7,6, 6,3,0, 7,4,1, 8,5,2, 8,4,0, 6,4,2)
        for i in range(24):
            l = lines[i]
            two_cond = obs[l[0]] == obs[l[1]] == two
            one_cond = obs[open_spot[i]] == one
            print("two_cond,", two_cond, "one_cond", one_cond)
            if two_cond and one_cond:
                two_list = two_list + [l[0], l[1]]
                one_list.append(open_spot[i])
        return two_list, one_list
    
print(two_one(o,E))




