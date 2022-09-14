# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 16:23:26 2022

@author: alexp

M
"""
import pandas as pd
import os

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model')

camp_res_month = pd.read_csv('Arcmap/Camping_reservations/NB_campground_reservations.csv')


camp_dict = {}
for year, df_year in camp_res_month.groupby('Year_'):
    camp_dict[year] = df_year

month_res_df = {}
for year,df in camp_dict.items():
    month_res_df[year] = df.groupby('Month_').size().reset_index(name='count')


#convert dictionary of dataframes to a single dataframe
d = { k: v.set_index('Month_') for k, v in month_res_df.items()}
df = pd.concat(d, axis= 1)


#
df_short = df
df_short.columns = df_short.columns.droplevel(-1)
df_short['mean'] = df_short.mean(axis=1)
df_short['ste'] = df_short.sem(axis=1,skipna=True)



#
df_long = df.reset_index()
#df_long.columns = df_long.columns.droplevel(-1)
df_long = pd.melt(df_long, id_vars='Month_', value_vars=[2015, 2016, 2017,2018,2019,2020])
df_long=df_long.rename(columns={'variable':'year', 'value':'reservations'})





import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize = (20,10))
ax =sns.barplot(data=df_long,x= 'Month_',y='reservations', hue ='year' )
plt.show()
#rotate x labels 90 degrees
#ax.set_xticklabels(ax.get_xticklabels(),rotation = 90)

ax = sns.barplot(data = df_short, x= df_short.index, y = 'mean')
ax.errorbar(x =[0,1,2,3,4,5], y = df_short['mean'], yerr = df_short['ste'],fmt='none',c = 'k')
ax.
plt.show()