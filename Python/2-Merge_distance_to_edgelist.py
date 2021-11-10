# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 17:41:20 2021

@author: alexp
"""

import pandas as pd

dist_df=pd.read_csv('Arcmap/Distance_calc/Distance_camp_city.csv')
dist_df= dist_df[['Name','Total_Leng']]

camp_df=pd.read_csv('Coding/Camping_data/edgelist.csv')

camp_df = camp_df.rename(columns={'Unnamed: 0':'ID'})

pd.concat(dist_df, on='Name')
