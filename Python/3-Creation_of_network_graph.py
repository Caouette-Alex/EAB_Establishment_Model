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
import os
os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding/Python')
import pandas as pd
import networkx as nx
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

#%% Define the initial state of infested locations from non-infested ones and define what happens in the following year
#initial state defines cities that are infested, this is a fixed set of locations: Edmundston, Halifax, Fredericton, Oromocto, and Moncton
prpgl_pres = pd.DataFrame(index = G.nodes)

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
# State transition defines area's that transition from susceptible to infested in a year. 
def state_transition(G, current_state):
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
    inf_city=[]
    for node in G.nodes:
        #if the node is infected, print the number of campers leaving the campground with infested wood/year(per capita value) is calculated, and calculate the total campground pull value from all campgrounds(in degree)
        if current_state[node] == 'I':
            
            # Only cities that are infected can move EAB to different places
            if G.nodes[node]['Type'] == 'city_to_city':
                inf_city.append(node)
                #number of infected campers from Origin location
                nx.set_node_attributes(G,{node:(((G.nodes[node]['Population']*0.0016729+6.24567023)*0.85*(0.3333*210)+(G.nodes[node]['Population']*0.0016729+6.24567023)*0.15*(0.6666*210))*prob_infested_wood)},'Infected_camper')
                #nx.set_node_attributes(G,{node:(G.nodes[node]['Population']*per_capita_value*prob_infested_wood)},'Infected_camper')
                Inf_camper = nx.get_node_attributes(G,'Infected_camper')
                
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
                        P_j=G.nodes[neighbor]['Population']
                        #Mean number of trips made from county A to county B
                        M_ij=G.edges[neighbor,node]['mean_trips_year']
                        D_ij=G.edges[neighbor,node]['Distance_Km']
                    
                        #Calculate attractance value(Pull) load them into a dictionary of dictionary for each infected node
                        #dict : origin_degree = {Origin(node):{Campground(neighbor): normalized_pull}}
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
        #print(num_inf_camper)
        #randomly select campgrounds(v.keys) based on the pull value that each one has(weight) using the number of campers leaving the city with infested firewood
        infected.append(random.choices(list(v.keys()), weights=list(v.values()), k=num_inf_camper[k]))
        #turn a list of lists into a simple list, by removing extra brackets(flatten list)
    infected_flat=[val for subgroup in infected for val in subgroup]
    infected_flat.sort()  
    d = {x:infected_flat.count(x) for x in infected_flat}
    
###
#Distribute infected firewood based on movement of people across cities 
###
    #this loop gets the total pull from all the cities in the in the list from Origin degree cities to a single 
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
    #Changing the state of campground +
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
                        
    firewood_dispersal = {}
    for node in G.nodes:
        if G.nodes[node]['Type'] == 'city_to_camp':
            if current_state[node] == 'S':
                if node in d.keys():
                    firewood_dispersal[node] = (random.choices(['1','2','3','4','5','6'],weights=[109.4,619.67,1521.83,1583.33,559,62], k=d[node]))
    
    from collections import Counter
    
    for k,v in firewood_dispersal.items():
        firewood_dispersal[k] = dict(Counter(v))

    num_count = 10
    for node in G.nodes:
        if G.nodes[node]['Type'] == 'city_to_camp':
            if current_state[node] == 'S':
                if node in firewood_dispersal.keys():
                    if dict((k, v) for k, v in firewood_dispersal[node].items() if v >= int_load):
                        #print(node, firewood_dispersal[node].values())
                        next_state[node] = 'I'
        elif G.nodes[node]['Type'] == 'city_to_city':
            if current_state[node] == 'S':
                if node in d.keys():
                    #print(d[node])
                    if d[node] >=1: 
                        #print(node)
                        next_state[node] = 'I'
    #print(len(d.values()))
    
    
    
    global prpgl_pres
    # TODO s 
    # prpgl_pres[Sim._step()] = pd.Series(d_1)
    return next_state




#%% Run simulations 
import numpy as np
import matplotlib.pyplot as plt
import time


start = time.process_time()

#Run the simulation
#   specify the number of interations that you want to where num_of_sims is the number of iterations of the simulation that you want to run normal amount is 1000
#   Specify the number of years that you want to test in a list like format [5,10,20] = Runs model for 5 years, 10 years, and 20 years
num_of_sims = 10
num_of_years = [5] 
prog_pres = [1,10,25,50]
# Create a dictionary to store the total invasions for the probability of firewood transportation and time to first transportation of firewood in years
total_invas={}

for int_load in prog_pres:
    print("propagule pressure required", int_load)
    # Iterate through each set to measure the number of each moved in each set.
    
    for year in num_of_years:
        prop_list=[]    
        #create two dataframes one that measures if a single piece of wood is transported to the destination
        invas_prob = pd.DataFrame(index=G.nodes)
        invas_time = pd.DataFrame(index=G.nodes)
        prop_infect = pd.DataFrame(index=range(1,year+1))
        invas_propagule = pd.DataFrame(index=G.nodes)
    
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
            Sim.invasion_time()
            #Append each simulation time to invasion as a column in a dataframe
            invas_time[i] = invas_time.index.map(Sim._time_invas)
            invas_prob[i] = invas_prob.index.map(Sim._prob_invas)
            prop_infect[i] = prop_infect.index.map(Sim._prop_infect)
        invas_prob = invas_prob.fillna(0)
        sum_invas_prob_df = invas_prob.transpose().describe().transpose() 
        sum_invas_time_df = invas_time.transpose().describe().transpose()
        total_invas[year] = {'invas_prob':invas_prob,'sum_invas_prob_df':sum_invas_prob_df,'invas_time':invas_time,'sum_invas_time_df':sum_invas_time_df,'prop_infect':prop_infect}
print(time.process_time() - start)

#%%
"""Write dictionary of dataframes to separate sheets, within 
    1 file."""
    
os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Model_results')

from datetime import datetime
path = 'Sim_'+ datetime.today().strftime('%Y-%m-%d')+'_'+ str(num_of_sims)+ str(num_of_years)+'invas_bundle_test.xls'

writer = pd.ExcelWriter(path, engine='xlsxwriter')
#this names and adds each dataframe as sheet in the excel file 
for k,v in total_invas.items():
    for key,dframe in v.items():
        dframe.to_excel(writer, sheet_name=(str(k)+key))

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