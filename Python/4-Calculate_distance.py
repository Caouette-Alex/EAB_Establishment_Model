# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 14:25:04 2021

@author: alexp
"""

import geopandas as gpd
import pandas as pd
import networkx as nx
import osmnx as ox

edgelist_df= pd.read_csv('Edgelist.csv')

G= ox.graph_from_place(['New Brunswick, Canada','Nova Scotia, Canada', 'Prince Edward Island, Canada'])

ox.plot_graph(G)