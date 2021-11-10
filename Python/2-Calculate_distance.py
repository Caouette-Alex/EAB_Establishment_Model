# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 14:25:04 2021

@author: alexp
"""
from shapely.geometry import shape
from shapely.geometry import LineString

import geopandas as gpd
import pandas as pd
import networkx as nx
import osmnx as ox
import os
import matplotlib.pyplot as plt
import time
from osgeo import osr,ogr

os.chdir("/..")
os.chdir("Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding/Camping_data")

edgelist_df= pd.read_csv('Edgelist.csv')

ox.config(timeout=10000)
start = time.time()
G= ox.graph_from_place(['New Brunswick, Canada','Prince Edward Island, Canada','Nova Scotia, Canada'], network_type='drive')
end = time.time()
print(end - start)

fig, ax= ox.plot_graph(G)


def nodes_to_linestring(path):
    coords_list = [(G.nodes[i]['x'], G.nodes[i]['y']) for i in path ]
    #print(coords_list)
    line = LineString(coords_list)
    
    return(line)

#%%
def shortestpath(o_lat, o_long, d_lat, d_long):
    
    nearestnode_origin, dist_o_to_onode = ox.distance.get_nearest_node(G, (o_lat, o_long), method='haversine', return_dist=True)
    nearestnode_dest, dist_d_to_dnode = ox.distance.get_nearest_node(G, (d_lat, d_long), method='haversine', return_dist=True)
    
    #Add up distance to nodes from both o and d ends. This is the distance that's not covered by the network
    dist_to_network = dist_o_to_onode + dist_d_to_dnode
    
    shortest_p = nx.shortest_path(G,nearestnode_origin, nearestnode_dest) 
    
    route = nodes_to_linestring(shortest_p) #Method defined above
    
    # Calculating length of the route requires projection into UTM system.  
    inSpatialRef = osr.SpatialReference()
    inSpatialRef.ImportFromEPSG(4326)
    outSpatialRef = osr.SpatialReference()
    outSpatialRef.ImportFromEPSG(32643)
    coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
    
    #route.wkt returns wkt of the shapely object. This step was necessary as transformation can be applied 
    #only on an ogr object. Used EPSG 32643 as Bangalore is in 43N UTM grid zone.
    geom = ogr.CreateGeometryFromWkt(route.wkt)
   
    geom.Transform(coordTransform)
    length = geom.Length()
    
    #Total length to be covered is length along network between the nodes plus the distance from the O,D points to their nearest nodes
    total_length = length + dist_to_network
    #in metres
    
    return(route, total_length )
#%%







Source_lat_col=edgelist_df['Source_Lat']
Source_long_col=edgelist_df['Source_Long']
Target_lat_col=edgelist_df['Target_Lat']
Target_long_col=edgelist_df['Target_Long']


#orig_node = ox.nearest_nodes(G, X = edgelist_df['Source_Lat'], Y = edgelist_df['Source_Long'])
#dest_node = ox.nearest_nodes(G, X = edgelist_df['Target_Lat'], Y = edgelist_df['Target_Long'])
orig_node = ox.nearest_nodes(G, X = Source_lat_col[6052], Y = Source_long_col[6052])
dest_node = ox.nearest_nodes(G, X = Target_lat_col[6052], Y = Target_long_col[6052])

route = ox.shortest_path(G, orig_node, dest_node)
edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, "length")
round(sum(edge_lengths))

# Retrieve nodes and edges
#nodes, edges = ox.graph_to_gdfs(G)
#nodes.head()

# Plot the nodes
#fig, ax = plt.subplots(figsize=(12,8))
#nodes.plot(ax=ax, facecolor='black')


