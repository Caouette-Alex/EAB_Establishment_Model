# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 16:27:12 2022

@author: alexp
"""

import pandas as pd

import os

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Testing travel data')

pop_cen = pd.read_excel('Pop_ctr_det_census_div.xls').reset_index()

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model')

Trav_df = pd.read_csv('Coding/TSRC/TSRC_values_ON_QC.csv')

