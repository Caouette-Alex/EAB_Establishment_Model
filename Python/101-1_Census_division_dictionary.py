# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 15:49:35 2022

@author: alexp

Creating the census division code dictionary using the data collected from ArcMap

"""
import os

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model')


import pandas as pd

city_df = pd.read_excel('Arcmap/Distance_calc/Cen_div_city.xls')
city_df = city_df.loc[city_df['Dest_name'] == 'Halifax']
city_df = city_df[['Orig_name','Orig_pop', 'Orig_lat', 'Orig_long', 'CDUID']]


camp_df = pd.read_excel('Arcmap/Distance_calc/Cen_div_camp.xls')
camp_df = camp_df.loc[camp_df['Orig_name'] == 'Halifax']
camp_df = camp_df[['Dest_name','Sites', 'Dest_lat', 'Dest_long', 'CDUID']]

##%-----------------------------
