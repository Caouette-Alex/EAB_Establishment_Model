# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 14:19:07 2021

@author: alexp
"""

import pandas as pd

import os

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies')

df = pd.read_spss('EAB_Model/Data_Collection/TRSC_2017.sav')


print(df.dtypes.head(15))

Dest_mrtm_df = df.copy()

#Orig_mrtm_df = df[df['orcprovt'].isin(['New Brunswick', 'Nova Scotia', 'Prince Edward Island'])]
#Dest_mrtm_df['mddplfl'] =Dest_mrtm_df.loc[Dest_mrtm_df['mddplfl'].isin(['New Brunswick', 'Nova Scotia', 'Prince Edward Island'])]
Dest_mrtm_df= Dest_mrtm_df[Dest_mrtm_df['mddplfl'].str.match('New Brunswick|Nova Scotia|Prince Edward Island')]




#Mrtm_df= df[df['orcprovt'].isin(['New Brunswick', 'Nova Scotia', 'Prince Edward Island'])]

#%%

Dest_mrtm_df['mddplfl'] = Dest_mrtm_df['mddplfl'].replace({'Prince Edward Island':'11','Nova Scotia':'12', 'New Brunswick':'13'})

Dest_mrtm_df = Dest_mrtm_df[Dest_mrtm_df['mdccd'].notna()].astype(str).replace('\.0', '', regex=True)
Dest_mrtm_df['mdccd'] = Dest_mrtm_df['mdccd'].apply(lambda x: '{0:0>2}'.format(x))

#Dest_mrtm_df['mdccd'] = Dest_mrtm_df['mdccd'].astype(str).str.zfill(2)


print(Dest_mrtm_df.dtypes.head(15))
Dest_mrtm_df['Code'] = Dest_mrtm_df['mddplfl'].astype(str) + Dest_mrtm_df['mdccd'].astype(str)
Dest_mrtm_df['Code'] = Dest_mrtm_df['Code'].astype(str).replace('\.0', '', regex=True)


Dest_mrtm_df= Dest_mrtm_df[['refmonth', 'tripid', 'triptype', 'mddplfl', 'mdccd','Code','mdccma2','tmdtype2']]

#%%
Cen_div_df= pd.read_csv('EAB_Model/Data_Collection/SGC-CGT-2016-Structure-eng.csv')

Cen_div_df = Cen_div_df[Cen_div_df['Hierarchical structure'] == 'Census division']

Cen_div_df['Code'] = Cen_div_df['Code'].astype(str)
Cen_div_df['prov'] = Cen_div_df['Code'].str[0:2]
Cen_div_df['Census_division'] =Cen_div_df['Code'].str[2:4]
Mrtm_div_df= Cen_div_df[Cen_div_df['Code'].astype(str).str[:2].isin(['11','12','13'])]
Mrtm_div_df['prov'] = Mrtm_div_df['prov'].replace(['11','12','13'], ['PEI','NS', 'NB'])
Mrtm_div_df['Class title'] = (Mrtm_div_df['Class title'] +","+ Mrtm_div_df['prov'])
#Mrtm_div_df = Mrtm_div_df['Code'].astype(str)
#%%
Merge_df = Dest_mrtm_df.merge(Mrtm_div_df.explode('Code'), on = 'Code', how = 'left')
print(Mrtm_div_df.explode('Code'))

#%%
import matplotlib.pyplot as plt
import numpy as np
Plot_df = Merge_df['Class title'].value_counts()

print(Plot_df.values)

objects = Plot_df.index
y_pos = np.arange(len(objects))
plt.bar(y_pos, Plot_df.values)
plt.xticks(y_pos, objects, size=5,rotation=90)
plt.ylabel('Trips')
plt.title('Trips to Counties in the Maritimes 2017')

plt.rcParams['figure.dpi'] = 300



plt.show()
