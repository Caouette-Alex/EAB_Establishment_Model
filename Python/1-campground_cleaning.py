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
pd.set_option("display.max_columns", None)

#Import distance table and route table to
Campground_df=pd.read_csv('Parks_and_camping_Master_2021-10-05.csv')

Campground_df.insert(15,'OID', 0)

print(Campground_df)


## Copying and adding 4 new rows to each existing row
Campground_df=Campground_df.append([Campground_df]*4)

#Organize values so that all 4 copied rows are at the same place
Campground_df=Campground_df.sort_values(by=['OID'],ascending=True)

#add 4 new columns 
Campground_df.insert(11,'CODE',0)
Campground_df.insert(12,'Origin',0)
Campground_df.insert(13,'lat',0)
Campground_df.insert(14,'long',0)




#change the type of column OID from float64 to Object(String)
Campground_df = Campground_df.astype({'OID':'object'})
