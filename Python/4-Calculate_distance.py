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

os.chdir("/..")
os.chdir("Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding/Camping_data")

edgelist_df= pd.read_csv('Edgelist.csv')

G= ox.graph_from_place('Alberta, Canada')

fig, ax= ox.plot_graph(G)

# Retrieve nodes and edges
nodes, edges = ox.graph_to_gdfs(G)
nodes.head()

# Plot the nodes
fig, ax = plt.subplots(figsize=(12,8))
nodes.plot(ax=ax, facecolor='black')


