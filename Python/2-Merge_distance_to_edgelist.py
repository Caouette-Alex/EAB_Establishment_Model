# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 17:41:20 2021

@author: alexp

This file takes the edgelist from (C:/Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding/Python/1-Create_edgelist.py) to add distance and travel between origin and destination

"""
import numpy as np
import pandas as pd
import os

os.chdir('\..')
#os.getcwd()
os.chdir("Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding")
#%%

#Create dataframe of City to campground distance data pulled from Arcmap
dist_camp_df = pd.read_csv('Camping_data/Distance_camp_city.csv')
dist_camp_df = dist_camp_df[['Name','Total_Leng']].rename(columns={'Total_Leng':'Distance_Km'})
dist_camp_df['Distance_Km'] = dist_camp_df['Distance_Km']/1000

#Open edgelist of city to campground locations
camp_df = pd.read_csv('Camping_data/Edgelist_citytocamp.csv').rename(columns={'Unnamed: 0':'ID'})
#Merge dataframes to a single edgelist dataframe including the population size,number campsites, distance, etc..
camp_edgelist = camp_df.merge(dist_camp_df, left_on='ID', right_on='Name').dropna(subset=['Sites'])

#Create dataframe of City to city distance data pulled from Arcmap
dist_city_df = pd.read_csv('Camping_data/Distance_city_city.csv')
dist_city_df = dist_city_df[['Name','Total_Leng']].rename(columns={'Total_Leng':'Distance_Km'})
dist_city_df['Distance_Km'] = dist_city_df['Distance_Km']/1000

#Open edgelist of city to campground locations
city_df = pd.read_csv('Camping_data/Edgelist_citytocity.csv').rename(columns={'Unnamed: 0':'ID'})
#Merge dataframes to a single edgelist dataframe including the population size,number campsites, distance, etc..
city_edgelist = city_df.merge(dist_city_df, left_on='ID', right_on='Name') 
city_edgelist['Distance_Km'] = city_edgelist['Distance_Km'].replace(0, np.nan)
city_edgelist = city_edgelist.dropna(subset=['Distance_Km'])
#fill all empty 
Edgelist_df= camp_edgelist.append(city_edgelist).fillna(-1)

Edgelist_df.to_csv('Camping_data/Edgelist_dist.csv')

#%%
"""
Add the TSRC travel data to the columns

"""
Edgelist_df['CDUID_joined'] = Edgelist_df['Orig_CDUID'].astype(str) + '_' + Edgelist_df['Dest_CDUID'].astype(str)

TSRC_raw = pd.read_csv('TSRC/TSRC_values.csv')
#TSRC_values['CDUID_joined'] = TSRC_values['orig_code'].astype(str) + '_' + TSRC_values['dest_code'].astype(str)
TSRC_raw = TSRC_raw.rename(columns={'join_code':'CDUID_joined'})

TSRC_mean = TSRC_raw[['CDUID_joined','mean_trips_year']]

Edgelist_join_df= Edgelist_df.merge(TSRC_mean, on='CDUID_joined',how='outer').fillna(0.00000000000001)



Edgelist_join_df['trips_norm'] = Edgelist_join_df['mean_trips_year']/(Edgelist_join_df['mean_trips_year'].sum())

Edgelist_join_df.to_csv('Camping_data/Edgelist_Dist_TSRC.csv')