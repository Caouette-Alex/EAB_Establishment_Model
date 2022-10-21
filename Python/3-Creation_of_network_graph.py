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
            if current_state[node] == 'S':
                if node in d.keys():
                    #randomly distribute pieces of firewood based on the weights of reservation months. campgrounds are separated by month, weights= number of res, made per year, k= number of pieces of firewood that show up in a year
                    firewood_dispersal[node] = (random.choices(list(reservations_month.keys()),weights=list(reservations_month.values()), k=d[node]))
    
    from collections import Counter
    #Count the total number of pieces of firewood distributed to each month
    for k,v in firewood_dispersal.items():
        firewood_dispersal[k] = dict(Counter(v))
    
    ###
    #Distribute firewood arriving into campground based on month of arrival change the status of the campground based on the number of introduced load(propagule pressure)
    ###
    
    for node in G.nodes:
        if G.nodes[node]['Type'] == 'city_to_camp':
            if current_state[node] == 'S':
                if node in firewood_dispersal.keys():
                    #Measures if the there are any months within that campground that have a high enough arrival rate that equal or surpasses the int_load
                    if dict((k, v) for k, v in firewood_dispersal[node].items() if v >= int_load):
    
                        next_state[node] = 'I'
        #This changes the state of the one city that changes that year
        elif G.nodes[node]['Type'] == 'city_to_city':
            if current_state[node] == 'S':
                if node in d.keys():
                    
                    if d[node] >=1: 
                       
                        next_state[node] = 'I'
    
    
    return next_state, firewood_dispersal




#%% Run simulations 
import numpy as np
import matplotlib.pyplot as plt
import time


start = time.process_time()

#Run the simulation


#   specify the number of interations that you want to where num_of_sims is the number of iterations of the simulation that you want to run normal amount is 1000
num_of_sims = 2
#   Specify the number of years that you want to test in a list like format [5,10,20] = Runs model for 5 years, 10 years, and 20 years
num_of_years = [20] 
#   Specify the introduced load required so that a location is considered 
prog_pres = [2,6]

###
# Dictionary of dictionaries of dictionaries that stores all the measurements of proportion, time, and total numebr of campgrounds with established pops of EAB
# The dictionary has the following structure k1:k2:k3:v3 where k1 = Introduced load(propagule pressure), k2 = is the number of years the simulation runs for, k3 = are the names of dataframes
# Invasion probability(campground infested or not), Invas_time(time point that the campground became infested), Prop_infect(proportion of campgrounds becoming infested based on the year of infestation), descriptive stats of both invas_prob and invas_year
###

total_invas={}
grid_list = []
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
        # TODO Find the count of campgrounds inside each grid code in the datasheet (28 is the number of repeated values on the edgelist, there are that many cities
        grid_df_counts['total_counts'] = grid_df_counts.index.map(edgelist_df['Grid_ID'].value_counts()/28)
        invas_prob= pd.DataFrame(index=G.nodes)
        invas_time = pd.DataFrame(index=G.nodes)
        prop_infect = pd.DataFrame(index=range(1,year+1))
        invas_propagule = pd.DataFrame(index=G.nodes)
        d = {}
        for i in range(num_of_sims):#1000 repeats
            print('Completed', i, 'Simulations out of', num_of_sims)
            
            #Define the class and the variables inital state and state transition are described above as 
            Sim = Simulation(G, initial_state, state_transition, name='EAB network model')
            #run the simulation
            Sim.run(year)
            #Draw the network at each interval of nth steps()
            #Sim.draw()
            #plt.show()
            
            #Draw the proportions of infested nodes vs. susceptible nodes from time 0 to nth steps()
            #Sim.plot()
            #plt.show()
            #Show the time to invasion for each city c
            #Sim.invasion_time()
            #Append each simulation time to invasion as a column in a dataframe
            invas_time[i] = invas_time.index.map(Sim._time_invas)
            
            grid_df[i] =  grid_df.index.map(Sim._grid_invas)
            grid_df_counts[i] = grid_df_counts.index.map(grid_df[i].value_counts())
            #invas_propagule[i] = invas_propagule(Sim._propagule_pres)
            invas_prob[i] = invas_prob.index.map(Sim._prob_invas)
            prop_infect[i] = prop_infect.index.map(Sim._prop_infect)
            for k,v in Sim._test.items():
                for k2,v2 in v.items():
                    invas_propagule[i] = invas_propagule.index.map(v2)
                    d['propagule_pres'] = invas_propagule
        invas_prob = invas_prob.fillna(0)
        sum_invas_prob_df = invas_prob.transpose().describe().transpose() 
        sum_invas_time_df = invas_time.transpose().describe().transpose()
        d2 = {year:d}
        year_invas[year] = {'invas_prob':invas_prob,'sum_invas_prob_df':sum_invas_prob_df,'invas_time':invas_time,'sum_invas_time_df':sum_invas_time_df,'prop_infect':prop_infect,'grid_counts':grid_df_counts}
    total_invas[int_load] = {'Est':year_invas,'Int':d2}
print(time.process_time() - start)

#%%
"""Write dictionary of dataframes to separate sheets, within 
    1 file."""
    
os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Model_results')

from datetime import datetime
path = 'Sim_'+ datetime.today().strftime('%Y-%m-%d')+'_'+ str(num_of_sims)+ str(num_of_years)+'invas_grid_counts.xls'

writer = pd.ExcelWriter(path, engine='xlsxwriter')
#this names and adds each dataframe as sheet in the excel file 
for k,v in total_invas.items():
    for k1,v1 in v.items():
        for k2,v2 in v1.items():
            for k3,dframe in v2.items():
                dframe.to_excel(writer, sheet_name=(str(k)+str(k2)+str(k3)))
    #for k1,v1 in v[1].items():
         #for k2,dframe in v1.items():
             #v1.to_excel(writer, sheet_name=(str(k)+k2))
writer.save()
#%%

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Model_results')
df= pd.DataFrame()
for k,v in total_invas.items():
    #for dataframe in interval:
    df[k] = v[0]['mean']
df_coord = df.join(pd.DataFrame.from_dict(dict_pos,orient ='index')).rename(columns = {0:'lat', 1:'long'})
from datetime import datetime
filename = 'Sim_'+ datetime.today().strftime('%Y-%m-%d')+'_'+ str(num_of_sims)+'_Mean_invasion_probability_per_year'
df_coord.to_csv(filename)

df2 = pd.DataFrame()
for k,v in total_invas.items():
    #for dataframe in interval:
    df2[k] = v[1]['mean']
df_coord = df2.join(pd.DataFrame.from_dict(dict_pos,orient ='index')).rename(columns = {0:'lat', 1:'long'})

filename = 'Sim_'+ datetime.today().strftime('%Y-%m-%d')+'_'+ str(num_of_sims)+'_Mean_invasion_year'
df_coord.to_csv(filename)
#save data to CSV file using the following format Sim_YYYY_MM_DD_####(number of simulations)


filename = 'Sim_'+ datetime.today().strftime('%Y-%m-%d')+'_'+ str(num_of_sims)
invas_time.to_csv(filename)

print(time.process_time() - start)
#%%
from datetime import datetime
os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Model_results')
filename = 'Sim_'+ datetime.today().strftime('%Y-%m-%d')+'_'+ str(num_of_sims)+'_Mean_invasion_year'
sum_invas_time_df.to_csv(filename)


        
#%%
Sim = Simulation(G, initial_state, state_transition, name='EAB network model')
from matplotlib import pyplot as plt
figures = []
n= 20

for i in range(n):
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
#%% Draw the graph with node lat and long without running the simulation

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding')

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np
#add
pos=nx.get_node_attributes(G, 'pos')
fig     = plt.figure()
ax      = fig.add_subplot(111)

city_nodes = [n
   for (n, ty) in \
      nx.get_node_attributes(G, 'Type').items() if ty == 'city_to_city']

camp_nodes = [n  
    for (n, ty) in \
      nx.get_node_attributes(G, 'Type').items() if ty == 'city_to_camp']


plt.rcParams['figure.dpi'] = 300
#Create the outer edges of the image
map = Basemap(llcrnrlon=-68.6,llcrnrlat=43.42,urcrnrlon=-59.68,urcrnrlat=48.07,resolution='l', ellps='WGS84',lat_0=-64.37, lon_0=45.73)
# Get shapegfile data and colour it by provincs
map.readshapefile("maritime_prov1", "states")
patches   = []
for info, shape in zip(map.states_info, map.states):
    if info['Name_EN'] == 'New Brunswick' or 'Nova Scotia' or 'Prince Edward Island' :
        patches.append( Polygon(np.array(shape), True) )
ax.add_collection(PatchCollection(patches, facecolor= 'coral', edgecolor='k', linewidths=1., zorder=0))

# add other boundaries and colour in water as blue and other states as grey
map.drawmapboundary(fill_color='paleturquoise',zorder=-2)
map.drawstates(linewidth=0.2)
map.fillcontinents(color='gray',zorder=-1)
map.drawcoastlines()

#draw the network graph
#nx.draw_networkx(G,pos=nx.get_node_attributes(G, 'pos'), with_labels=True,font_size=1,node_size=8,node_color='green', width=0.05)
nx.draw_networkx_edges(G, pos,width=0.05 )
nx.draw_networkx_nodes(G, pos, nodelist = city_nodes, node_shape = '^', node_size=8,node_color='green')
nx.draw_networkx_nodes(G, pos, nodelist = camp_nodes, node_shape = 'o', node_size=8,node_color='green')

#pos = nx.get_node_attributes(self.G, 'pos')
#city_pos = nx.get_node_attributes([x for x,y in self.G.nodes(data=True) if y['Type'] == 'city_to_city'], 'pos')
#camp_pos = nx.get_node_attributes(self.G, 'pos')
#nx.draw_networkx_edges(self.G, pos,width=0.05 )
#nx.draw_networkx_nodes(self.G, city_pos, nodelist = city_nodes, node_shape = 's', node_size=8, node_color = node_colors)
#nx.draw_networkx_nodes(self.G, pos, nodelist = camp_nodes, node_shape = 'o', node_size=8, node_color = node_colors)

plt.show()



#%% Test Variables
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
lon1s = df_coord['lat'].tolist()
lat1s = df_coord['long'].tolist()
# make-up list of 3-values data for the locations above
# -----------------------------------------------------
coord = df_coord.to_dict('split')


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