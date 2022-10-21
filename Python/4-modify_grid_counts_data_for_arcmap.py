# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 11:06:02 2022

@author: alexp
"""
import pandas as pd
import os
from datetime import datetime
import seaborn as sns

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model')

grid_2_df,grid_6_df  = pd.read_excel("Model_results/Sim_2022-10-11_1000[20]invas_grid_counts.xls", sheet_name = '2grid_counts', index_col = 0), pd.read_excel("Model_results/Sim_2022-10-11_1000[20]invas_grid_counts.xls", sheet_name = '6grid_counts', index_col = 0)

d = {'grid_2_df':grid_2_df,'grid_6_df':grid_6_df}
d_2 = {}
for k,v in d.items():
    v = v.mask(v > 1, 1)
    n_v = v.drop(columns = 'total_counts')
    d_2[k] = n_v.transpose().fillna(0).describe(include='all').transpose()

for k,v in d_2.items():
    path = 'model_results/'+k +'_'+ datetime.today().strftime('%Y-%m-%d')+'.csv'
    v.to_csv(path)
    
#%% Proportion of locations with EAB infestations
d_3={}

for k,v in d.items():
    v = v.mask(v > 1, 1)
    v = v[v['total_counts'].notna()]
    d_3[k] = v.fillna(0).describe()

test = pd.DataFrame()
for k,v in d_3.items():
    mean_val = v.drop(columns='total_counts').transpose()
    mean_val = mean_val['mean'].describe()
    name = k[5]
    test[name] = mean_val


test = test.transpose()    
ax = sns.barplot(data = test, x = test.index, y = 'mean', color=sns.color_palette('pastel')[0])
ax.errorbar(x =[0,1], y = test['mean'], yerr = test['std'],fmt='none',c = 'k')
sns.despine()
ax.set_ylabel('Proportion of infested locations')
ax.set_xlabel('Establishment threshold')
#mean proportion of locations with EAB infestations


