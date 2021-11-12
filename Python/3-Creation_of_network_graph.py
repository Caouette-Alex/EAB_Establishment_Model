# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 11:13:42 2021

@author: alexp
"""
import os
os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding/Python')

import os
import pandas as pd
import networkx as nx
import B_Simulation as sim
from A_Defined_States import States as ste

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding')


edgelist_df= pd.read_csv('Camping_data/Edgelist.csv')
#%%
G = nx.from_pandas_edgelist(edgelist_df,source='Orig_name',target='Dest_name',edge_attr=['Distance_Km'])
for index, dest in edgelist_df[['type']].iterrows():
    if dest['type'] == 'city_to_camp':
        nx.set_node_attributes(G, dict(zip(edgelist_df['Dest_name'],edgelist_df['Sites'])),'Sites')
    elif dest['type'] == 'city_city':
        nx.set_node_attributes(G, dict(zip(edgelist_df['Dest_name'],edgelist_df['Dest_pop'])),'Dest_Population')
nx.set_node_attributes(G,dict(zip(edgelist_df['Orig_name'],edgelist_df['Orig_pop'])),'Population')

#%%

dict_pos=dict(zip(edgelist_df.Dest_name,list(zip(edgelist_df.Dest_long,edgelist_df.Dest_lat))))
dict_pos.update(dict(zip(edgelist_df.Orig_name,list(zip(edgelist_df.Orig_long,edgelist_df.Orig_lat)))))
nx.draw(G,pos=dict_pos,node_size=8,node_color='green', width=0.05)

#%%
sim.Simulation(G, ste.initial_state(G), ste.state_transition(G, ste.initial_state(G)),name='SIS-model')
