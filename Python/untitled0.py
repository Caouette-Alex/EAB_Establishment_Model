# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 19:37:35 2022

@author: alexp
"""
import os
import pandas as pd


os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model')

#import campground reservation dataset
camp_res_month = pd.read_csv('Arcmap/Camping_reservations/NB_campground_reservations.csv')

camp_dict = {}
for year, df_year in camp_res_month.groupby('Year_'):
    camp_dict[year] = df_year
