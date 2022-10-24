# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 15:23:58 2022

@author: alexp
"""

import pandas as pd
import numpy as np
import ast
d_1 = {}
for num in range(2):    
    d_1[num] = pd.read_excel('Sim_2022-10-21_2[20]Introduction.xls',index_col = 0,sheet_name=num)


#for column in df:
for k,v in d_1.items():
    for index,row in v.iterrows():
        for i in range(20):
            if isinstance(row[i],str):
                
                
                d = ast.literal_eval(row[i])
                t = sum(d.values())
                v.loc[index,i] = t
d_2 = {}
for k,v in d_1.items():
    out= v.groupby('Grid_ID').sum()
    d_2[k]= (out.transpose().describe().transpose())['mean']
df = pd.concat(d_2, axis = 1)
#d = { k: v for k, v in d_2.items()}
#describe_df.to_csv('propagule_pressure.csv')