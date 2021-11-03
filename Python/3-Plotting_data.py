# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 16:02:56 2021

input a list of locations with their Lat and Long and output the driving distance between the two points

@author: alexp
"""

import networkx as nx
import pandas as pd
import os
import matplotlib.pyplot as plt

os.chdir('\..')
os.chdir("Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding/Camping_data/")

Edgelist_df = pd.read_csv('Edgelist.csv',index_col=False)
#camp_df = pd.read_csv('Parks_and_camping_Master_2021-10-13.csv')
#city_df = pd.read_csv('Cities_Master_2021-10-12.csv')


##Clean Camp_df 
#Remove any values that don't include real numbers to simplify(this can be removed when the campground data sheet is cleaned up)
#import numpy as np
#camp_df=camp_df.replace('?',np.NaN).replace(r'^\s*$',np.NaN,regex=True).replace('>50',np.NaN).replace('>45',np.NaN).replace('>60',np.NaN)
##Fill NAN sites to have zero 
#camp_df['Sites'] = camp_df['Sites'].fillna(0)
#include only pertanent columns
#camp_df= camp_df[['Type of Campground', 'Name', 'Province', 'Sites', 'Latitude', 'Longitude', 'Aquiring firewood']]
#Change data type of Sites, Latitude, and Longitude
#camp_df= camp_df.astype({'Sites':'int32','Latitude':'float64', 'Longitude':'float64' })
#camp_df= camp_df.replace(0,np.NaN).dropna(subset=['Latitude'])



#Create a dict of latitude and longitude to draw the network
dict_pos=dict(zip(Edgelist_df.Name,list(zip(Edgelist_df.camp_Long,Edgelist_df.camp_Lat))))
dict_pos.update(dict(zip(Edgelist_df.Geographic_Name,list(zip(Edgelist_df.city_Long,Edgelist_df.city_Lat)))))
#print(dict_pos)

#Create a merged dataframe of both campground data and city data into one dataframe
#merge_df = camp_df.append(city_df, sort=False,ignore_index=True)

#Create a networkx graph(the dataframe needs to be an edgelist not a nodelist)
G = nx.from_pandas_edgelist(Edgelist_df, source='Geographic_Name',target='Name')
#Draw the network
#nx.draw_networkx_nodes(G, pos = dict_pos, node_size=8, node_color='green')
nx.draw(G, pos=dict_pos,node_size=8,node_color='green', width=0.05)

plt.savefig('graph.png',dpi=300, format='PNG')
# get the nearest network node to each point
#orig_node = ox.get_nearest_node(G, (37.828903, -122.245846))
#dest_node = ox.get_nearest_node(G, (37.812303, -122.215006))

# how long is our route in meters?
#nx.shortest_path_length(G, orig_node, dest_node, weight='length')
