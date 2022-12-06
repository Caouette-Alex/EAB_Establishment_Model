# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 19:37:35 2022

@author: alexp
"""
import os
import pandas as pd
import numpy as np

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model')

Prov_camp = {'New River Beach':[45.136835, -66.529251],'Mactaquac':[45.954424, -66.889190],
             'Mount Carleton':[47.429853, -66.947429],'Murray Beach':[46.177457, -63.978940],
             'The Anchorage':[44.660932, -66.805999],'Parlee Beach':[46.229522, -64.504533],
             'Sugarloaf':[47.982447, -66.692120],'République':[47.440343, -68.395702],
             'Herring Cove':[44.877552, -66.934288]}



#import campground reservation dataset
camp_res = pd.read_csv('Arcmap/Camping_reservations/NB_campground_reservations.csv')


camp_res.replace(r'^\s*$', np.nan, regex = True, inplace = True)
camp_res = camp_res.dropna(subset = 'PRUID')
print(camp_res['PRUID'].isna().sum())



camp_res = camp_res[camp_res.PRUID != '10']
camp_res = camp_res[camp_res.Park != 'Nepisiguit Migmaq Trail']
print(camp_res['Park'].unique())

camp_res['Latitude'] = camp_res.Park.map(lambda x: Prov_camp[x][0])
camp_res['Longitude'] = camp_res.Park.map(lambda x: Prov_camp[x][1])

camp_res.to_csv('Arcmap/camping_number_reservations/camp_res_cords.csv')

camp_dict = {}
for year, df_year in camp_res.groupby('Year_'):
    camp_dict[year] = df_year
    
for k,v in camp_dict.items():
    name = 'Arcmap/Camping_number_reservations/'+str(k)+'camp_res_cords.csv'
    print(name)
    v.to_csv(name)
