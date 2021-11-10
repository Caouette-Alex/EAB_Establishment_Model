# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 09:58:54 2021

@author: alexp

Clean data and create an edgelist
"""

import pandas as pd
import os


os.chdir('\..')
os.chdir("Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Coding/Camping_data/")

camp_df = pd.read_csv('Parks_and_camping_Master_2021-10-27.csv')
city_df = pd.read_csv('Cities_Master_2021-10-12.csv')

city_df = city_df.rename(columns={'Latitude':'Lat','Longitude':'Long','Province':'Prov','Geographic_Name': 'Name'})
city_df['index1'] = city_df.index

#Remove any values that don't include real numbers to simplify(this can be removed when the campground data sheet is cleaned up)
import numpy as np
camp_df=camp_df.replace('?',np.NaN).replace(r'^\s*$',np.NaN,regex=True).replace('>50',np.NaN).replace('>45',np.NaN).replace('>60',np.NaN)
#Fill NAN sites to have zero 
camp_df['Sites'] = camp_df['Sites'].fillna(0)
#include only pertinent columns
camp_df= camp_df[['Type of Campground', 'Name', 'Province', 'Sites', 'Latitude', 'Longitude', 'Aquiring firewood']]
#Change data type of Sites, Latitude, and Longitude
camp_df= camp_df.astype({'Sites':'int32','Latitude':'float64', 'Longitude':'float64' })
camp_df= camp_df.replace(0,np.NaN).dropna(subset=['Latitude'])
camp_df= camp_df.rename(columns={'Name':'Dest_name','Latitude':'Dest_lat','Longitude':'Dest_long'})
camp_df = camp_df

#Multiply the rows of camp_df and city_df to have the same number of replicates 
Rep_camp_df = pd.concat([camp_df]*len(city_df.index), ignore_index=True)
Rep_city_df = pd.concat([city_df]*len(camp_df.index), ignore_index=True).sort_values(by=['index1']).reset_index().rename(columns= {'Name':'Orig_name','Lat':'Orig_lat', 'Long':'Orig_long','Population':'Orig_pop','Prov':'Orig_prov'})
Edgelist_citytocamp_df = Rep_camp_df.join(Rep_city_df[['Orig_name','Orig_pop','Orig_lat','Orig_long']]) 
Edgelist_citytocamp_df['type'] = 'city_to_camp'


#Create an edgelist of cities going to other cities and their connections by duplicating city numbers
city_target_df= pd.concat([city_df]*len(city_df.index), ignore_index=True).rename(columns = {'Name':'Dest_name','Lat':'Dest_lat','Long':'Dest_long','Population':'Dest_pop',})
city_source_df= pd.concat([city_df]*len(city_df.index), ignore_index=True).sort_values(by=['index1']).reset_index().rename(columns = {'Name':'Orig_name','Lat':'Orig_lat', 'Long':'Orig_long','Population':'Orig_pop','Prov':'Orig_prov'})
Edgelist_citytocity_df = city_target_df[['Dest_name','Dest_pop','Dest_lat','Dest_long']].join(city_source_df[['Orig_name','Orig_pop','Orig_lat','Orig_long']]) 
Edgelist_citytocity_df['type'] = 'city_to_city'

Edgelist_df= Edgelist_citytocamp_df.append(Edgelist_citytocity_df)
#Create two separate csv files with the edgelist of campground to city and city to city(use this to run Network analyst distance between locations twice separately)
Edgelist_citytocamp_df.to_csv('Edgelist_citytocamp.csv')
Edgelist_citytocity_df.to_csv('Edgelist_citytocity.csv')

Edgelist_df.to_csv('Edgelist.csv')