# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 14:19:18 2022

@author: alexp
This is  a testing file for the Creation of network graph file. 

Here you can test new ways to implement code in the initial and state transition functions *make sure to update the files by adding the newest function parameters from the creation of a network model file



"""

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
#import random is used for the random generation of numbers
    #import random is used for the random generation of numbers
import random

#Dictionary of destination campgrounds and cities that become infested in the next time period
next_state={}
#Degree is the in-degree, the number of campground nodes connected to it
degree={}

origin_degree_camp={}
origin_degree_city={}
num_inf_camper={}
#Per capita value is a source of number of reservations taken from a national system 
#per_capita_value=0.0047

#Firewood source(0.66 of campers bring their own firewood, of that the source is that outside park:0.25, from home:0.17,cut of collected from another area:0.14)Jacobi et al. 2011, and and incident that wood has live insects in it (percent wood fraxinus:0.1455, percent with live borers:0.34)  Haack et al. 2010
prob_infested_wood=(0.66)*(0.25+0.17+0.14)*(0.1455*0.34)
#Iterate through each node splitting the two by infected and uninfected nodes 
for node in G.nodes:
    #if the node is infected, print the number of campers leaving the campground with infested wood/year(per capita value) is calculated, and calculate the total campground pull value from all campgrounds(in degree)
    if G.nodes[node]['current_state'] == 'I':
        # Only cities that are infected can move EAB to different places
        if G.nodes[node]['Type'] == 'city_to_city':
            #Measures the total number of campers going to campgrounds in all three provinces = (reservations to within province campgrounds)+ (reservations to outside province campgrounds)
            #number of infected campers from Origin location using the follwing equation (Number of people making reservations from inf. city)*proportion of reservations made within province*(prop. of campgrounds in province*total campgrounds)+
            #(Number of people making reservations from inf. city)*proportion of reservations made outside of province*(prop. of campgrounds outside of province province*total campgrounds)
            nx.set_node_attributes(G,{node:(((G.nodes[node]['Population']*0.0016729+6.24567023)*0.85*(0.3333*210)+(G.nodes[node]['Population']*0.0016729+6.24567023)*0.15*(0.6666*210))*prob_infested_wood)},'Infected_camper')

            #Get total campground attractance from all neighbour nodes
            degree[node]= G.degree(node, weight='Campground_pull')
            nx.set_node_attributes(G, degree,'in_degree')
            num_inf_camper[node]=round(G.nodes[node]['Infected_camper'])
            
            #Get the pull of each campground using number of campsites in campground and distance between campground and origin
            node_degree_camp={}
            node_degree_city={}
            pull_list=[]
            
            #
            for neighbor in G.neighbors(node):
                #If else statement to separate campgrounds and cities to send 
                    #campgrounds:
                if G.nodes[neighbor]['Sites'] >1: 
                    #defined variables X_i are the number of campsites, D_ij is the Distance between campground and origin
                    X_i=G.nodes[neighbor]['Sites']
                    D_ij=G.edges[neighbor,node]['Distance_Km']
                    
                    #Calculate attractance value(Pull) load them into a dictionary of dictionary for each infected node
                    #dict : origin_degree = {Origin(node):{Campground(neighbor): attractance}
                    #A majority of campground visits involve relatively short travel distances (<100 km, which is usually a <2-h drive from home) Koch et al. 2012 also see Eagles et al. 2015
                    pull = (X_i*(1*(1-0.5))**(D_ij/100))
                    pull_list.append(pull)
                    node_degree_camp[neighbor]=pull
                    origin_degree_camp[node]=node_degree_camp
                    #cities:
                else : 
                    P_j=G.nodes[neighbor]['Population']
                    #Mean number of trips made from county A to county B
                    M_ij=G.edges[neighbor,node]['mean_trips_year']
                    D_ij=G.edges[neighbor,node]['Distance_Km']
                
                    #Calculate attractance value(Pull) load them into a dictionary of dictionary for each infected node
                    #dict : origin_degree_city = {Origin city(node):{destnation city(neighbor): pull value(population multiplied by the amount of travel between locations )}}
                    pull = (P_j*M_ij)
                    node_degree_city[neighbor]=pull
                    origin_degree_city[node]=node_degree_city          
   
###  
#Distribute infected campers to campgrounds based on gravity values
###                  
#create a list containing the names of locations that become infected    
infected=[]

# distribute campers randomly (number of campers using k values) going from origin to a susceptible campground
for k, v in origin_degree_camp.items():
    #randomly select campgrounds(v.keys) based on the pull value that each one has(weight) using the number of campers leaving the city with infested firewood
    infected.append(random.choices(list(v.keys()), weights=list(v.values()), k=num_inf_camper[k]))
    #turn a list of lists into a simple list, by removing extra brackets(flatten list)
infected_flat=[val for subgroup in infected for val in subgroup]
infected_flat.sort()  
d = {x:infected_flat.count(x) for x in infected_flat}

###
#Calculate total pull and select city at a weighted random value based on the total amount of in traffic coming from 
###
#this loop gets the total pull from all the cities in the in the list from Origin degree cities to a single summed value
total = {}
for k, v in origin_degree_city.items():
    for k2, v2 in v.items():
        total[k2] = total.get(k2, 0) + v2

#remove the cities that are already infected
for node in G.nodes:
    if G.nodes[node]['Type'] == 'city_to_city':
        if G.nodes[node]['current_state'] == 'I':
            del total[node]
if total:
    infected.append(random.choices(list(total.keys()), weights=list(total.values()), k=1))
#iterate through the dictionary of uninfested cities(k) and the 
#for k, v in origin_degree_city.items():
    #infected.append(random.choices(list(v.keys()), weights=list(v.values()), k=1))
    #turn a list of lists into a simple list, by removing extra brackets(flatten list)
infected_flat=[val for subgroup in infected for val in subgroup]
infected_flat.sort()  
d = {x:infected_flat.count(x) for x in infected_flat}

###
#Changing the state of campground + based on yearly arrival rate of firewood
###

#num_count = 2
#for node in G.nodes:
    #if G.nodes[node]['Type'] == 'city_to_camp':
        #if current_state[node] == 'S':
            #if node in d.keys():
                #if d[node] >= num_count:
                    #next_state[node] = 'I'
    #elif G.nodes[node]['Type'] == 'city_to_city':
        #if current_state[node] == 'S':
            #if node in d.keys():
                #if d[node] >=1: 
                    #next_state[node] = 'I'

###
#Disperse firewood into camping months based on the mean number of reservations made to NB provicial parks
###

#Dictionary of the mean number of reservations made based on the month 
reservations_month = {'May':109.4,'June':619.67, 'July':1521.83, 'August':1583.33, 'September':559.3,'October':62}                   

firewood_dispersal = {}
#Iterate through each susceptible node that received firewood and distribute the firewood based on mean monthly reservations made to campgrounds
for node in G.nodes:
    if G.nodes[node]['Type'] == 'city_to_camp':
        #if current_state[node] == 'S':
        if node in d.keys():
            #randomly distribute pieces of firewood based on the weights of reservation months. campgrounds are separated by month, weights= number of res, made per year, k= number of pieces of firewood that show up in a year
            firewood_dispersal[node] = (random.choices(list(reservations_month.keys()),weights=list(reservations_month.values()), k=d[node]))

from collections import Counter
#Count the total number of pieces of firewood distributed to each month
for k,v in firewood_dispersal.items():
    firewood_dispersal[k] = dict(Counter(v))

#Supply rate of EAB from unburnt firewood. Calculated using the equation from the file Relationship_firewood_burn_vs_emergence_probability.py
sup_rate_EAB={'May':0.0635, 'June':0.269, 'July':0.391, 'August':0.0694, 'September':0, 'October': 0}



int_load=2
 
 
 ###
 #Distribute firewood arriving into campground based on month of arrival change the status of the campground based on the number of introduced load(propagule pressure)
 ###
firewood_dispersal_2 = {}
def test():
    for node in G.nodes:
        if G.nodes[node]['Type'] == 'city_to_camp':
            if G.nodes[node]['current_state'] == 'S':
                if node in firewood_dispersal.keys():
                    #Measures if the there are any months within that campground that have a high enough arrival rate that equal or surpasses the int_load
                    #if dict((k, v) for k, v in firewood_dispersal[node].items() if v >= int_load):
                    for month,firewood_load in firewood_dispersal[node].items():
                        
                        emerged_firewood = 0
                        for piece_firewood in range(firewood_load):
                            rand=random.random()
                            if rand < sup_rate_EAB[month]:
                                emerged_firewood = emerged_firewood+1
                        firewood_dispersal[node][month] = emerged_firewood
                        #for firewood in rangefirewood_dispersal
                            #print(firewood_dispersal[node].items())
                    if dict((k, v) for k, v in firewood_dispersal[node].items() if v >= int_load):
                    #print(test.values())
                        G.nodes[node]['current_state']= 'I'
                            #print(rand, sup_rate_EAB[i])
                            
                        #print(node, sup_rate_EAB[list(test.keys())])
    for node in G.nodes:
        if G.nodes[node]['Type'] == 'city_to_camp':
            if G.nodes[node]['current_state'] == 'I':
                print(node,firewood_dispersal[node].items())
    #return print(nx.get_node_attributes(G,'current_state'))

test()
    #This changes the state of the one city that changes that year
    #elif G.nodes[node]['Type'] == 'city_to_city':
        #if current_state[node] == 'S':
            #if node in d.keys():
                
                #if d[node] >=1: 
                   
                    #next_state[node] = 'I'
#print(nx.get_node_attributes(G,'current_state'))
#%%
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