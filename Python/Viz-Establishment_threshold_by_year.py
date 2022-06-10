# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 10:21:59 2022

@author: alexp

This file is meant to plot the mean probability of infestation of a location based on the establishment threshold(number of bundles of infested firewood transported before establishment) 

"""

###
#Import packages
###

import pandas as pd
import os
from matplotlib import pyplot as plt

###
# Change the directory so that we are working out of EAB_Model
###

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model')

###
#Run through a loop to get all the files into a dictionary of dataframes
###

d={}
# The range starts at one and uses the n+1 number of files that you have. 
for i in range(1,22):
    #the name of each df is the establishment threshold or the number of wood bundles required before population establishes
    name = str(i)
    #read the excel file 
    exc_doc = pd.ExcelFile('Model_results/Sim_2022-06-09_100[50]invas_bundle_'+ name +'.xls')
    #select only the sheet that has the proportion of established locations
    df = pd.read_excel(exc_doc,'50prop_infect',index_col=0)
    #Describe the data including showing the mean, count of locations for each, etc.
    df= df.transpose().describe().transpose()
    #create a column in the dataframe that is the proportion of campgrounds that with EAB establishements
    df['mean_prop'] = (df['mean']/238)*100
    # Create a dictionary of dataframes
    d[name]= df

###
#Create figure of the proportion of campgrounds with EAB establishments
###
    
ax = plt.subplot(111)

# run a loop adding a colour for each establishment threshold of wood bundles
for k,v in d.items():
    ax.bar(v.index, v['mean_prop'], label = k )
#plt.legend(ncol=1,fontsize=1, bbox_to_anchor=(1.08,1),title='Establishment threshold (pieces wood)')
ax.set_xlim([0, 50.5])
#create a legend
legend = ax.legend(loc=0, ncol=1,fontsize = 'xx-small', bbox_to_anchor=( 1.08, 1),fancybox=True,shadow=False,
                   title='Establishment threshold (pieces wood)')
#set the legend title fontsize
plt.setp(legend.get_title(),fontsize='xx-small')
plt.xlabel('Years')
plt.ylabel('Proportion of locations with established populations of EAB ')
#plt.savefig('Model_results/Probability_of EAB_establishment_year.png', dpi=300)
plt.show()

###
#Create figure of the proportion of locations with established populations of emerald ash borer based on the
#establishment threshold of number of bundles of infested firewood needed before emerald ash borer establishes in a location
###

ax = plt.subplot(111)
plt.title('10 years establishment probability based on number of transported wood',size=8)
for k,v in d.items():
    ax.bar(k, v['mean_prop'][10], label = k)#,color = 'c')
#ax.legend(ncol=1,fontsize=4, loc = 1)
plt.xlabel('Establishment threshold (bundles infested firewood)')
plt.ylabel('Proportion of locations with established population of EAB',size= 8)
plt.show()

#%%Violin plot

###
#Create a figure of violin plots that shows the mean establishment probability at 10 years
###
l=[]
df_mean_2 = pd.DataFrame()
d2={}
# The range starts at one and uses the n+1 number of files that you have. 
for i in range(1,13):
    #the name of each df is the establishment threshold or the number of wood bundles required before population establishes
    name = str(i)
    #read the excel file 
    exc_doc = pd.ExcelFile('Model_results/Sim_2022-06-08_1000[5, 10]invas_bundle_'+ name +'.xls')
    #select only the sheet that has the proportion of established locations
    df2 = pd.read_excel(exc_doc,'10invas_prob',index_col=0)
    #Describe the data including showing the mean, count of locations for each, etc.
    df2 = df2.transpose().describe().transpose()
    #create a column in the dataframe that is the proportion of campgrounds that with EAB establishements
    df2 = df2.drop(['1e-14']) 
    # Create a dictionary of dataframes
    d2[name]= df2
    df_mean_2[name] = df2['mean'] 
    l.append(df2['mean'])
df_mean = pd.DataFrame(l).transpose()

#%%

ax = plt.subplot(111)
ax.violinplot(df_mean_2)




plt.show()