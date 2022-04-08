# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 21:04:28 2022

@author: alexp
"""

import os
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Model_results')

df = pd.read_csv('Sim_2022-03-28_50_Mean_invasion_probability_per_year',index_col=0).drop(['1e-14'])

# prep values for map extents and more
llcrnrlat = 43.42
llcrnrlon = -68.6
urcrnrlat = 49
urcrnrlon = -59.68
mid_lon = (urcrnrlon+llcrnrlon)/2.0
hr_lon = (urcrnrlon-llcrnrlon)/2.0
mid_lat = (urcrnrlat+llcrnrlat)/2.0
l=['5','10','20']

plt.rcParams['figure.dpi'] = 1000

fig = plt.figure() 

n=0

for i in l:
    n = n + 1
    
    ax = fig.add_subplot(1,3,n)
    ax.set_title( i + 'years', fontsize=10)
    bm = Basemap(llcrnrlat= llcrnrlat,\
                     llcrnrlon= llcrnrlon,\
                     urcrnrlat= urcrnrlat,\
                     urcrnrlon= urcrnrlon,\
                     ax = ax,\
                     resolution='i', projection='tmerc', lon_0=-62, lat_0=45)
    
        
    bm.drawstates(linewidth = 0.2)
    bm.drawcountries(linewidth = 0.5 )
    bm.drawmapboundary(fill_color='paleturquoise',zorder=-2)
    bm.fillcontinents(color='lightyellow', zorder=0)
    bm.drawcoastlines(color='gray', linewidth=0.3, zorder=2)
        
    x, y = bm(df['lat'].tolist(), df['long'].tolist())
    sc = bm.scatter(x, y, marker='o', c = df[i], zorder=5, cmap= 'plasma',s=1)
    print(((df[i]))*3)
fig.suptitle('Probability of emerald ash borer transport by years', y = 0.75)

#fig2 = plt.figure() 
#plt.axis('off')

#l1 = plt.scatter([],[], s=0.25, color='red')
#l2 = plt.scatter([],[], s=0.5, color='red')
#l3 = plt.scatter([],[], s=0.75, color='red')
#l4 = plt.scatter([],[], color='red')

labels = ["0.25", "0.5", "0.75", "1"]



leg = plt.legend(*sc.legend_elements(num=5), bbox_to_anchor=(-0.7,-0.25),loc='center', ncol=6, frameon= False, fontsize=8, borderpad = 1) 
plt.show()
#%%

df2 = pd.read_csv('Sim_2022-03-18_1000_Mean_invasion_year',index_col=0).drop(['1e-14'])
fig, ax = plt.subplots(figsize=(10, 9))  # bigger is better

llcrnrlat = 43.42
llcrnrlon = -68.6
urcrnrlat = 49
urcrnrlon = -59.68
mid_lon = (urcrnrlon+llcrnrlon)/2.0
hr_lon = (urcrnrlon-llcrnrlon)/2.0
mid_lat = (urcrnrlat+llcrnrlat)/2.0

bm = Basemap(llcrnrlat= llcrnrlat,\
             llcrnrlon= llcrnrlon,\
             urcrnrlat= urcrnrlat,\
             urcrnrlon= urcrnrlon,\
             ax = ax,\
             resolution='i', projection='tmerc', lon_0=-62, lat_0=45)



bm.drawstates(linewidth=0.2)
bm.drawcountries(linewidth = 0.5)
bm.drawmapboundary(fill_color='paleturquoise',zorder=-2)
bm.fillcontinents(color='lightyellow', zorder=0)
bm.drawcoastlines(color='gray', linewidth=0.3, zorder=2)
    
x, y = bm(df['lat'].tolist(), df['long'].tolist())


sc = plt.scatter(x, y, marker=, zorder=5, s=50, cmap= 'plasma_r', c = df2['50'])
plt.title('Mean transportation year',fontsize=20)
plt.legend(*sc.legend_elements("sizes", num=6))
l1 = plt.scatter([],[], s=50, color='red')
l2 = plt.scatter([],[], s=100, color='red')
l3 = plt.scatter([],[], s=150, color='red')
l4 = plt.scatter([],[], s=200, color='red')
l5 = plt.scatter([],[], s=250, color='red')

labels = ["10", "20", "30", "40","50"]



leg = plt.legend(*sc.legend_elements(num=[1,5,10,15,20,25,30,40,50]),loc = 'upper right',  frameon= False, ncol=1, fontsize=12, borderpad = 1)

#handlelength=2,loc='upper right', borderpad = 1,
#handletextpad=1, scatterpoints = 1)


#x, y = bm(df['long'].tolist(), df['lat'].tolist() ) # transform coordinates
#plt.scatter(x, y, marker='o', color='Red',zorder=5)
#plt.plot(x, y, color='r', markersize=5)
#df.plot.scatter(x = df['long'], y = df['lat'])# s=df['Total']*50, c=df['Total']

plt.show()