# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 11:13:42 2021

@author: alexp
"""
#%% Import packages 
import os
os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding/Python')

import os
import pandas as pd
import networkx as nx
from B_Simulation import Simulation
from A_Defined_States import States

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding')


edgelist_df= pd.read_csv('Camping_data/Edgelist.csv')
#%%
def initial_state(G):
    state = {}
    for node in G.nodes:
        if node == 'Edmundston':
            state[node] = 'I'
        elif node == 'Halifax':
            state[node] = 'I'
        elif node == 'Fredericton':
            state[node] = 'I'
        elif node == 'Moncton':
            state[node] = 'I'
        elif node == 'Oromocto':
            state[node] = 'I'
        else:
            state[node] = 'S'
    nx.set_node_attributes(G,state,'State')
    return state

def state_transition(G, current_state):
    import random
    #The first generalization is that mostThe Þrst generalization is that a majority of campground visits involve relatively short travel distances (<100 km, which is usually a <2-h drive fromhome) Koch et al. 2012 
    next_state={}
    degree={}
    origin_degree={}
    num_inf_camper={}
    #Per capita value is a source of number of reservations taken from a national system 
    per_capita_value=0.0047
    #Firewood source(outside park:0.25, from home:0.17,cut of collected from another area:0.14)Jacobi et al. 2011, and incident that wood has invasive buprestids (percent wood fraxinus:0.1455, percent with live borers:0.34)  Haack et al. 2010
    prob_infested_wood=(0.25+0.17+0.14)*0.23
    #Iterate through each node splitting the two by infected and uninfected nodes 
    for node in G.nodes:
        #if the node is infected, print the number of campers leaving the campground with infested wood/year(per capita value) is calculated, and calculate the total campground pull value from all campgrounds(in degree)
        
        if current_state[node] == 'I':
            
            #number of infected campers from Origins
            nx.set_node_attributes(G,{node:G.nodes[node]['Population']*0.0016729+6.24567023*prob_infested_wood},'Infected_camper')
            Inf_camper = nx.get_node_attributes(G,'Infected_camper')
            
            #Get total campground pull from all neighbour nodes
            degree[node]= G.degree(node, weight='Campground_pull')
            nx.set_node_attributes(G, degree,'in_degree')
            num_inf_camper[node]=int(G.nodes[node]['Infected_camper'])
            
            #Get the pull of each campground using number of campsites in campground and distance between campground and origin
            node_degree={}
            pull_list=[]
            number=0
            for neighbor in G.neighbors(node):
                if G.nodes[neighbor]['Sites'] >1: 
                    X_i=G.nodes[neighbor]['Sites']
                    D_ij=G.edges[neighbor,node]['Distance_Km']
                    
                    #Calculate pull value and normalize data using the total in-degree of nodes and load them into a dictionary of dictionary
                    #dict : origin_degree = {Origin(node):{Campground(neighbor): normalized_pull}}
                    pull = (X_i/D_ij)
                    pull_list.append(pull)
                    node_degree[neighbor]=pull
                    print(node_degree)
                    origin_degree[node]=node_degree
                    number = number+ G.degree([node],weight='Sites')
                       # create a list of randomly distributed infected campers(number of campers using k values) going from origin to a susceptible campground       
    infected=[]
    Origin_keys=[]
    Origin_values=[]
    for k, v in origin_degree.items():
        infected.append(random.choices(list(v.keys()), weights=list(v.values()), k=num_inf_camper[k]))
        #flatten list
        infected_flat=[val for subgroup in infected for val in subgroup]
    infected_flat.sort()  
    d = {x:infected_flat.count(x) for x in infected_flat}
    
    for node in G.nodes:
        if current_state[node] == 'S':
            for node,count in d.items():
                if count >1: 
                    next_state[node] = 'I'          
    
    return next_state
#%%
G = nx.from_pandas_edgelist(edgelist_df,source='Orig_name',target='Dest_name',edge_attr=['Distance_Km'])
#for index, dest in edgelist_df[['type']].iterrows():
    #if dest['type'] == 'city_to_camp':
        #nx.set_node_attributes(G, dict(zip(edgelist_df['Dest_name'],edgelist_df['Sites'])),'Sites')
    #elif dest['type'] == 'city_to_city':
        #nx.set_node_attributes(G, dict(zip(edgelist_df['Dest_name'],edgelist_df['Dest_pop'])),'Dest_Population')
nx.set_node_attributes(G, dict(zip(edgelist_df['Orig_name'],edgelist_df['Orig_pop'])),'Population')
nx.set_node_attributes(G, dict(zip(edgelist_df['Dest_name'],edgelist_df['Sites'])),'Sites')
#%%
current_state = (initial_state(G))
print(state_transition(G, current_state))
#%%

dict_pos=dict(zip(edgelist_df.Dest_name,list(zip(edgelist_df.Dest_long,edgelist_df.Dest_lat))))
dict_pos.update(dict(zip(edgelist_df.Orig_name,list(zip(edgelist_df.Orig_long,edgelist_df.Orig_lat)))))
nx.draw(G,pos=dict_pos,node_size=8,node_color='green', width=0.05)

#%%

Sim = Simulation(G, initial_state, state_transition, name='test')
#%%
Sim.run(20)
Sim.plot()

