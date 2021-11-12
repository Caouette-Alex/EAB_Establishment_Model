# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 10:48:38 2021

@author: alexp
"""

''' 
Simulation class creation for the simulation of EAB dynamic network in Maritime Canada

'''
import networkx as nx
import pandas as pd
import random
#%%
import os

class States:
    #%%
    #Initial infected(I) vs susceptible(S) state 
    def initial_state(G):
            state = {}
            for node in G.nodes:
                if node == 'Edmunston':
                    state[node] = 'I'
                elif node == 'Bedford':
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
    #%%
    #test initial_state
    #initial_state(G)
    #%%
    def state_transition(G, current_state):
        #The first generalization is that mostThe Þrst generalization is that a majority of campground visits involve relatively short travel distances (<100 km, which is usually a <2-h drive fromhome) Koch et al. 2012 
        next_state={}
        degree={}
        iorigin_degree={}
        
        #Per capita value is a source of number of reservations taken from a national system 
        per_capita_value=0.0047
        #Firewood source(outside park:0.25, from home:0.17,cut of collected from another area:0.14)Jacobi et al. 2011, and Percent of live borers found in wood(0.23) Haack et al. 2010
        prob_infested_wood=(0.25+0.17+0.14)*0.23
        #Iterate through each node splitting the two by infected and uninfected nodes 
        for node in G.nodes:
            #if the node is infected, print the number of campers leaving the campground with infested wood/year(per capita value) is calculated, and calculate the total campground pull value from all campgrounds(in degree)
            
            if current_state[node] == 'I':
                #number of infected campers from campgrounds
                nx.set_node_attributes(G,{node:G.nodes[node]['Population']*(per_capita_value*prob_infested_wood)},'Infected_camper')
                Inf_camper = nx.get_node_attributes(G,'Infected_camper')
                
                #Get total campground pull from all neighbour nodes
                degree[node]= G.degree(node, weight='Campground_pull')
                nx.set_node_attributes(G, degree,'in_degree')
                
            #iCampground_pull={}
                inode_degree={}
                for neighbor in G.neighbors(node):
                    
                    
                    #ipull_dict={}
                    ipull = (G.nodes[neighbor]['Sites']/G.edges[neighbor,node]['Distance_Km'])/degree[node]
                    #ipull_dict['Campground_pull']=ipull
                    #iCampground_pull[node,neighbor]=ipull_dict
                    
                    inode_degree[neighbor]=ipull
                    iorigin_degree[node]=inode_degree
            
        for node in G.nodes:
            if current_state[node] == 'I':
                num_inf_camper=int(G.nodes[node]['Infected_camper'])
                
                
            
                #G.edges[node]['Campground_pull']
                #random.choices(degree[node])
        #return next_state
        return Inf_camper, degree, iorigin_degree