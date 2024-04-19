# -*- coding: utf-8 -*-
"""
Created on Fri May 20 10:45:42 2022

@author: alexp

This code is meant to find the correlation and model the relationship between the population size of a location based on the population size. 

To do this, We upload data from Arcmap using the Tourism, Heritage, and Culture of New Brunswick campground reservation data, we then seperate the locations by year

For each year from 2015-2020 we join it to the shapefile of population centres from the gov of canada(https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/bound-limit-2016-eng.cfm) getting a count of the number of reservatiosn made for each campground in the area

We then import all these files into and using a loop add all the files to separate dataframes

I then get the mean number of reservations/year based on the population of the population centre

Calculate the pearsons correlation between population and the number of reservations made to a campground

Using this measurement we found a correlation of -.840 and calculated the linear regresssion of the relationship. 



"""

import pandas as pd
import os
from matplotlib import pyplot as plt
from decimal import Decimal
import statsmodels.api as sm

os.chdir('\..')
os.chdir('Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model')

plt.rcParams['figure.dpi'] = 300

###
# Get the dataframe set up  
###

list = [2015, 2016, 2017, 2018, 2019, 2020]

city_df = pd.read_csv('Coding/Camping_data/Cities_Master_2021-12-07.csv').sort_values(by='Geographic_Name').reset_index()

l=[]

#Loop through the files to read the excel files and merge them so that there was population data added to it then add them to the list l

for year in list:
    name = 'df_'+ str(year)
    file = 'Arcmap/Camping_reservations/' + str(year) +'_pop_cent_reserv.xls'
    pd_file = pd.read_excel(file)
    merge_df = pd.merge(city_df, pd_file,left_on='Geographic_Name',right_on=('PCNAME'))
    merge_df = merge_df[merge_df['Province'] == 'NB']#Arcmap.set_index('PCNAME')      
    l.append(merge_df)


#add together all the dataframes from all the years and get the mean number of reservations for each city
df = pd.concat(l).groupby(level=0).mean()

#Get the number mean number of reservations per campground per year 
df['per_camp_reserv'] = (df['Count_']/9)

#plot as a scatterplot the number of reservation per year 
df.plot('Population', 'per_camp_reserv', kind='scatter')
plt.xlabel('Population size', fontsize=12)
plt.ylabel('Campground reservations/year', fontsize=12)


###
# Measure the pearson correlation coefficient between the population and the number of reservations made to a single campground
###

x = df['Population']
y = df['per_camp_reserv']

#measure the correlation
from scipy.stats import pearsonr
corr, p_value = pearsonr(x,y)
print('Pearsons correlation: %.3f' % corr)
print('p-value:', p_value)
###
# Measure the linear regression of the relationship between the number of reservations made to a single campground
###

from sklearn.linear_model import LinearRegression

#Convert these values into a numpy matrix 
x = df[['Population']].to_numpy()
y = df[['per_camp_reserv']].to_numpy()


# Create a model for the linear regression 
model = LinearRegression()
#find the line of best fit
model.fit(x,y)
model = LinearRegression().fit(x,y)

r_sq = model.score(x,y)
print('coefficient of determination:', r_sq)
itrcpt = model.intercept_

slp = model.coef_


print('y=',str(slp)[2:-2],'x+',str(itrcpt)[1:-1])
plt.plot(x, slp*x+itrcpt)

#Find confidence interval lower and upper bounds for the slope and y-intercept
alpha = 0.05 # 95% confidence interval
#Fit a linear model using Generalized Least Squares
lr = sm.OLS(y, sm.add_constant(x)).fit()
conf_interval = lr.conf_int(alpha)

#post the confidence intervals.
print('                          Confidence intervals \n ================================================================== \n                Slope                               Y-intercept',
      '\n Lower bound:',conf_interval[1][0],'          ',conf_interval[0][0],
      '\n Upper bound:',conf_interval[1][1],'           ', conf_interval[0][1])



#Create scatterplot in Seaborn

import seaborn as sns

custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style = 'ticks', rc=custom_params)


fig = plt.figure()
ax = sns.regplot(data=df, x=x, y=y ,ci=None, scatter_kws={"color": "black"}, line_kws={"color": "dimgray"})
ax.plot(x, x*conf_interval[1][1] + conf_interval[0][1], linestyle = '--',c='black')
ax.plot(x, x*conf_interval[1][0] + conf_interval[0][0], linestyle = '--',c='black',label='_nolegend_')


x = df['Population']
y = df['per_camp_reserv']

slp = '%.1E' % Decimal(round(slp.item(),4))
itrcpt = round(itrcpt.item(),1)

equ = ('y= ' + str(slp) + 'x + ' + str(itrcpt))
#plt.legend()
plt.text(86000,200,(equ))

#ax.plot(x, slp*x+itrcpt)


ax.set_xlabel("Population size")
ax.set_ylabel("Campground reservations/year")

plt.savefig('Model_results/Campground_res_pop_size.png',dpi = 300)

