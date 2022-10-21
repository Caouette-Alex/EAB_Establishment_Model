# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 11:06:02 2022

@author: alexp
"""
import pandas as pd

grid_list = []
for letter in list(map(chr,range(65,79))):
    for num in range(9):
        grid_list.append(letter+'-'+str(num+1))

grid_df = pd.DataFrame(index=grid_list)
