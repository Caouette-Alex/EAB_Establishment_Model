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
import seaborn as sns
###
# Change the directory so that we are working out of EAB_Model
###

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model')

###
#Run through a loop to get all the files into a dictionary of dataframes
###

d={}
prop_mean= pd.DataFrame()
prop_std= pd.DataFrame()
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
    prop_mean[name] = (df['mean']/238)*100
    prop_std[name] = df['std']

prop_mean_df = prop_mean.stack().reset_index()
prop_mean_df.columns = ['year','establishment_threshold','proportion_established']
prop_mean_wide = prop_mean_df.pivot('year','establishment_threshold','proportion_established')

#stack files to convert from a matrix to a longform data file
prop_std_df = prop_std.stack().reset_index()
prop_std_df.columns = ['year','establishment_threshold','proportion_established_std']


prop_mean_df = pd.merge(prop_mean_df,prop_std_df,  how='left', left_on=['year','establishment_threshold'], right_on = ['year','establishment_threshold'])
prop_mean_df['std_lower'], prop_mean_df['std_upper'] = prop_mean_df['proportion_established']-prop_mean_df['proportion_established_std'],prop_mean_df['proportion_established']+prop_mean_df['proportion_established_std']
#%%Create figure for the proportion of locations with EAB established over time #MATPLOTLIB#

###
#Create figure of the proportion of campgrounds with EAB establishments Using Matplotlib
###
    
ax = plt.subplot(111)

# run a loop adding a colour for each establishment threshold of wood bundles
for k,v in d.items():
    #ax.bar(v.index, v['mean_prop'], label = k )
    ax.plot(v.index, v['mean_prop'], label = k)
#plt.legend(ncol=1,fontsize=1, bbox_to_anchor=(1.08,1),title='Establishment threshold (pieces wood)')
ax.set_xlim([0, 50.5])
#create a legend
legend = ax.legend(loc=4, ncol=4,fontsize = 'xx-small',fancybox=True,shadow=False,
                   title='Establishment threshold (inf. pieces/year)')#bbox_to_anchor=( 1.08, 1)
#set the legend title fontsize
plt.setp(legend.get_title(),fontsize='xx-small')
plt.xlabel('Years')
plt.ylabel('Locations with established populations of EAB(%)')
plt.savefig('Model_results/Proportion_of_EAB_establishment_year.png', dpi=300)
plt.show()
#%%Create figure for the proportion of locations with EAB established over time #SEABORN#

###
#Create figure of the proportion of campgrounds with EAB establishments using SeaBorn
###

sns.set_theme()

prop_mean_short = prop_mean_df[prop_mean_df['establishment_threshold'].isin(['1','5','10','15','20'])] 

ax = sns.lineplot(data=prop_mean_short, x ='year', y= 'proportion_established', hue = 'establishment_threshold',palette="Spectral", )
ax.legend(title = 'Establishment threshold (# inf. pieces/year)',title_fontsize= 'xx-small',loc= 4,ncol = 5, fontsize = 'xx-small' )
#ax.fill_between(prop_mean_df.index, prop_mean_df.std_upper, prop_mean_df.std_lower)
ax.set_ylabel('Locations with established population of EAB(%)')
ax.set_xlabel('Year')
ax.heatmap(prop_mean_short)

plt.savefig('Model_results/Proportion_of_EAB_establishment_year_seaborn.png', dpi=300)

plt.show()
#%%Proportion of locations with EAB establishment based on the establishment threshold @ 10 years #SEABORN#

###
#Create figure of the proportion of locations with established populations of emerald ash borer based on the
#establishment threshold of number of bundles of infested firewood needed before emerald ash borer establishes in a location
###

sns.set_theme()
prop_mean_10 = prop_mean_df[prop_mean_df['year'] == 10]

ax = sns.barplot(data=prop_mean_10, x ='establishment_threshold', y= 'proportion_established',color='c')
ax.set_ylabel('Locations with established pop. of EAB (%)')
ax.set_xlabel('Establishment threshold (inf. pieces/year)')
ax.set_yticks([0, 20, 40, 60,80 , 100-1], labels=[0,20,40,60,80,100])
ax.set_xticks([1-1,5-1,10-1,15-1,20-1], labels=[1,5,10,15,20])
ax.errorbar(prop_mean_10['establishment_threshold'],prop_mean_10['proportion_established'], yerr=prop_mean_10['proportion_established_std'], fmt='none', elinewidth=0.5,color = 'grey')

plt.savefig('Model_results/Proportion_of_EAB_establishment_at_10_years_seaborn.png', dpi=300)
#ax2 = sns.lineplot(data=prop_mean_10, x ='establishment_threshold', y= 'proportion_established')
#%%Proportion of locations with EAB establishment based on the establishment threshold @ 10 years #MATPLOTLIB#
###
#Create figure of the proportion of locations with established populations of emerald ash borer based on the
#establishment threshold of number of bundles of infested firewood needed before emerald ash borer establishes in a location
###

ax = plt.subplot(111)
plt.title('10 years establishment probability based on number of transported wood',size=8)
for k,v in d.items():
    ax.bar(k, v['mean_prop'][10], label = k)#,color = 'c')
#ax.legend(ncol=1,fontsize=4, loc = 1)
plt.xlabel('Establishment threshold (inf. pieces/year)')
plt.ylabel('Locations with established population of EAB(%)',size= 8)
plt.savefig('Model_results/Proportion_of_EAB_establishment_at_10_years.png', dpi=300)
plt.show()

#%%Violin plot #SEABORN

###
#Create a figure of violin plots that shows the mean establishment probability at 10 years
###
cities = ['Antigonish', 'Amherst', 'Bathurst', 'Campbellton', 'Bridgewater', 'Cape Breton - Sydney', 'Charlottetown',
          'Chatham - Douglastown', 'Enfield - Lantz', 'Edmundston', 'Fredericton', 'Glace Bay', 'Halifax', 'Kentville',
          'Kingston - Greenwood', 'Moncton', 'New Glasgow', 'New Waterford', 'Oromocto', 'Quispamsis - Rothesay',
          'Saint John','Shediac' , 'Summerside', 'Sydney Mines', 'Sussex', 'Truro', 'Windsor', 'Yarmouth','1e-14']
l=[]
prob_mean = pd.DataFrame()
df_test = pd.DataFrame()
d2={}
# The range starts at one and uses the n+1 number of files that you have. 
for i in range(1,21):
    #the name of each df is the establishment threshold or the number of wood bundles required before population establishes
    name = str(i)
    #read the excel file 
    exc_doc = pd.ExcelFile('Model_results/Sim_2022-06-08_1000[5, 10]invas_bundle_'+ name +'.xls')
    #select only the sheet that has the proportion of established locations
    df2 = pd.read_excel(exc_doc,'10invas_prob',index_col=0)
    #Describe the data including showing the mean, count of locations for each, etc.
    df2 = df2.transpose().describe().transpose()
    #create a column in the dataframe that is the proportion of campgrounds that with EAB establishements
    #Create a dictionary of dataframes
    d2[name]= df2
    prob_mean[name] = df2['mean'] 
    l.append(df2['mean'])
prob_mean  = prob_mean.drop(cities) 
test = prob_mean.stack().reset_index()
test.columns = ['campground', 'establishment_threshold', 'establishment_probability']
            

df_mean = pd.DataFrame(l).transpose()
#%%
sns.set_theme()

ax = sns.violinplot( x=test['establishment_threshold'],y= test['establishment_probability'] ,scale = 'width')


ax.set(ylim=(0, 1),xlabel='establishment threshold(inf. pieces/year)', ylabel='Probability of infestation(%)', aspect = 4*3)
#sns.set(rc={'figure.figsize':(30,10)})
#ax = plt.subplot(111)

#ax.violinplot(df_mean_2)
#plt.xticks(np.arange(1,14,1))

plt.savefig('Model_results/violin_plot_probability_of_being_infested.png',dpi=300)


plt.show()