# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 12:08:02 2021

@author: alexp
"""

from shapely.geometry import shape
from shapely.geometry import LineString

from osgeo import ogr, osr
import geopandas as gpd
import pandas as pd
import time
import networkx as nx
import osmnx as ox
import os
#%%
#Read the Origin-Destination csv
os.chdir("/..")
os.chdir("Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding/Camping_data")


start = time.time()
G= ox.graph_from_place(['New Brunswick, Canada','Nova Scotia, Canada','Prince Edward Island, Canada'])
end = time.time()
print(end - start)

fig, ax = ox.plot_graph(G)

#%%
#ox.save_graph_xml(G, filepath="test.xml", oneway=True)
#ox.save_graph_geopackage(G, filepath='test.gpkg')
#%%
Gs=ox.utils_graph.get_largest_component(G,strongly=True)
edgelist_df= pd.read_csv('Edgelist.csv')

def nodes_to_linestring(path):
    coords_list = [(Gs.nodes[i]['x'], Gs.nodes[i]['y']) for i in path ]
    #print(coords_list)
    line = LineString(coords_list)
    
    return(line)

def shortestpath(Orig_lat, Orig_long, Dest_lat, Dest_long):
    
    nearestnode_origin, dist_o_to_onode = ox.distance.nearest_nodes(Gs, X = Orig_long, Y = Orig_lat, return_dist=True)
    nearestnode_dest, dist_d_to_dnode = ox.distance.nearest_nodes(Gs, X = Dest_long, Y = Dest_lat, return_dist=True)
    
    #Add up distance to nodes from both o and d ends. This is the distance that's not covered by the network
    dist_to_network = dist_o_to_onode + dist_d_to_dnode
    
    shortest_p = nx.shortest_path(Gs,nearestnode_origin, nearestnode_dest) 
    
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

start_time = time.time()

edgelist_df['osmnx_geometry'] = edgelist_df.apply(lambda x: shortestpath(x['Orig_lat'], x['Orig_long'], x['Dest_lat'], x['Dest_long'])[0] , axis=1)
edgelist_df['osmnx_length'] = edgelist_df.apply(lambda x: shortestpath(x['Orig_lat'], x['Orig_long'], x['Dest_lat'], x['Dest_long'])[1] , axis=1)

print("Time taken: ", (time.time() - start_time), "seconds")
#