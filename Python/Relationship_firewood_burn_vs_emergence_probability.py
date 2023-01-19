# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 11:42:50 2022

@author: alexp
Measuring the sigmoid curve relationship of degree days vs. to emergrance date

"""
import numpy as np
from scipy.optimize import curve_fit
from datetime import date
import pandas as pd
from matplotlib import pyplot as plt

#dictionary representing the flight percentile based on the degree day corrected for the date (Data is from Tobin et al. 2021)
d = {0.1:[2022,7,13], 0.25:[2022,7,20], 0.5:[2022,7,27], 0.75:[2022,8,5], 0.9:[2022,8,16]}
#d = {0.9:[2022,7,13], 0.75:[2022,7,20], 0.5:[2022,7,27], 0.25:[2022,8,5], 0.1:[2022,8,16]}
#convert dates to the Julien date
for k,v in d.items():
    day_of_year = date(v[0], v[1], v[2]).timetuple().tm_yday
    d[k] = day_of_year


#Create a dataframe of dates and percentiles into separate numpy arrays to input into logistic growth curves
df= pd.DataFrame(list(zip(np.array(list(d.values())),np.array(list(d.keys())))), columns= ['x','y'])

#Define the logistic curve equation
def logisticr(x, a, b):
    return 1.0 / (1.0 + np.exp(-(-a*(x-b))))

#Calculate the logistic decay relationship of EAB beetle emergence based on Degree days optimal values to describe the equation (a and b)
popt, pcov = curve_fit(logisticr, df['x'], df['y'], method='dogbox', bounds=([0.1, 200.],[0.9, 240.]))
print('a value =', popt[0], 'b value =', popt[1])

#Create a numerical sequence of values from 135 to 283
x = np.linspace(135, 283, 283-135)
#calulate the Y values based on the calcualted x values and the decriptor values calculated by the curve-fit function
sig_y = logisticr(x, *popt)

#linear regression of the proportion of firewood calculated using an estimated probability of firewood burnt before beetle emergence
lin_y = (-0.009*x+ 2.22)

#Calulate the probability that EAB emerges before fire is burnt by measuring the product of 
arrival_prob_array= (1.0 / (1.0 + np.exp(-(-0.135*(x-208))))) * (1-(-0.009*x+ 2.22))



#####

# Create new figure with a 2 row:1 col setup
fig = plt.figure()
ax = fig.add_subplot(211)

#Plot the data points to show fit of the model
ax.plot(df['x'], df['y'],'o', color = 'royalblue', label='data')
#Plot the proportion of beetles left to emerge(logistic decay function)
ax.plot(x,sig_y,'royalblue' ,label='Proportion of EAB still present in the firewood (A)')
ax.axis(ymin=0, ymax=1.05)
ax.set_ylabel('Proportion/probability')
#ax.grid() 

#Plot the proportion of firewood to be burnt before emerald ash borer emergence
ax.plot(x,lin_y,'-r',label = 'Probability that firewood is burnt before EAB emergence season (B)')
#Create a second y acis with the 
#ax2 = ax.twinx()
#ax2.axis(ymin=0, ymax=1.05)
ax.plot(x,arrival_prob_array, color ='g' , label = 'Probability of EAB emergence from unburned firewood (A*(1-B))')
#ax2.set_ylabel('Probability of EAB emergence Firewood Burnt (B)', fontsize=9)


#Create labels for the legend
lines, labels = ax.get_legend_handles_labels()
#lines2, labels2 = ax2.get_legend_handles_labels()



#Create the second plot on the figure
ax3 = fig.add_subplot(212, sharex = ax)


#Dictionary of the number of days campgrounds are open for during each month
d2 = {'May':17,'Jun':30,'Jul':31,'Aug':31, 'Sept':30,'Oct': 9}

val= 0
val2= -1

#Replot the proportion of firewood to be burnt before emerald ash borer emergence
ax3.plot(x,arrival_prob_array, color ='g' , label = 'A*B')

# 
df3 = pd.DataFrame(arrival_prob_array,columns = ['y'])
df3['x']  = range(135,283)

# For loop that creates  length of each month and the measurement of the mean area under the curve for each value
for k,v in d2.items():
    val2= val2 + (v)
    trap = np.trapz(df3['y'].loc[val:val2],df3['x'].loc[val:val2])/v
    
    #l = [d2[v], trap]
    d2[k] = [v,trap]
    val = val+v
#Insert values into dataframe to make it easier to plot on barchart
df2 = pd.DataFrame(list(d2.values()),index = list(d2.keys()), columns=['width','height'])
#Create color map that changes color for each month
cmap = iter([plt.cm.Set3(i) for i in range(20)])
#define the colors of each month
colors = {'May':next(cmap),'June':next(cmap),'July':next(cmap),'August':next(cmap),'September':next(cmap),'October':next(cmap)}
#Plot barchart that represents the mean probability that EAB emerges before firewood is burnt in that single month
ax3.bar([135,152,182,213,244,274],align = 'edge', height = df2['height'], width = df2['width'], color = list(colors.values()))

#Create labels for the legend
labels3 = list(colors.keys())
handles3 = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels3]
lgd = fig.legend(lines , labels , bbox_to_anchor = (0.925,1.2), ncol = 1)
#ax3.legend(handles, labels, loc = 'right')
ax3.set_ylabel('Probability')
ax3.set_xlabel('Julian Date')
#plt.legend(loc='best')
d={'May':138,'June':160,'July':192, 'August':220}
for k,v in d.items():
    ax3.text(v,0.1,k) 


import os 
os.chdir('\..')
os.chdir("Users/alexp/OneDrive - University of New Brunswick/Grad Studies/EAB_Model/Model_results")
plt.savefig('probability_EAB_emergence_from_unburned_firewood_joined',bbox_inches='tight',dpi=300)
plt.show()
