# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 14:19:07 2021

@author: alexp

This document is meant to read the Travel Survey for the Residents of Canada(TSRC) data set from 2017 from statistics Canada. 
It can be found in the microdata files from the statistics Canada website, and the file must be read using SPSS and transferred before it can be used.

The input is a document showing origin and destination of trips made by people including the method of travel and the census division(county) that the person left from and arriced to 
The outputs of the file:
    -A document with only travel destinations in the Martiimes and those that were completed using either a car or truck, or a camper or RV(Dest_mrtm_df).
    -A frequency histogram of the frequency of trips done to each county during that time
    -
    
"""

import pandas as pd

import os

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model')

#Read the full TSRC data set from 2017
df = pd.read_spss('Data_collection/TRSC_2017.sav')


#print(df.dtypes.head(15))
#Create a copy of the main datasheet but only include Maritime province destinations in the maritimes
mrtm_df = df.copy()
mrtm_df = mrtm_df[(mrtm_df['mddplfl'].str.match('New Brunswick|Nova Scotia|Prince Edward Island') & mrtm_df['orcprovt'].str.match('New Brunswick|Nova Scotia|Prince Edward Island'))]



#%%TRSC Destination data manipulation

#Change the province name to the code system to match provinces name
cols = ['mddplfl','orcprovt']
mrtm_df[cols] = mrtm_df[cols].replace({'Prince Edward Island':'11','Nova Scotia':'12', 'New Brunswick':'13'})

#Remove NaN values and make all values two numbers long
mrtm_df = mrtm_df[mrtm_df['mdccd'].notna()].astype(str).replace('\.0', '', regex=True)
mrtm_df['mdccd'] = mrtm_df['mdccd'].apply(lambda x: '{0:0>2}'.format(x))

mrtm_df = mrtm_df[mrtm_df['orccdt2'].notna()].astype(str).replace('\.0', '', regex=True)
mrtm_df['orccdt2'] = mrtm_df['orccdt2'].apply(lambda x: '{0:0>2}'.format(x))



print(mrtm_df.dtypes.head(15))
#Create a new column with a code value including the province and census division
mrtm_df['dest_code'] = mrtm_df['mddplfl'].astype(str) + mrtm_df['mdccd'].astype(str)
mrtm_df['dest_code'] = mrtm_df['dest_code'].astype(str).replace('\.0', '', regex=True)

mrtm_df['orig_code'] = mrtm_df['orcprovt'].astype(str) + mrtm_df['orccdt2'].astype(str)
mrtm_df['orig_code'] = mrtm_df['orig_code'].astype(str).replace('\.0', '', regex=True)
#keep only trips that use a car or a truck or a camper or RV
print(mrtm_df.tmdtype2.unique())
mrtm_df= mrtm_df[mrtm_df['tmdtype2'].isin(['Car or truck','Camper or RV'])]
#Keep only columns that contain the trip month, ID, Type(overnight or sameday)
mrtm_df= mrtm_df[['refmonth', 'tripid', 'triptype','orcprovt','orccdt2','orig_code', 'mddplfl', 'mdccd','dest_code','mdccma2','tmdtype2']]

#%% Calcualte unique values from the grouped locations
travel = mrtm_df.groupby(['orig_code','dest_code']).size()
travel_df = pd.DataFrame(travel)
travel_df = travel_df.rename(columns = {0:'count'}) 
total_trips = travel_df['count'].count()
travel_df['trip_norm'] = travel_df['count']/total_trips

travel_df.to_csv('Coding/TSRC/TSRC_values.csv')