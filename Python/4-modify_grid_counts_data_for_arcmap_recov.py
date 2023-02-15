# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 11:06:02 2022

@author: alexp
"""
import pandas as pd
import os
from datetime import datetime
import seaborn as sns
from matplotlib import pyplot as plt
os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model')

##Create two dataframes that measures the establishment of EAB to different regions NOT influenced by the firewood timing arrival based on varying levels of an establishment threshold
ft_off_grid_2_df,ft_off_grid_6_df  = pd.read_excel("Model_results/Sim_2022-10-25_1000[20]Establishment_fire_off.xls", sheet_name = '2grid_counts', index_col = 0), pd.read_excel("Model_results/Sim_2022-10-25_1000[20]Establishment_fire_off.xls", sheet_name = '6grid_counts', index_col = 0)
#Create two dataframes that measures the establishment of EAB to different regions influenced by the firewood timing arrival based on varying levels of an establishment threshold
ft_on_grid_2_df,ft_on_grid_6_df  = pd.read_excel("Model_results/Sim_2022-10-26_1000[20]Establishment_fire_on.xls", sheet_name = '2grid_counts', index_col = 0), pd.read_excel("Model_results/Sim_2022-10-26_1000[20]Establishment_fire_on.xls", sheet_name = '6grid_counts', index_col = 0)

#Create a dictionary with of all the dataframes
d = {'Low':ft_off_grid_2_df,'High':ft_off_grid_6_df,'FT_Low':ft_on_grid_2_df,'FT_High':ft_on_grid_6_df}

d_2 = {}
#iterate through dictionary of dataframes and convert any value greater than one to binary set 1 or 0 (either hexagon is infested or not)
for k,v in d.items():
    v = v.mask(v > 1, 1)
    n_v = v.drop(columns = 'total_counts')
    #Get mean values across all the simulations 
    d_2[k] = n_v.transpose().fillna(0).describe(include='all').transpose()

#export each dataframe as a separate csv file for import into ArcMap
for k,v in d_2.items():
    path = 'model_results/'+k +'_'+ datetime.today().strftime('%Y-%m-%d')+'.csv'
    v.to_csv(path)
    
# Proportion of locations with EAB infestations
d_3={}
#Iterate to measure the proportion of locations that get established populations of EAB
for k,v in d.items():
    #convert any value greater than one to binary set 1 or 0 (either hexagon is infested or not)
    v = v.mask(v > 1, 1)
    #drop all hexagons that have a value of NA meaning there are no campgrounds there
    v = v[v['total_counts'].notna()]
    #get proportion of hexagons that have EAB establishment 
    d_3[k] = v.fillna(0).describe()


test = pd.DataFrame()
for k,v in d_3.items():
    mean_val = v.drop(columns='total_counts').transpose()
    mean_val = mean_val['mean'].describe()
    name = k
    test[name] = mean_val



test = test.transpose()
#%%
c = sns.color_palette('pastel')[0]
c2 = sns.color_palette('pastel')[1]   
sns.reset_orig()

fig, ax = plt.subplots()

l = []
for word in list(test.index[2:4]):
    a1 = word[3:] 
first = ax.bar([0,2], test['mean'].iloc[:2], color = c, label = 'Ignoring timing of firewood arrival')
second = ax.bar([1,3], test['mean'].iloc[2:4],color = c2, label = 'Considering timing of firewood arrival')

ax.errorbar(x =[0,2,1,3], y = test['mean'], yerr = test['std'],fmt='none',c = 'k')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_xticks([0,2,1,3])
ax.set_xticklabels(['Low','High','Low','High'])
ax.set_ylabel('Mean proportion of established hexagons')
ax.set_xlabel('Establishment threshold')
#plt.set_label('test')
ax.legend([first, second],['Ignoring timing of firewood arrival','Considering timing of firewood arrival'],bbox_to_anchor =(1,1.1)  )
#mean proportion of locations with EAB infestations

plt.savefig('Model_results/Mean_proportion_establishment.png', dpi=300)

#%%
print(test.loc[['Low','FT_Low']])
#print(test.iloc[[0,2],[1]])
fig, ax = plt.subplots(1,2, sharey=True)
#ax[0].bar(['Ignore FTI','Consider FTI'], test['mean'].loc[['Low','FT_Low']], color = c, label = 'Ignoring timing of firewood arrival')
ax[0].bar(['Ignore FTI'], test['mean'].loc[['Low']], color = c, label = 'Ignoring timing of firewood arrival')
ax[0].bar(['Consider FTI'], test['mean'].loc[['FT_Low']], color = c2, label = 'Ignoring timing of firewood arrival')

ax[1].bar(['Ignore FTI'], test['mean'].loc[['High']], color = c, label = 'Ignoring timing of firewood arrival')
ax[1].bar(['Consider FTI'], test['mean'].loc[['FT_High']], color = c2, label = 'Ignoring timing of firewood arrival')

ax[0].errorbar(x =[0,1], y = test['mean'].loc[['Low','FT_Low']], yerr = test['std'].loc[['Low','FT_Low']],fmt='none',c = 'k')
ax[1].errorbar(x =[0,1], y = test['mean'].loc[['High','FT_High']], yerr = test['std'].loc[['High','FT_High']],fmt='none',c = 'k')

ax[0].title.set_text('Low \n Propagule Pressure Threshold')
ax[1].title.set_text('High \n Propagule Pressure Threshold')

ax[0].spines['right'].set_visible(False)
ax[0].spines['top'].set_visible(False)

ax[1].spines['right'].set_visible(False)
ax[1].spines['top'].set_visible(False)

ax[0].set_ylabel('Mean proportion of established hexagons')
#ax[1].spines['left'].set_visible(False)
#ax[1].tick_params(left=False)
plt.savefig('Model_results/Mean_proportion_establishment_split.png', dpi=300)
#%%
d_4 = {}
temp2= {}
for k,v in d.items():
    v = v.mask(v > 1, 1)
    v = v[v['total_counts'].notna()].fillna(0)
    n_v = v.drop(columns = 'total_counts')
    temp = {}
    for k2,v2 in n_v.items():
        temp[k2] = sum(v2)/53
    temp2[k] = temp
df = pd.DataFrame(temp2.values(),temp2.keys()).transpose()
print(df.describe())

import scipy.stats as stats
from scipy.stats import tukey_hsd
# stats f_oneway functions takes the groups as input and returns ANOVA F and p value
fvalue, pvalue = stats.f_oneway(df['Low'], df['High'], df['FT_Low'], df['FT_High'])
print(fvalue, pvalue)


print(tukey_hsd(df['Low'], df['High'], df['FT_Low'], df['FT_High']))

#%%

df_long = pd.melt(df,value_vars = ['Low', 'High', 'FT_Low', 'FT_High'])

df_long['Firewood_timing'] = ''
df_long['Propagule_pressure'] = ''

df_long.loc[df_long['variable'] == 'Low', ['Firewood_timing','Propagule_pressure']] = ['Ignore', 'Low']
df_long.loc[df_long['variable'] == 'High', ['Firewood_timing','Propagule_pressure']] = ['Ignore', 'High']
df_long.loc[df_long['variable'] == 'FT_Low', ['Firewood_timing','Propagule_pressure']] = ['Consider', 'Low']
df_long.loc[df_long['variable'] == 'FT_High', ['Firewood_timing','Propagule_pressure']] = ['Consider', 'High']

import statsmodels.api as sm
from statsmodels.formula.api import ols

#perform two-way ANOVA
model = ols('value ~ C(Firewood_timing) + C(Propagule_pressure) + C(Firewood_timing):C(Propagule_pressure)', data=df_long).fit()
sm.stats.anova_lm(model, typ=2)



#for index, row in df_long.iterrows():
    #if row['variable'] == 'Low':
       #row['Firewood timing'] = 'ignored'
