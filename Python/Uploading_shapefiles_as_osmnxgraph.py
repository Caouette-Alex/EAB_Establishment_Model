# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 06:53:59 2021

@author: alexp
"""
import osmnx as ox
import geopandas as gpd

# load GeoPackage as node/edge GeoDataFrames indexed as described in OSMnx docs
gdf_nodes = gpd.read_file('Maritime_road_network.gpkg', layer='nodes').set_index('osmid')
gdf_edges = gpd.read_file('Maritime_road_network.gpkg', layer='edges').set_index(['u', 'v', 'key'])
assert gdf_nodes.index.is_unique and gdf_edges.index.is_unique

# convert the node/edge GeoDataFrames to a MultiDiGraph
graph_attrs = {'crs': 'epsg:4326', 'simplified': True}
G2 = ox.graph_from_gdfs(gdf_nodes, gdf_edges, graph_attrs)

