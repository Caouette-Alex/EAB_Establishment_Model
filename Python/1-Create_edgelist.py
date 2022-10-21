# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 09:58:54 2021

@author: alexp

Take information from campgrounds and cities in the maritimes and create an edgelist of origin and destinations including city->city and city->campground
This involves cleaning the data by removing nan rows and keeping only columns that we are interested in
We create two dataframes of city to city and of city to campground (edge between each connection) 
The dataframe is then merged into one dataframe containing both city->camp edges and city->camp edges

"""

import pandas as pd
import os

#change 
os.chdir('\..')
os.chdir("Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/")

camp_df = pd.read_csv('Coding/Camping_data/Parks_and_camping_Master_2022-10-06.csv')
city_df = pd.read_csv('Coding/Camping_data/Cities_Master_2021-12-07.csv').sort_values(by='Geographic_Name').reset_index()

#import the dictionary codes for the Census divisions of each campground and city
#cen_camp_dic = pd.read_csv('Coding/Camping_data/Cen_div_camp.csv').drop(columns='Name')
cen_city_dic = pd.read_csv('Coding/City_data/Cen_div_city.csv').sort_values(by='Orig_name').reset_index(drop=True).rename(columns={'Orig_name': 'Name'})

city_df = city_df.rename(columns={'Latitude':'Lat','Longitude':'Long','Province':'Prov','Geographic_Name': 'Name'})
#join a the TSRC data to the camp and city data
#camp_df = camp_df.merge(cen_camp_dic, on='Key')
city_df = city_df.merge(cen_city_dic, on='Name')


city_df['index1'] = city_df.index

#Remove any values that don't include real numbers to simplify(this can be removed when the campground data sheet is cleaned up)
import numpy as np
camp_df=camp_df.replace('?',np.NaN).replace(r'^\s*$',np.NaN,regex=True).replace('>50',np.NaN).replace('>45',np.NaN).replace('>60',np.NaN)
#Fill NAN sites to have zero 
camp_df['Sites'] = camp_df['Sites'].fillna(0)
#include only pertinent columns
camp_df= camp_df[['Type of Campground', 'Name','Province', 'Sites', 'Latitude', 'Longitude','Grid_ID', 'Aquiring firewood']]
#Change data type of Sites, Latitude, and Longitude
camp_df= camp_df.astype({'Sites':'int32','Latitude':'float64', 'Longitude':'float64' })
camp_df= camp_df.replace(0,np.NaN).dropna(subset=['Latitude'])
camp_df= camp_df.rename(columns={'Name':'Dest_name','Latitude':'Dest_lat','Longitude':'Dest_long', 'CDUID':'Dest_CDUID'})
camp_df = camp_df

Grid_ID_count = camp_df['Grid_ID'].value_counts()

#Multiply the rows of camp_df and city_df to have the same number of replicates 
Rep_camp_df = pd.concat([camp_df]*len(city_df.index), ignore_index=True)
Rep_city_df = pd.concat([city_df]*len(camp_df.index), ignore_index=True).sort_values(by=['index1']).reset_index().rename(columns= {'Name':'Orig_name','Lat':'Orig_lat', 'Long':'Orig_long','Population':'Orig_pop','Prov':'Orig_prov'})
Edgelist_citytocamp_df = Rep_camp_df.join(Rep_city_df[['Orig_name','Orig_pop','Orig_lat','Orig_long']]) 
Edgelist_citytocamp_df['type'] = 'city_to_camp'


#Create an edgelist of cities going to other cities and their connections by duplicating city numbers
city_target_df= pd.concat([city_df]*len(city_df.index), ignore_index=True).rename(columns = {'Name':'Dest_name','Prov': 'Province','Lat':'Dest_lat','Long':'Dest_long','Population':'Dest_pop','CDUID': 'Dest_CDUID'})
city_source_df= pd.concat([city_df]*len(city_df.index), ignore_index=True).sort_values(by=['index1']).reset_index().rename(columns = {'Name':'Orig_name','Lat':'Orig_lat', 'Long':'Orig_long','Population':'Orig_pop','Prov':'Orig_prov','CDUID': 'Orig_CDUID'})
Edgelist_citytocity_df = city_target_df[['Dest_name','County','Province','Dest_pop','Dest_lat','Dest_long','Dest_CDUID']].join(city_source_df[['Orig_name','Orig_pop','Orig_lat','Orig_long','Orig_CDUID']]) 
Edgelist_citytocity_df['type'] = 'city_to_city'

Edgelist_citytocamp_df = Edgelist_citytocamp_df.reset_index(drop=True)
Edgelist_citytocity_df = Edgelist_citytocity_df.reset_index(drop=True)

Edgelist_df= pd.concat([Edgelist_citytocamp_df, Edgelist_citytocity_df])
#Create two separate csv files with the edgelist of campground to city and city to city(use this to run Network analyst distance between locations twice separately)
Edgelist_citytocamp_df.to_csv('Coding/Camping_data/Edgelist_citytocamp.csv')
Edgelist_citytocity_df.to_csv('Coding/Camping_data/Edgelist_citytocity.csv')

Edgelist_df.to_csv('Coding/Camping_data/Edgelist_nodistance.csv')