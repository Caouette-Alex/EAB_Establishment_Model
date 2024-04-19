# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 14:55:16 2023

@author: alexp
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

os.chdir("../")
os.chdir("C:/Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Model_results/")

df = pd.read_excel('global_sen_anal_2023-05-01.xls',sheet_name='first_Si',index_col=0)
df.drop(labels='Campground reservation eveness',inplace=True)
df.sort_values(by='S1',ascending = False,inplace = True)
df.rename(index={'Travel distance probability':'Halving distance',
                 'Probability of live beetles in ash wood':'EAB infested firewood',
                 'Firewood sourced from outside park':'Firewood source',
                 'Per capita reservation rate':'Reservation rate',
                 'Propagule pressure threshold': 'Allee effect threshold',
                 'Campground reservation distribution eveness':'Campground reservations',
                 'Burning probability of emerald ash borer firewood':'Firewood burn',
                 'Timing of eab emergence':'EAB emergence'},inplace=True)

fig,ax = plt.subplots()

ax.barh(df.index,df['S1'],xerr=df['S1_conf'],capsize=3, color='dimgray')
ax.set_xlabel('Sensitivity index',fontsize=12)
ax.spines[['right', 'top']].set_visible(False)

#ax.set_xticklabels(df.index,rotation=45,ha='right',fontsize=12)

plt.savefig('first_order_indices.png',dpi=300,bbox_inches='tight')