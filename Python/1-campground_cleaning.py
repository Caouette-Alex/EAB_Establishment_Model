# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 16:05:43 2021

@author: alexp
"""
#### Taking campground data and adding 4 new rows for each campground then cleaning up

##### Edited: April 09, 2021

import os
import pandas as pd

os.chdir('/..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_model/Coding/Camping_data')
os.getcwd()

#Import distance table and route table to
Campground_df = pd.read_csv('Parks_and_camping_Master_2021-10-05.csv')

Campground_df = Campground_df.reset_index().rename({'index':'OID'}, axis = 'columns')

print(Campground_df)


## Copying and adding 4 new rows to each existing row
Campground_df=Campground_df.append([Campground_df]*4)

#Organize values so that all 4 copied rows are at the same place
Campground_df=Campground_df.sort_values(by=['OID'],ascending=True)


Campground_df = Campground_df.loc[:, ~Campground_df.columns.str.contains('^Unnamed')]

Campground_df = Campground_df.drop(columns=['Contacted', 'Responded?','Additional Info Provided from Campground (mostly regarding the origin of campers)'],axis='columns')

list(Campground_df)

#add 4 new columns 
Campground_df.insert(15,'CODE',0)
Campground_df.insert(16,'Origin',0)
Campground_df.insert(17,'lat',0)
Campground_df.insert(18,'long',0)


#Add data to CODE column 
    #Add C + the OID value and  O + an ascending value of 1-5 for each set of campground  
Code=[]
Origin=0
for index,row in Campground_df.iterrows():
    if Origin<5:
        Origin=Origin+1
    else:
        Origin=1
    Code.append('C'+ str(int(row['OID']))+'O'+str(Origin))
Campground_df['CODE']=Code

#change the type of column OID from float64 to Object(String)
#Campground_df = Campground_df.astype({'OID':'object'})

# Create a new column for with only the origin using the last two values of the origin code
Origin_code=Campground_df['CODE'].str[-2:]
Campground_df['Origin_code']=Origin_code

#Insert data into each column by specified Origin codeto add data from Origin location + GPS coordinates 
Origin=[]
Lat=[]
Long=[]
for index,row in Campground_df.iterrows():
    if row['Origin_code'] == 'O1':
        city='Edmunston'
        lat=47.363138271024624
        long=-68.32607675625937
    elif row['Origin_code'] == 'O2':
        city='Bedford'
        lat=44.649481728336255 
        long=-63.575298068542146
    elif row['Origin_code'] == 'O3':
        city='Oromocto'
        lat=45.8412673684528
        long=-66.508238007871
    elif row['Origin_code'] == 'O4':
        city='Moncton'
        lat=46.08971442081271
        long=-64.7753305171323
    elif row['Origin_code'] == 'O5':
        city='Fredericton'
        lat=45.96360737172908
        long=-66.64307843615934
    Origin.append(city)
    Lat.append(lat)
    Long.append(long)
Campground_df['Origin']=Origin
Campground_df['lat']=Lat
Campground_df['long']=Long


#Remove OID and Origin_code columns because no longer necessary
Campground_df=Campground_df.drop(['Origin_code','OID'],axis=1)

#Rename columns to be more readable
Campground_df=Campground_df.rename(columns={'Lat':'C_Lat','Name':'Campground','Long':'C_Long','lat':'O_Lat','long':'O_Long','Tye_of_Cam':'Camp_type','Aquiring_f':'Firewood'})

#export data to Comma seperated value data sheet
Campground_df.to_csv('Parks_and_camping_Cleand_2021-10-05.csv')