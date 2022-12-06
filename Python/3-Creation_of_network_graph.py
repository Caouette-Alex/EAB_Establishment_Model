# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 11:13:42 2021

@author: alexp

This file takes the edgelist of origin and destination locations to simulate the probability that a location see's the transportation of invasive buprestid infested firewood by human movement,
 the introduction of the emerald ash borer from the firewood into local trees, and their establishment by surmounting the allee effect.



To do this we use the edgelist created from (C:/Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding/Python/2-Merge_distance_to_edgelist.py) and simulate the movement of firewood
an origin(infested city) to a destination(susceptible city or campground).
Each simulation iteration starts with the current infested cities: Edmundston, Halifax, Fredericton, Moncton, and Oromocto and estimates the number of infested firewood leaving the origin and being distributed randomly based on weighted values.
We then extract data from the simulations into dataframes, including the transportation of firewood to destination after set period of time, the time to the first transportation of firewood, the number of propagules per year
"""
#%% Import packages and add edgelist dataframe

###
#Import files and packages we have to start at the python directort to import the simulation package written to run this simulation
###
import os
os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding/Python')
import pandas as pd
import networkx as nx
#imported from files from the book by filippo Menczer, Santo Fortunato, and Clayton Davies A first Course in Network Science
from B_Simulation import Simulation

#Change directory to open to where the majority of the data is
os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding')

#Open edgelist of camping and cities that are interconnected, inlcudes population, sites, lat and long, From file 2-Merge_distance_to_edgelist.py
edgelist_df= pd.read_csv('Camping_data/Edgelist_Dist_TSRC.csv')
#%% Create Graph
###
#Create Graph from pandas edgelist and insert node and edge attributes
###

G = nx.from_pandas_edgelist(edgelist_df,source='Orig_name',target='Dest_name',edge_attr=['Distance_Km','mean_trips_year'])

#add coordinates to the graph for each  origin and destination node by creating a dictionary of key value pairs using the structure {Dest name: Long, lat}
dict_pos=dict(zip(edgelist_df.Dest_name,list(zip(edgelist_df.Dest_long,edgelist_df.Dest_lat))))
dict_pos.update(dict(zip(edgelist_df.Orig_name,list(zip(edgelist_df.Orig_long,edgelist_df.Orig_lat)))))
nx.set_node_attributes(G, dict_pos, 'pos')
#Adding node attributes to origin locations and destination locations including the site population, number of campsites, and type of edge relationship(city-city vs. city-camp)
nx.set_node_attributes(G, dict(zip(edgelist_df['Orig_name'],edgelist_df['Orig_pop'])),'Population')
nx.set_node_attributes(G, dict(zip(edgelist_df['Dest_name'],edgelist_df['Sites'])),'Sites')
nx.set_node_attributes(G, dict(zip(edgelist_df['Dest_name'],edgelist_df['type'])),'Type')# might need to change this to an edge attribute
nx.set_node_attributes(G, dict(zip(edgelist_df['Dest_name'],edgelist_df['Grid_ID'])),'Grid_ID')
# 




#%% Define states
###
#Define functions for the initial state(start of the model) of infested locations from non-infested ones and define the transition state(what happens each year thereafter)
###

#initial state defines cities that are infested, this is a fixed set of locations: Edmundston, Halifax, Fredericton, Oromocto, and Moncton
def initial_state(G):
    state = {}
    inf_cities = 'Edmundston','Halifax', 'Fredericton', 'Moncton', 'Oromocto'
    for node in G.nodes:
        if node in inf_cities:
            state[node] = 'I'
        else:
            state[node] = 'S'
    nx.set_node_attributes(G,state,'State')
    return state


# State transition defines the crtieria that attract infested firewood from the origin location to the destination location that transitions from susceptible to infested in a year. 
def state_transition(G, current_state):
    
    #import random is used for the random generation of numbers
    import random
    #parameters
    parameter 1= 100
    
    
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
        if current_state[node] == 'I':
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
                
                
                node_degree_camp={}
                node_degree_city={}
                pull_list=[]
                
                #Get the pull of each campground using number of campsites in campground and distance between campground and origin
                for neighbor in G.neighbors(node):
                    #If else statement to separate campgrounds and cities to send 
                        #campgrounds:
                    if G.nodes[neighbor]['Sites'] >1: 
                        #defined variables X_i are the number of campsites, D_ij is the Distance between campground and origin
                        X_i=G.nodes[neighbor]['Sites']
                        D_ij=G.edges[neighbor,node]['Distance_Km']
                        
                        #Calculate attractance value (Pull) load them into a dictionary of dictionary for each infected node
                        #dict : origin_degree = {Origin(node):{Campground(neighbor): attractance}
                        #A majority of campground visits involve relatively short travel distances (<100 km, which is usually a <2-h drive from home) Koch et al. 2012 also see Eagles et al. 2015
                        #TODO _
                        pull = (X_i*(1*(1-0.5))**(D_ij/parameter))
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
            if current_state[node] == 'I':
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
    sup_rate_EAB={'May':0.0635, 'June':0.269, 'July':0.391, 'August':0.0694, 'September':0.002, 'October': 0}
    
    
    
    ###
    #Distribute firewood arriving into campground based on month of arrival change the status of the campground based on the number of introduced load(propagule pressure)
    ###
    
    def firewood_timing_off():
        #iterate through all the nodes in the network
        for node in G.nodes:
            #select on nodes that are attached to campgrounds
            if G.nodes[node]['Type'] == 'city_to_camp':
                #select only campgrounds that are susceptible
                if current_state[node] == 'S':
                    #Select only nodes that have firewood arriving at the campground
                    if node in firewood_dispersal.keys():
                        #Measures if the there are any months within that campground that have a high enough arrival rate that equal or surpasses the establishment threshold required for establishment
                        if dict((k, v) for k, v in firewood_dispersal[node].items() if v >= int_load):
                            #change location from susceptible to infested
                            next_state[node] = 'I'
            #One city becomes infested each year based on random weighted choice from the population and total travel to the area from all the infested locations
            elif G.nodes[node]['Type'] == 'city_to_city':
                #select only cities that are susceptible
                if current_state[node] == 'S':
                    #TODO confirm what the dictionary d has to do at this point
                    if node in d.keys():
                        #Find the city that is selected based on the size and weighted movement of firewood
                        if d[node] >=1: 
                            #change location from susceptible to infested
                            next_state[node] = 'I'
    
    def firewood_timing_on():
        #iterate through all the nodes in the network
        for node in G.nodes:
            #select on nodes that are attached to campgrounds
            if G.nodes[node]['Type'] == 'city_to_camp':
                #select only nodes that are susceptible
                if current_state[node] == 'S':
                    #Select only nodes that have firewood arriving at the campground
                    if node in firewood_dispersal.keys():
                        #Measures if the there are any months within that campground that have a high enough arrival rate that equal or surpasses the int_load
                        #if dict((k, v) for k, v in firewood_dispersal[node].items() if v >= int_load):
                        
                        #Measure the number of pieces of firewood that have emergence based on the month of arrival
                        #Iterate through each month in the dictionary firewood dispersal
                        for month,firewood_load in firewood_dispersal[node].items():
                            #reset the number of pieces of firewood that have emerged
                            emerged_firewood = 0
                            #loop through each piece of firewood to see if it reaches emergence before being burned
                            for piece_firewood in range(firewood_load):
                                #generate a random number between 0-1
                                rand=random.random()
                                # see if the random number is less than the supply rate of emerged firewood
                                if rand < sup_rate_EAB[month]:
                                    #add that firewood to those that have emerged in that month
                                    emerged_firewood = emerged_firewood+1
                            #change the value of arrived firewood to that of firewood that had beetles emerge from it
                            firewood_dispersal[node][month] = emerged_firewood
                        #Measures if the there are any months within that campground that have a high enough arrival rate that equal or surpasses the establishment threshold required for establishment
                        if dict((k, v) for k, v in firewood_dispersal[node].items() if v >= int_load):
                            next_state[node] = 'I'
            #One city becomes infested each year based on random weighted choice from the population and total travel to the area from all the infested locations
            elif G.nodes[node]['Type'] == 'city_to_city':
                #select only cities that are susceptible
                if current_state[node] == 'S':
                    #TODO confirm what the dictionary d has to do at this point
                    if node in d.keys():
                        #Find the city that is selected based on the size and weighted movement of firewood
                        if d[node] >=1: 
                            #change location from susceptible to infested
                            next_state[node] = 'I'
    #Select which package to write
    firewood_timing_on()
    
    return next_state, firewood_dispersal




#%% Run simulations 
import numpy as np
import matplotlib.pyplot as plt
import time


start = time.process_time()

#Run the simulation

#firewood = [firewood_timing_off,firewood_timing_on]
#   specify the number of interations that you want to where num_of_sims is the number of iterations of the simulation that you want to run normal amount is 1000
num_of_sims = 1
#   Specify the number of years that you want to test in a list like format [5,10,20] = Runs model for 5 years, 10 years, and 20 years
num_of_years = [20] 
#   Specify the introduced load required so that a location is considered 
prog_pres = [1]

###
# Dictionary of dictionaries of dictionaries that stores all the measurements of proportion, time, and total numebr of campgrounds with established pops of EAB
# The dictionary has the following structure k1:k2:k3:v3 where k1 = Introduced load(propagule pressure), k2 = is the number of years the simulation runs for, k3 = are the names of dataframes
# Invasion probability(campground infested or not), Invas_time(time point that the campground became infested), Prop_infect(proportion of campgrounds becoming infested based on the year of infestation), descriptive stats of both invas_prob and invas_year
###

total_invas={}
grid_list = []
#Create a list that contains all the grid values from the hexagons
for letter in list(map(chr,range(65,79))):
    for num in range(9):
         grid_list.append(letter+'-'+str(num+1))

# repeat the simulation to iterate through the prog_pres(Propagule pressure) list, that relates to the introduced load required for a location to become infested
for int_load in prog_pres:
    print("propagule pressure required", int_load)
    # TODO Add description of year_invas
    year_invas={}
    # Repeat the simulation based on the number of years list
    for year in num_of_years:
        prop_list=[]    
        
        #create two dataframes one that measures how many campground in the zone is infested and another showing the number of campgrounds that are in each hexagon
        grid_df = pd.DataFrame(index=G.nodes)
        grid_df_counts = pd.DataFrame(index=grid_list)
        #Find the total number of campgrounds inside each grid code in the datasheet (28 is the number of repeated values on the edgelist, there are that many cities)
        grid_df_counts['total_counts'] = grid_df_counts.index.map(edgelist_df['Grid_ID'].value_counts()/28)
        
        #Create data frame to count if a location is infested or not
        invas_prob= pd.DataFrame(index=G.nodes)
        #Create data frame that measures the time that each campground becomes infested
        invas_time = pd.DataFrame(index=G.nodes)
        #Count proportion of campgrounds that are infested each year(col=simulation, row= year)
        prop_infect = pd.DataFrame(index=range(1,year+1))
        
        prop_pres_dict = {}
        
        for i in range(num_of_sims):#1000 repeats
            print('Completed', i, 'Simulations out of', num_of_sims)
            
            #Define the class and the variables inital state and state transition are described above as 
            Sim = Simulation(G, initial_state, state_transition, name='EAB network model')
            #run the simulation
            Sim.run(year)
            print(Sim._test[0][0])
            #Append each simulation time to invasion as a column in a dataframe
            invas_time[i] = invas_time.index.map(Sim._time_invas)
            
            #map whether campgrounds become invaded as a 0 or 1 value
            grid_df[i] =  grid_df.index.map(Sim._grid_invas)
            #convert those values to count the number of infested campgrounds for each locations
            grid_df_counts[i] = grid_df_counts.index.map(grid_df[i].value_counts())
            #add new col for eacb simulation and map to campgrounds
            invas_prob[i] = invas_prob.index.map(Sim._prob_invas)
            #add new col for eacb simulation and map to campgrounds
            prop_infect[i] = prop_infect.index.map(Sim._prop_infect)
            # Iterate through the dictionary of dictionaries{year:{:}} create a dataframe
            invas_propagule = pd.DataFrame(index=G.nodes)
            
            #Add column of Grid ID to number of pieces of firewood showing up in a give month
            index_col = pd.DataFrame.from_dict(dict(G.nodes(data=True)), orient='index')
            invas_propagule['Grid_ID'] = index_col['Grid_ID']
            
            #Create a dataframe for each iteration of simluation and add them together into a dictionary
            for k,v in Sim._prog_pres.items():
                #for k2,v2 in v.items():
                invas_propagule[k] = invas_propagule.index.map(v)
            prop_pres_dict[i] = invas_propagule
        
        #convert nan values to 0 values for the dataframe
        invas_prob = invas_prob.fillna(0)
        
        sum_invas_prob_df = invas_prob.transpose().describe().transpose() 
        sum_invas_time_df = invas_time.transpose().describe().transpose()
        #create a seperate dictionary that contains all the years that the model is run
        prop_pres_dict2 = {year:prop_pres_dict}
        ##create a seperate dictionary that contains all the years that the model is run and have each measurement as a separate page for excel export
        year_invas[year] = {'invas_prob':invas_prob,'sum_invas_prob_df':sum_invas_prob_df,'invas_time':invas_time,'sum_invas_time_df':sum_invas_time_df,'prop_infect':prop_infect,'grid_counts':grid_df_counts}
    
    total_invas[int_load] = year_invas
     
print(time.process_time() - start)

#%%
"""Write dictionary of dataframes to separate sheets, within 
    1 file."""

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Model_results')

#Create a path to save the file including the date, number of simulations, number of years, and whether firewood timing is on or off
from datetime import datetime
path = 'Sim_'+ datetime.today().strftime('%Y-%m-%d')+'_'+ str(num_of_sims)+ str(num_of_years)+'Establishment_fire_on.xls'

#
writer = pd.ExcelWriter(path, engine='xlsxwriter')
#loop through all the dataframes in the dictionary and adds each dataframe as sheet in the excel file 
for k,v in total_invas.items():
    for k1,v1 in v.items():
        for k2,dframe in v1.items():
            #save datafram using sheetnames as k = number of years run, k=measured main sheet name
            dframe.to_excel(writer, sheet_name=(str(k)+str(k2)))

writer.save()

#create a path to save the file as including the date, number of simulations, number of years, and that's its the introduction model
path = 'Sim_'+ datetime.today().strftime('%Y-%m-%d')+'_'+ str(num_of_sims)+ str(num_of_years)+'Introduction.xls'

# save each simualtion as a separate datasheet
intro_writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
for k,v in prop_pres_dict2.items():
    for k1,dframe in v.items():
        dframe.to_excel(intro_writer, sheet_name=('years#'+str(k)+'_sim#'+str(k1)))

intro_writer.save()

#%%
'''Run a single simulation printing an image in each year to represent the change of susceptible to established campgrounds in the model'''
Sim = Simulation(G, initial_state, state_transition, name='EAB network model')
from matplotlib import pyplot as plt
figures = []
n= 20
int_load = 3

for i in range(n):
    figures.append(Sim.draw())
    #filename = str(i) + '.png'
    Sim.run(1)
    #i = Sim.draw()
    #plt.show() 
    #plt.savefig(filename)
    figures.append(Sim.draw())

fig_names = []
for idx, fig in enumerate(figures):
    fname = '{}_tmp.jpg'.format(idx)
    fig.savefig(fname)
    fig_names.append(fname)
    
import imageio
images = []
for filename in fig_names:
    images.append(imageio.imread(filename))
imageio.mimsave('movie.gif', images, duration = 0.75)

#import imageio
#with imageio.get_writer('mygif.gif', mode='I') as writer:
    #for filename in ['1.png', '2.png', '3.png', '4.png']:
        #image = imageio.imread(filename)
        #writer.append_data(image)
