# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 17:41:20 2021

@author: alexp
"""

import pandas as pd
import os

os.chdir('\..')
#os.getcwd()
os.chdir("Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding/Camping_data")
#%%

#Create dataframe of City to campground distance data pulled from Arcmap
dist_camp_df = pd.read_csv('Distance_camp_city.csv')
dist_camp_df = dist_camp_df[['Name','Total_Leng']].rename(columns={'Total_Leng':'Distance_Km'})
dist_camp_df['Distance_Km'] = dist_camp_df['Distance_Km']/1000

#Open edgelist of city to campground locations
camp_df = pd.read_csv('Edgelist_citytocamp.csv').rename(columns={'Unnamed: 0':'ID'})
#Merge dataframes to a single edgelist dataframe including the population size,number campsites, distance, etc..
camp_edgelist = camp_df.merge(dist_camp_df, left_on='ID', right_on='Name')
#%%

#Create dataframe of City to city distance data pulled from Arcmap
dist_city_df = pd.read_csv('Distance_city_city.csv')
dist_city_df = dist_city_df[['Name','Total_Leng']].rename(columns={'Total_Leng':'Distance_Km'})
dist_city_df['Distance_Km'] = dist_city_df['Distance_Km']/1000

#Open edgelist of city to campground locations
city_df = pd.read_csv('Edgelist_citytocity.csv').rename(columns={'Unnamed: 0':'ID'})
#Merge dataframes to a single edgelist dataframe including the population size,number campsites, distance, etc..
city_edgelist = city_df.merge(dist_city_df, left_on='ID', right_on='Name')
#%%
Edgelist_df= camp_edgelist.append(city_edgelist)

Edgelist_df.to_csv('Edgelist.csv')