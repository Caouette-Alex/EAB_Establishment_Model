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
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/data_collection')

d={}
for filename in os.listdir('RAW_TSRC_DATA'):
    csv_file = "RAW_TSRC_DATA/" + filename
    #Read the full TSRC data set from all years
    print(csv_file)
    df = pd.read_csv(csv_file)
     

    #print(df.dtypes.head(15))
    #Create a copy of the main datasheet but only include Maritime province destinations in the maritimes
    mrtm_df = df.copy().astype({'mddplfl': str, 'orcprovt': str})
    mrtm_df = mrtm_df.rename(columns = {'orccdt':'orccdt2', 'tripnum':'tripid'})
    mrtm_df = mrtm_df[(mrtm_df['mddplfl'].str.match('11|12|13') & mrtm_df['orcprovt'].str.match('11|12|13'))]
    

    #TRSC Destination data manipulation

    #Change the province name to the code system to match provinces name
    #cols = ['mddplfl','orcprovt']
    #mrtm_df[cols] = mrtm_df[cols].replace({'Prince Edward Island':'11','Nova Scotia':'12', 'New Brunswick':'13'})

    #Remove NaN values and make all values two numbers long
    mrtm_df = mrtm_df[mrtm_df.mdccd != (0)]
    mrtm_df = mrtm_df[mrtm_df.mdccd != (999)]
    #mrtm_df = mrtm_df[mrtm_df['mdccd'].notna()].astype(str).replace('\.0', '', regex=True)
    mrtm_df['mdccd'] = mrtm_df['mdccd'].astype(str).str.zfill(2)
    
    

    mrtm_df = mrtm_df[mrtm_df.orccdt2 != (0)]
    mrtm_df = mrtm_df[mrtm_df.orccdt2 != (999)]
    mrtm_df['orccdt2'] = mrtm_df['orccdt2'].astype(str).str.zfill(2)


    #Create a new column with a code value including the province and census division
    mrtm_df['dest_code'] = mrtm_df['mddplfl'].astype(str) + mrtm_df['mdccd'].astype(str)
    mrtm_df['dest_code'] = mrtm_df['dest_code'].astype(str).replace('\.0', '', regex=True)
    
   

    mrtm_df['orig_code'] = mrtm_df['orcprovt'].astype(str) + mrtm_df['orccdt2'].astype(str)
    mrtm_df['orig_code'] = mrtm_df['orig_code'].astype(str).replace('\.0', '', regex=True)
    

    #keep only trips that use a car or a truck or a camper or RV
    print(mrtm_df.tmdtype2.unique())
    mrtm_df= mrtm_df.loc[mrtm_df['tmdtype2'].isin([1,3])]
    
   
    
    #Keep only columns that contain the trip month, ID, Type(overnight or sameday)
    mrtm_df= mrtm_df[['refmonth', 'tripid','orcprovt','orccdt2','orig_code', 'mddplfl', 'mdccd','dest_code','mdccma2','tmdtype2']]

    # Calcualte unique values from the grouped locations
    travel = mrtm_df.groupby(['orig_code','dest_code']).size()
    travel_df = pd.DataFrame(travel)
    travel_df = travel_df.rename(columns = {0:'count'}) 
    travel_df = travel_df.reset_index()
    travel_df['join_code'] = travel_df['orig_code'].astype(str) + '_' + travel_df['dest_code'].astype(str)
    name = str(filename)+'_count_data.csv'
    travel_df.to_csv(name)
    d[filename]=travel_df
#%%
d = { k: v.set_index('join_code') for k, v in d.items()}

df = pd.concat(d,axis = 1)
df.columns = df.columns.droplevel(-1)
#%%
df = df.iloc[:, 2::3]
#%%
df = df.fillna(0)

df['sum'] = (df.sum(axis=1))/11

    
#total_trips = travel_df['count'].count()

#travel_df['trip_norm'] = travel_df['count']/total_trips

#travel_df.to_csv('Coding/TSRC/TSRC_values.csv')