# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 15:23:58 2022

@author: alexp
"""

import pandas as pd
import numpy as np
import ast
import time
d_1 = {}
start = time.process_time()
d_1 = {}
for num in range(1000):  
    print(num)
    d_1[num] = pd.read_excel('Sim_2022-10-24_1000[20]Introduction.xls', index_col = 0, sheet_name=num, usecols=[0, 1, 6, 11, 16, 21], names  = ['Campground','Grid_ID','5','10','15','20'])
print(time.process_time() - start)
# TODO move below once code has run
d_4 = d_1.copy()
#%%

### TODO Remove after running code
import os
os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/')
camp_df = pd.read_csv('Coding/Camping_data/Parks_and_camping_Master_2022-10-06.csv')
camp_df = camp_df[['Name', 'Grid_ID']]

d_4 = {}
for k,df in d_1.items():
    x = df.merge(camp_df,left_index = True, right_on=camp_df['Name'])
    x = x[['Grid_ID','5','10','15','20']]
    d_4[k] = x
###


l= ['5','10','15','20']
#for column in df:
d_2 = {}
for k,v in d_4.items():
    print(k)
    for index,row in v.iterrows():
        for i in l:
            if isinstance(row[i],str):
                d = ast.literal_eval(row[i])
                t = sum(d.values())
                v.loc[index,i] = t
                #d_2[i] = t
for k,v in d_4.items():
    d_4[k] = v.set_index('Grid_ID').sum(level=0)

from operator import itemgetter
#df_concat = pd.concat(itemgetter(0,1)(d_4))
df_concat = pd.concat((d_4.values()))

#df_concat = pd.concat((d_4[0,1]))
by_row_index= df_concat.groupby(df_concat.index)
df = by_row_index.mean()
df_std = by_row_index.std().rename(columns={'5':'5_std','10':'10_std','15':'15_std', '20':'20_std'})
df_ste = by_row_index.sem().rename(columns={'5':'5_ste','10':'10_ste','15':'15_ste', '20':'20_ste'})

df = df.join([df_std,df_ste])

df.to_csv('Model_results/propagule_pressure.csv')

