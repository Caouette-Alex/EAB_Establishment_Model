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

camp_df = pd.read_csv('Parks_and_camping_Master_2021-10-13.csv')
city_df = pd.read_csv('Cities_Master_2021-10-12.csv')

city_df = city_df.rename(columns={'Latitude':'city_Lat','Longitude':'city_Long','Province':'City_prov'})
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
camp_df= camp_df.rename(columns={'Latitude':'camp_Lat','Longitude':'camp_Long'})


Camp_df = pd.concat([camp_df]*len(city_df.index), ignore_index=True)

City_df = pd.concat([city_df]*len(camp_df.index), ignore_index=True).sort_values(by=['index1']).reset_index()

Edgelist_df = Camp_df.join(City_df[['Geographic_Name','Population','city_Lat','city_Long']]) 

Edgelist_df.to_csv('Edgelist.csv')