# -*- coding: utf-8 -*-
"""
Created on Thu May 19 17:08:14 2022

@author: alexp
"""

import pandas as pd
from matplotlib import pyplot as plt
import os
import numpy as np
from sklearn.linear_model import LinearRegression

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model')


df = pd.read_excel('Arcmap/Camping_reservations/pop_centr_counts.xls')
city_df = pd.read_csv('Coding/Camping_data/Cities_Master_2021-12-07.csv').sort_values(by='Geographic_Name').reset_index()

merge_df = pd.merge(city_df,df,left_on='Geographic_Name',right_on=('PCNAME'))

merge_df = merge_df[merge_df['Province'] == 'NB']


##Drop Fredericton as it's an outlier
#merge_df = merge_df[merge_df.PCNAME != 'Fredericton']

plt.scatter(merge_df['Population'], merge_df['Count_'])
#x = 
#y = 

from scipy.stats import pearsonr
corr, _ = pearsonr(x,y)
print('Pearsons correlation: %.3f' % corr)


#%%
x = merge_df[['Population']].to_numpy()
#df['log_pop/dist'] =  df['log_pop']/df['log_dist']
y = merge_df[['Count_']].to_numpy()

#%%

model = LinearRegression()
model.fit(x,y)
model = LinearRegression().fit(x,y)

r_sq = model.score(x,y)
print('coefficient of determination:', r_sq)
itrcpt = model.intercept_

slp = model.coef_

print('y=',slp,'x+',itrcpt)
