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
Dest_mrtm_df = df.copy()
Dest_mrtm_df = Dest_mrtm_df[Dest_mrtm_df['mddplfl'].str.match('New Brunswick|Nova Scotia|Prince Edward Island')]

#Create a copy of the main datasheet but only include the Maritime province origins
Orig_mrtm_df = df.copy()
Orig_mrtm_df = Orig_mrtm_df[Orig_mrtm_df['orcprovt'].str.match('New Brunswick|Nova Scotia|Prince Edward Island')]


#%%TRSC Destination data manipulation

#Change the province name to the code system to match provinces name
Dest_mrtm_df['mddplfl'] = Dest_mrtm_df['mddplfl'].replace({'Prince Edward Island':'11','Nova Scotia':'12', 'New Brunswick':'13'})

#Remove NaN values and make all values two numbers long
Dest_mrtm_df = Dest_mrtm_df[Dest_mrtm_df['mdccd'].notna()].astype(str).replace('\.0', '', regex=True)
Dest_mrtm_df['mdccd'] = Dest_mrtm_df['mdccd'].apply(lambda x: '{0:0>2}'.format(x))


print(Dest_mrtm_df.dtypes.head(15))
#Create a new column with a code value including the province and census division
Dest_mrtm_df['Code'] = Dest_mrtm_df['mddplfl'].astype(str) + Dest_mrtm_df['mdccd'].astype(str)
Dest_mrtm_df['Code'] = Dest_mrtm_df['Code'].astype(str).replace('\.0', '', regex=True)
#keep only trips that use a car or a truck or a camper or RV
Dest_mrtm_df= Dest_mrtm_df[Dest_mrtm_df['tmdtype2'].isin(['Car or truck','Camper or RV'])]
#Keep only columns that contain the trip month, ID, Type(overnight or sameday)
Dest_mrtm_df= Dest_mrtm_df[['refmonth', 'tripid', 'triptype', 'mddplfl', 'mdccd','Code','mdccma2','tmdtype2']]

#%%
Orig_mrtm_df['orcprovt'] = Orig_mrtm_df['orcprovt'].replace({'Prince Edward Island':'11','Nova Scotia':'12', 'New Brunswick':'13'})

#Remove NaN values and make all values two numbers long
Orig_mrtm_df = Orig_mrtm_df[Orig_mrtm_df['orccdt2'].notna()].astype(str).replace('\.0', '', regex=True)
Orig_mrtm_df['orccdt2'] = Orig_mrtm_df['orccdt2'].apply(lambda x: '{0:0>2}'.format(x))

Orig_mrtm_df['Code'] = Orig_mrtm_df['orcprovt'].astype(str) + Orig_mrtm_df['orccdt2'].astype(str)
Orig_mrtm_df['Code'] = Orig_mrtm_df['Code'].astype(str).replace('\.0', '', regex=True)
#keep only trips that use a car or a truck or a camper or RV
Orig_mrtm_df= Orig_mrtm_df[Orig_mrtm_df['tmdtype2'].isin(['Car or truck','Camper or RV'])]
#Keep only columns that contain the trip month, ID, Type(overnight or sameday)
Orig_mrtm_df= Orig_mrtm_df[['refmonth', 'tripid', 'triptype', 'orcprovt', 'orccdt2','Code','mdccma2','tmdtype2']]
#%%Create a dataframe of the census divsion with matching column codes to TRSC destination
Cen_div_df= pd.read_csv('Data_Collection/SGC-CGT-2016-Structure-eng.csv')
#change the column name to Census division
Cen_div_df = Cen_div_df[Cen_div_df['Hierarchical structure'] == 'Census division']

#Match the formatting for the code and add a name for the county and province
Cen_div_df['Code'] = Cen_div_df['Code'].astype(str)
Cen_div_df['prov'] = Cen_div_df['Code'].str[0:2]
Cen_div_df['Census_division'] =Cen_div_df['Code'].str[2:4]
Mrtm_div_df= Cen_div_df[Cen_div_df['Code'].astype(str).str[:2].isin(['11','12','13'])]
Mrtm_div_df['prov'] = Mrtm_div_df['prov'].replace(['11','12','13'], ['PEI','NS', 'NB'])
Mrtm_div_df['Class title'] = (Mrtm_div_df['Class title'] +","+ Mrtm_div_df['prov'])

#Mrtm_div_df = Mrtm_div_df['Code'].astype(str)
#%%Merge data from TRSC destinations and census divisions
Dest_merg_df = Dest_mrtm_df.merge(Mrtm_div_df.explode('Code'), on = 'Code', how = 'left')
Orig_merg_df = Orig_mrtm_df.merge(Mrtm_div_df.explode('Code'), on = 'Code', how = 'left')

d={'Destination': Dest_merg_df,'Origin': Orig_merg_df}
print(Mrtm_div_df.explode('Code'))
Dest_merg_df.to_csv('Destination_TSRC')
Orig_merg_df.to_csv('Origin_TSRC')

#%%
import matplotlib.pyplot as plt
import numpy as np
for k,v in d.items():
    data = v['Class title'].value_counts()
    print(data)
    Plot_df = pd.DataFrame(data,)

    filename = k + '_' + 'TSRC_counts.csv'
    Plot_df.to_csv(filename)
    flat_list = []
    for sublist in Plot_df.values:
        for item in sublist:
            flat_list.append(item)
    objects = data.index
    y_pos = np.arange(len(objects))
    print(Plot_df.values)
    plt.bar(y_pos, height = flat_list)
    plt.rcParams['figure.dpi'] = 600
    plt.xticks(y_pos, objects, size=5,rotation=90)
    plt.ylabel('Trips')
    plt.title(k+' '+'Trips to Counties in the Maritimes 2017')

   



    plt.show()
