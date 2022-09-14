# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 14:19:18 2022

@author: alexp
This is  a testing file for the Creation of network graph file. 

Here you can test new ways to implement code in the initial and state transition functions *make sure to update the files by adding the newest function parameters from the creation of a network model file



"""

|
#%% Import packages and add edgelist dataframe
import os
os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding/Python')
import pandas as pd
import networkx as nx
import math
#imported from files from the book by filippo Menczer, Santo Fortunato, and Clayton Davies A first Course in Network Science
from B_Simulation import Simulation

#Change direcotory to open to where the majority of the data is
os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding')

#Open edgelist of camping and cities that are interconnected, inlcudes population, sites, lat and long, From file 2-Merge_distance_to_edgelist.py
edgelist_df= pd.read_csv('Camping_data/Edgelist_Dist_TSRC.csv')
#%% Create Graph from pandas edgelist and insert node and edge attributes
G = nx.from_pandas_edgelist(edgelist_df,source='Orig_name',target='Dest_name',edge_attr=['Distance_Km','mean_trips_year'])

#add coordinates for each node by first creating key value group of {Dest name: Long, lat}
dict_pos=dict(zip(edgelist_df.Dest_name,list(zip(edgelist_df.Dest_long,edgelist_df.Dest_lat))))
dict_pos.update(dict(zip(edgelist_df.Orig_name,list(zip(edgelist_df.Orig_long,edgelist_df.Orig_lat)))))
nx.set_node_attributes(G, dict_pos, 'pos')
#Adding node attributes to origin locations and destination locations including the site population, number of campsites, and type of edge relationship(city-city vs. city-camp)
nx.set_node_attributes(G, dict(zip(edgelist_df['Orig_name'],edgelist_df['Orig_pop'])),'Population')
nx.set_node_attributes(G, dict(zip(edgelist_df['Dest_name'],edgelist_df['Sites'])),'Sites')
nx.set_node_attributes(G, dict(zip(edgelist_df['Dest_name'],edgelist_df['type'])),'Type')# might need to change this to an edge attribute

# TODO 



#%%l_test = ['Edmundston','Fredericton', 'Oromocto', 'Halifax', 'Moncton']

l_test = ['Edmundston','Fredericton', 'Halifax', 'Moncton','Oromocto']

for node in G.nodes:
    if node in l_test:
        nx.set_node_attributes(G,{node:{'current_state': 'I'}})
    else:
        nx.set_node_attributes(G,{node:{'current_state':'S'}})



d_1 = {}
import random
#The first generalization is that a majority of campground visits involve relatively short travel distances (<100 km, which is usually a <2-h drive from home) Koch et al. 2012 
next_state={}
degree={}
origin_degree_camp={}
origin_degree_city={}
num_inf_camper={}
#Per capita value is a source of number of reservations taken from a national system 
per_capita_value=0.0047
#Firewood source(0.66 of campers bring their own firewood, of that the source is that outside park:0.25, from home:0.17,cut of collected from another area:0.14)Jacobi et al. 2011, and and incident that wood has live insects in it (percent wood fraxinus:0.1455, percent with live borers:0.34)  Haack et al. 2010
prob_infested_wood=(0.66)*(0.25+0.17+0.14)*(0.1455*0.34)
#Iterate through each node splitting the two by infected and uninfected nodes 
for node in G.nodes:
    #if the node is infected, print the number of campers leaving the campground with infested wood/year(per capita value) is calculated, and calculate the total campground pull value from all campgrounds(in degree)
    if G.nodes[node]['current_state'] == 'I':
        # Only cities that are infected can move EAB to different places
        if G.nodes[node]['Type'] == 'city_to_city':
            #number of infected campers from Origin location
            nx.set_node_attributes(G,{node:((G.nodes[node]['Population']*0.0016729+6.24567023)*210*prob_infested_wood)},'Infected_camper')
            Inf_camper = nx.get_node_attributes(G,'Infected_camper')
            
            #Get total campground attractance from all neighbour nodes
            degree[node]= G.degree(node, weight='Campground_pull')
            nx.set_node_attributes(G, degree,'in_degree')
            num_inf_camper[node]=round(G.nodes[node]['Infected_camper'])
            
            #Get the pull of each campground using number of campsites in campground and distance between campground and origin
            node_degree_camp={}
            node_degree_city={}
            pull_list=[]
            for neighbor in G.neighbors(node):
                #If else statement to separate campgrounds and cities to send 
                if G.nodes[neighbor]['Sites'] >1:
                    #defined variables X_i are the number of campsites, D_ij is the Distance between campground and origin
                    X_i=G.nodes[neighbor]['Sites']
                    D_ij=G.edges[neighbor,node]['Distance_Km']
                    #g = X_i/(1-)
                    #Calculate attractance value(Pull) load them into a dictionary of dictionary for each infected node
                    #dict : origin_degree = {Origin(node):{Campground(neighbor): attractance}
                    pull = (X_i*(1*(1-0.5))**(D_ij/100))
                    pull_list.append(pull)
                    node_degree_camp[neighbor]=pull
                    origin_degree_camp[node]=node_degree_camp
                else : 
                    P_i=G.nodes[neighbor]['Population']
                    #Mean number of trips made from county A to county B
                    M_ij=G.edges[neighbor,node]['mean_trips_year']
                    D_ij=G.edges[neighbor,node]['Distance_Km']
                
                    #Calculate attractance value(Pull) load them into a dictionary of dictionary for each infected node
                    #dict : origin_degree = {Origin(node):{Campground(neighbor): normalized_pull}}
                    pull = (P_i*M_ij)
                    node_degree_city[neighbor]=pull
                    origin_degree_city[node]=node_degree_city          
   
###
#Distribute infected firewood based on movement of people across cities 
###
#this loop gets the total pull from all the cities in the 
infected=[]
total = {}
import numpy as np
import timeit
from numpy.random import rand
start = timeit.default_timer()
for k, v in origin_degree_camp.items():
    #print(num_inf_camper)
    #randomly select campgrounds(v.keys) based on the pull value that each one has(weight) using the number of campers leaving the city with infested firewood
    #probs = np.random.rand(k); probs/=probs.sum()
    #print([list(v.values())])
    #for i in range(num_inf_camper[k]):
        #weights = np.array([list(v.values())])
        #cs = np.cumsum(weights)
        #idx = sum(cs < rand())
        #print(v.keys())
    #print(num_inf_camper[k])
    #infected.append(np.random.choice(list(v.keys()), p=list(v.values()), size=num_inf_camper[k]))
    infected.append(random.choices(list(v.keys()), weights=list(v.values()), k=num_inf_camper[k]))
    #turn a list of lists into a simple list, by removing extra brackets(flatten list)
print(timeit.default_timer() - start)
infected_flat=[val for subgroup in infected for val in subgroup]
infected_flat.sort()  
d = {x:infected_flat.count(x) for x in infected_flat}


for k, v in origin_degree_city.items():
    for k2, v2 in v.items():
        total[k2] = total.get(k2, 0) + v2
        
for node in G.nodes:
    if G.nodes[node]['current_state'] == 'I':
        del total[node]

infected.append(random.choices(list(total.keys()), weights=list(total.values()), k=1))

#print(infected)
#iterate through the dictionary of uninfested cities(k) and the 
#for k, v in origin_degree_city.items():
    #infected.append(random.choices(list(v.keys()), weights=list(v.values()), k=1))
    #turn a list of lists into a simple list, by removing extra brackets(flatten list)
infected_flat=[val for subgroup in infected for val in subgroup]
infected_flat.sort()  
d = {x:infected_flat.count(x) for x in infected_flat}



###
#Changing the state of campground +
###
num_count = 2
for node in G.nodes:
    if G.nodes[node]['Type'] == 'city_to_camp':
        if G.nodes[node]['current_state'] == 'S':
            if node in d.keys():
                if d[node] >= num_count:
                    #print(node, d[node]) 
                    next_state[node] = 'I'
    elif G.nodes[node]['Type'] == 'city_to_city':
        if G.nodes[node]['current_state'] == 'S':
            if node in d.keys():
                #print(d[node])
                if d[node] >=1: 
                    #print(node)
                    next_state[node] = 'I'
###
# Creating a poisson distribution of the probability that a location has n number of pieces of firewood appearing in the same month
###

#this creates a dictionary with values that represent the likelihood that two pieces of firewood will show up in the same month
poisson_dict = {}
for node in G.nodes:
    if G.nodes[node]['Type'] == 'city_to_camp':
        if G.nodes[node]['current_state'] == 'S':
            if node in d.keys():
                mean_succ= d[node]/5
                e=2.71828
                act_succ=2
                poisson_dict[node] = ((e**(-mean_succ))*(mean_succ**act_succ))/math.factorial(act_succ)

from collections import Counter,OrderedDict


firewood_dispersal = {}
for node in G.nodes:
    if G.nodes[node]['Type'] == 'city_to_camp':
        if G.nodes[node]['current_state'] == 'S':
            if node in d.keys():
                firewood_dispersal[node] = (random.choices(['1','2','3','4','5','6'],weights=[109.4,619.67,1521.83,1583.33,559,62], k=d[node]))

for k,v in firewood_dispersal.items():
    firewood_dispersal[k] = dict(Counter(v))

num_count = 25
for node in G.nodes:
    if G.nodes[node]['Type'] == 'city_to_camp':
        if G.nodes[node]['current_state'] == 'S':
            if node in firewood_dispersal.keys():
                if dict((k, v) for k, v in firewood_dispersal[node].items() if v >= num_count):
                    print(node, firewood_dispersal[node].values())
                    #next_state[node] = 'I'
    elif G.nodes[node]['Type'] == 'city_to_city':
        if G.nodes[node]['current_state'] == 'S':
            if node in d.keys():
                #print(d[node])
                if d[node] >=1: 
                    #print(node)
                    next_state[node] = 'I'

#od = OrderedDict(sorted(firewood_dispersal.items()))

#res = sorted(firewood_dispersal.items(), key = lambda x: x[1]['1'])

print(len(d.keys()))
        

global prpgl_pres