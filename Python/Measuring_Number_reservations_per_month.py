# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 16:23:26 2022

@author: alexp

This file takes the campground reservations dataset from the new brunswick campground reservations from Tourism, heritage, and culture new brusnwick
and measure the mean number of reservations that are made per month from the years of 2015-2020
"""
import pandas as pd
import os

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model')

#import campground reservation dataset
camp_res_month = pd.read_csv('Arcmap/Camping_reservations/NB_campground_reservations.csv')

#group campground reservations into dictionaries of dataframes based on the year that the reservation was made
camp_dict = {}
for year, df_year in camp_res_month.groupby('Year_'):
    camp_dict[year] = df_year

#measure the number of reservations made based on the month that gone camping
month_res_df = {}
for year,df in camp_dict.items():
    month_res_df[year] = df.groupby('Month_').size().reset_index(name='count')


#convert dictionary of dataframes to a single dataframe with the index as a month and the columns representing the number of reservations made that year
d = { k: v.set_index('Month_') for k, v in month_res_df.items()}
df = pd.concat(d, axis= 1)
df= df.rename(index={5:'May',6:'June',7:'July',8:'August', 9:'September',10:'October'})
#df = df.drop(columns=2020)

#Represent the dataframe similar as df but more cleaned up and with mean and standard error
df_short = df
df_short.columns = df_short.columns.droplevel(-1)
df_short['mean'] = df_short.mean(axis=1)
df_short['ste'] = df_short.sem(axis=1,skipna=True)



#Create a dataframe in longview format to represent number of reservations each year 
df_long = df.reset_index()
df_long = pd.melt(df_long, id_vars='Month_', value_vars=[2015, 2016, 2017,2018,2019,2020])
df_long=df_long.rename(columns={'variable':'year', 'value':'reservations'})


import matplotlib.pyplot as plt
import seaborn as sns

#Create a figure that represents teh number of reservations made each month based on the year that the reservation was made
plt.figure(figsize = (20,10))
ax =sns.barplot(data=df_long,x= 'Month_',y='reservations', hue ='year' )
plt.show()



#Create a figure that represents the mean number of reservations  
ax = sns.barplot(data = df_short, x= df_short.index, y = 'mean', color=sns.color_palette('pastel')[0])
ax.errorbar(x =[0,1,2,3,4,5], y = df_short['mean'], yerr = df_short['ste'],fmt='none',c = 'k')
ax.set_ylabel('Mean reservations/year')
ax.set_xlabel('Month')
plt.show()