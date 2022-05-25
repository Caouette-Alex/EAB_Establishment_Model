# -*- coding: utf-8 -*-
"""
Created on Fri May 20 10:45:42 2022

@author: alexp
"""

import pandas as pd

import os

from matplotlib import pyplot as plt

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model')
list = [2015, 2016,2017, 2018, 2019, 2020]
city_df = pd.read_csv('Coding/Camping_data/Cities_Master_2021-12-07.csv').sort_values(by='Geographic_Name').reset_index()
l=[]
d={}
for year in list:
    name = 'df_'+ str(year)
    file = 'Arcmap/Camping_reservations/' + str(year) +'_pop_cent_reserv.xls'
    pd_file = pd.read_excel(file)
    merge_df = pd.merge(city_df, pd_file,left_on='Geographic_Name',right_on=('PCNAME'))
    merge_df = merge_df[merge_df['Province'] == 'NB']#Arcmap.set_index('PCNAME')  
    d[name] = merge_df    
    l.append(merge_df)
    
df = pd.concat(l).groupby(level=0).mean()

df.plot('Population', 'Count_', kind='scatter')


#%%
x=df['Population']
y= df['Count_']

from scipy.stats import pearsonr
corr, _ = pearsonr(x,y)
print('Pearsons correlation: %.3f' % corr)


#%%
df_ = pd.read_excel('Arcmap/Camping_reservations/2015_pop_cent_reserv.xls')
df_2016 = pd.read_excel('Arcmap/Camping_reservations/2016_pop_cent_reserv.xls')
df_2017 = pd.read_excel('Arcmap/Camping_reservations/2017_pop_cent_reserv.xls')
df_2018 = pd.read_excel('Arcmap/Camping_reservations/2018_pop_cent_reserv.xls')
df_2019 = pd.read_excel('Arcmap/Camping_reservations/2019_pop_cent_reserv.xls')
df_2020 = pd.read_excel('Arcmap/Camping_reservations/2020_pop_cent_reserv.xls')

import numpy as np
fig, ax = plt.subplots(1,5,figsize=(30,5))

def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x'], point['y'], str(point['val']))


df_2015.plot('Time', 'Total_Leng', kind='scatter', ax=ax[0])
label_point(tor_df.Time, tor_df.Total_Leng, tor_df.PCNAME, ax[0])

mont_df.plot('Time', 'Total_Leng', kind='scatter', ax=ax[1])
label_point(mont_df.Time, mont_df.Total_Leng, mont_df.PCNAME, ax[1])

ott_df.plot('Time', 'Total_Leng', kind='scatter', ax=ax[2])
label_point(ott_df.Time, ott_df.Total_Leng, ott_df.PCNAME, ax[2])
#%%