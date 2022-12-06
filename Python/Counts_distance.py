# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 03:47:52 2022

@author: alexp
"""

import pandas as pd
import os
from matplotlib import pyplot as plt

from operator import attrgetter
import numpy as np
from simpledbf import Dbf5

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/')

years = [2015,2016,2017,2018,2019,2020]
ranges = [0,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900]

d = {}
plt.figure(figsize=(9, 5), dpi=80)
fig, ax  = plt.subplots(figsize=(9, 5), dpi=150)

for year in years:
    name = 'Arcmap/camping_number_reservations/'+str(year)+'_dist.dbf'
    dbf = Dbf5(name)
    df = dbf.to_dataframe()
    df['Total_Leng'] = df['Total_Leng']/1000
    df_2 = df.groupby(pd.cut(df.Total_Leng, ranges)).count()
    df_2.index.names = ['test'] 
    df_2 = df_2.reset_index(level=0)
    df_2['left'] = df_2['test'].map(attrgetter('left'))
    df_2['left'] = pd.to_numeric(df_2['left'])
    
    df_2['right'] = df_2['test'].map(attrgetter('right'))
    df_2['right'] = pd.to_numeric(df_2['right'])
    df_2['central_point'] = (df_2['right'] + df_2['left'])/2
    d[year] = df_2
    ax.scatter(df_2['central_point'], df_2['Total_Leng'])
plt.legend(years)
plt.xticks(np.arange(0, 901,50))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlabel('Distance (Km)')
plt.ylabel('Number of reservations')

plt.savefig('Model_results/camper_travel_distance_scatter.png')
plt.show()

frames = list(d.values())
names = list(d.keys())

new = pd.DataFrame(zip(frames[0].Total_Leng,frames[1].Total_Leng,frames[2].Total_Leng,
                       frames[3].Total_Leng,frames[4].Total_Leng),index=frames[0].central_point)

new = new.transpose()

plt.figure(figsize=(9, 5), dpi=150)

plt.boxplot(new, positions = list(new.columns), widths=(50) )

plt.xticks([0,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900],
           ['0','50','100','150','200','250','300','350','400','450','500','550','600','650','700','750','800','850','900'])
plt.xlabel('Distance (Km)')
plt.ylabel('Number of reservations')

plt.savefig('Model_results/camper_travel_distance_boxplot_50km.png')
    