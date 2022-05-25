# -*- coding: utf-8 -*-
"""
Created on Tue May 24 10:45:34 2022

@author: alexp

This code is to measure the number of reservations made to campgrounds in provincial parks based on the origin city of the campers. 

Using the data from Tourism, Heritage, and Culture New Brunswick, I uploaded the data to Arcmap and added the population centre digital boudary shapefile

I did a spatial join on the reservations to associate them to a population centre then uploaded them into this document

this file contains all the cities in New Brunswick and the reservations made to each campground by camper origin city
"""
#
import pandas as pd
import os
from matplotlib import pyplot as plt

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Arcmap/Camping_reservations/')

#import this CSV from arcmap
df= pd.read_csv('location_based_by_city.csv')
#keep only locations from new brusnwick
df= df[df['PRUID'] == '13']


#Plot the total number of reservations made to campgrounds
df_campground = df.groupby(by=['Park']).size()
df_campground.plot.bar()


#Group the campgrounds based on their city and the provincial park, count the number of instances and 
#remove the rows that didnt have a city
df_grouped = df.groupby(by=['PCNAME','Park']).size().reset_index().rename(columns={0:'reservation'})
df_grouped = df_grouped[df_grouped['PCNAME'].str.strip().astype(bool)]




#%%
#create a bar chart of the number of reservations to provicial park campgrounds based on the origin city of the camper
import seaborn as sns
plt.figure(figsize = (20,10))

ax =sns.barplot(data=df_grouped, x='PCNAME', y='reservation', hue='Park')
#rotate x labels 90 degrees
ax.set_xticklabels(ax.get_xticklabels(),rotation = 90)
