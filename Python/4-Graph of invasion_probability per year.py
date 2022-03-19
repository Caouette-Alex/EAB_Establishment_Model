# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 14:02:52 2022

@author: alexp
"""
import os
import pandas as pd

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Model_results')

df = pd.read_csv('Sim_2022-03-14_1000_Mean_invasion_probability_per_year',index_col=0)


from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches


# prep values for map extents and more
llcrnrlat = 43.42
llcrnrlon = -68.6
urcrnrlat = 49
urcrnrlon = -59.68
mid_lon = (urcrnrlon+llcrnrlon)/2.0
hr_lon = (urcrnrlon-llcrnrlon)/2.0
mid_lat = (urcrnrlat+llcrnrlat)/2.0
hr_lat = (urcrnrlat-llcrnrlat)/2.0

# function to create inset axes and plot bar chart on it
# this is good for 3 items bar chart
def build_bar(mapx, mapy, ax, width, xvals=['a','b','c'], yvals=[1,4,2], fcolors=['r','y','b']):
    ax_h = inset_axes(ax, width=width, \
                    height=width, \
                    loc=3, \
                    bbox_to_anchor=(mapx, mapy), \
                    bbox_transform=ax.transData, \
                    borderpad=0, \
                    axes_kwargs={'alpha': 0.35, 'visible': True})
    for x,y,c in zip(xvals, yvals, fcolors):
        ax_h.bar(x, y, label=str(x), fc=c)
    #ax.xticks(range(len(xvals)), xvals, fontsize=10, rotation=30)
    ax_h.axis('off')
    return ax_h

fig, ax = plt.subplots(figsize=(10, 9))  # bigger is better

bm = Basemap(llcrnrlat= llcrnrlat,\
             llcrnrlon= llcrnrlon,\
             urcrnrlat= urcrnrlat,\
             urcrnrlon= urcrnrlon,\
             ax = ax,\
             resolution='i', projection='tmerc', lon_0=-62, lat_0=45)
    

bm.drawstates(linewidth=0.2)
bm.drawmapboundary(fill_color='paleturquoise',zorder=-2)
bm.fillcontinents(color='lightyellow', zorder=0)
bm.drawcoastlines(color='gray', linewidth=0.3, zorder=2)

plt.title('invasion probability by year', fontsize=20)

# ======================
# make-up some locations
# ----------------------
n = 238   # you may use 121 here
lon1s = df['lat'].tolist()
lat1s = df['long'].tolist()
# make-up list of 3-values data for the locations above
# -----------------------------------------------------
coord = df.to_dict('split')


bar_data = [item[0:3] for item in coord['data']]

# create a barchart at each location in (lon1s,lat1s)
# ---------------------------------------------------
bar_width = 0.05  # inch
colors = ['r','y','b']
for ix, lon1, lat1 in zip(list(range(n)), lon1s, lat1s):
    x1, y1 = bm(lon1, lat1)   # get data coordinates for plotting
    bax = build_bar(x1, y1, ax, 0.2, xvals=['a','b','c'], \
              yvals=bar_data[ix], \
              fcolors=colors)

# create legend (of the 3 classes)
patch0 = mpatches.Patch(color=colors[0], label='5 years')
patch1 = mpatches.Patch(color=colors[1], label='10 years')
patch2 = mpatches.Patch(color=colors[2], label='15 years')
ax.legend(handles=[patch0,patch1,patch2], loc=1)

plt.show()