# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 09:11:13 2023

@author: alexp
"""
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import norm
import statistics
import seaborn as sns


cutoff = [3,5,7]
test = [0.2,0.5,1]
for cutoff in cutoff:
    pieces = [1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]
    plt.plot(pieces,(([0.5*(1-np.tanh(0.5*(i-cutoff))) for i in pieces])))
    plt.xlabel('firewood arrival')
    plt.ylabel('probability of establishment')
    plt.show()



def logistic(x, x0, k, L):
    return L/(1+np.exp(k*(x-x0)))

x= np.arange(start= 1, stop = 10, step = 0.5)
k = -1
x0 = 5
L = 1

f_x = logistic(x=x, x0=x0, k=k, L=L)
plt.plot(x, f_x, label=f"K: {k}")




f_x = L/(1+np.exp(k*(x-x0)))
plt.plot(x,f_x,)

#month= [109, 619, 1521, 1583, 559, 62]
#mean = statistics.mean(month)
#sd = statistics.stdev(month)
#x = [5,6,7,8,9,10]
#plt.plot(x,norm.pdf(month,mean,sd))
#sns.distplot(x=x, y=month)

#%%
import numpy as np
from matplotlib import pyplot as plt

x = np.arange(start= 130, stop = 290, step = 1)




f_x = (1.0 / (1.0 + np.exp(-(-0.135*(x-208))))) * (1-(-0.009*x+ 2.22))


plt.plot(x,f_x)

#%%
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.stats

x= np.array([5,6,7,8,9,10])
y= np.array([109.4,558.0,1425.6,1458.4,502.4,55.0])


# note that the len of bins is 51, since it contains upper and lower limit of every bin

# restore data from histogram: counts multiplied bin centers
restored = [[d]*int(y[n]) for n,d in enumerate((x[1:]+ x[:-1])/2)]
# flatten the result
restored = [item for sublist in restored for item in sublist]
from scipy.stats import norm
from numpy import linspace
from pylab import plot,show,hist,figure,title
import numpy as np
from matplotlib import pyplot as plt
# picking 150 of from a normal distrubution
# with mean 0 and standard deviation 1




param = norm.fit(restored) # distribution fitting

# now, param[0] and param[1] are the mean and 
# the standard deviation of the fitted distribution
x=linspace(5, 11, 50)
# fitted distribution
pdf_fitted = norm.pdf(x,loc=param[0],scale=param[1])
# original distribution
pdf = norm.pdf(x)

plt.title('Normal distribution')
plt.plot(x,pdf_fitted,'r-')
plt.hist(restored, density=2,alpha=.3)

plt.show

#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#x= np.array([5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,8,8,8,8,8,9,9,9,9,9,10,10,10,10,10])
#y = np.array([87,106,137,105,112,490,543,541,647,569,1375,1532,1527,1360,1334,1410,1390,1421,1435,1636,419,494,581,602,416,5,13,108,81,68])

x= np.array([5,6,7,8,9,10])
y= np.array([(109.4),(558.0),(1425.6),(1458.4),(502.4),(55.0)])

def Gauss(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

parameters, covariance = curve_fit(Gauss, x, y,p0=(1600,7.5,1))
  
fit_A = parameters[0]
fit_x0 = parameters[1]
fit_S = parameters[2]

xvals = np.linspace(5,10,50)

fit_y = Gauss(xvals, fit_A, fit_x0,fit_S)
plt.plot(x, y, 'o', label='data')
plt.plot(xvals, fit_y, '-', label='fit')
#%%

s=[1,1.5,2,3]
for s in s:
    a=1631
    x0=7.46
    

    y = a*np.exp(-(xvals-x0)**2/(2*s**2))
    
    plt.plot(xvals, y)


#%%
import numpy as np
from scipy.optimize import curve_fit
from scipy.special import gamma as gamma


def betafunc(x,a,b,cst):
    return cst*gamma(a+b) * (x**(a-1)) * ((1-x)**(b-1))  / ( gamma(a)*gamma(b) )


popt2,pcov2 = curve_fit(betafunc,x,y,maxfev=5000)
xvals = np.linspace((0),(1),100)
from matplotlib import pyplot as plt
plt.plot(xvals,betafunc(xvals,*popt2))
plt.plot(x,y)
plt.show()

#%%
#a=26.1
#b=22.74
a=24
b=24
cst= 292.1

y = cst*gamma(a+b) * (xvals**(a-1)) * ((1-xvals)**(b-1))  / ( gamma(a)*gamma(b) )
plt.plot(xvals,y)

#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import gamma as gamma

x= np.array([5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,8,8,8,8,8,9,9,9,9,9,10,10,10,10,10])
#y = np.array([87,106,137,105,112,490,543,541,647,569,1375,1532,1527,1360,1334,1410,1390,1421,1435,1636,419,494,581,602,416,5,13,108,81,68])

y = np.array([87/3786,106/4078,137/4315,105/4230,112/4135,
              490/3786,543/4078,541/4315,647/4230,569/4135,
             1375/3786,1532/4078,1527/4315,1360/4230,1334/4135,
              1410/3786,1390/4078,1421/4315,1435/4230,1636/4135,
              419/3786,494/4078,581/4315,602/4230,416/4135,
              5/3786,13/4078,108/4315,81/4230,68/4135])
#x= np.array([5,6,7,8,9,10])
#y= np.array([(109.4/1458.4),(558.0/1458.4),(1425.6/1458.4),(1458.4/1458.4),(502.4/1458.4),(55.0/1458.4)])
#y= np.array([(109.4/4108.8),(558.0/4108.8),(1425.6/4108.8),(1458.4/4108.8),(502.4/4108.8),(55.0/4108.8)])
def Gauss_kurt(x, alpha, beta, sigma):
    return (beta/(2*sigma*gamma(1/beta)))*np.exp(-(abs((x-alpha)/sigma))**beta)

parameters, covariance = curve_fit(Gauss_kurt, x, y,p0=[7.5,2,1])
  
fit_A = parameters[0]
fit_B = parameters[1]
fit_S = parameters[2]

xvals = np.linspace(5,10,50)

fit_y = Gauss_kurt(xvals, fit_A, fit_B,fit_S)
plt.plot(x, y, 'o', label='data')
plt.plot(xvals, fit_y, '-', label='fit')

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import gamma as gamma
import random
xvals = np.linspace(5,10,50)
d={}
for i in range(1000):
    alpha=7.483
    #alpha= random.uniform(5,10)
    #beta=1.94
    beta = 1.9
    #beta = random.uniform(2, 18)
    #sigma = 1.4
    sigma = 0.8
    sigma = random.uniform(1, 3.2)
    
    yvals = (beta/(2*sigma*gamma(1/beta)))*np.exp(-(abs((xvals-alpha)/sigma))**beta)
    plt.plot(xvals, yvals, 'o', label='data')
    plt.plot(xvals,yvals)
    
    x1=[5,6,7,8,9,10]
    y1={}
    for x_ in x1:
        
        y1[x_]=(beta/(2*sigma*gamma(1/beta)))*np.exp(-(abs((x_-alpha)/sigma))**beta)

    d[i]=sum(y1.values())
print(np.array(list(d.values())).mean())
print(np.std(np.array(list(d.values()))))
months=[5,6,7,8,9,10]
test={}
for month in months:     
    test[month]=(beta/(2*sigma*gamma(1/beta)))*np.exp(-(abs((month-alpha)/sigma))**beta)*4456
    
#%%

x = np.linspace(0, 439, 439)
A=0.135
B=208
C=0.009
D=2.22
E=1
#=5
i1=1
i2=1
i3=1

#d = {'May':17,'Jun':30,'Jul':31,'Aug':31, 'Sept':30,'Oct': 9}
d = {'May':[135,151],'Jun':[152,181],'Jul':[182,212],'Aug':[213,243], 'Sept':[244,273],'Oct': [274,282]}
d2={}
#d={'May':140,'June':163,'July':195, 'August':223, 'September': 250, 'October':272}
val= 0
val2= -1

plt.xlim(135,282)


for i in range(1):
    #i1= random.uniform(1,1.4)
    #i2 = random.uniform(1,1.4)
    #i3 = random.uniform(1,1)
    #A = random.uniform(0.1,0.2)
    #B = random.uniform(170, 250)
    #C= random.uniform(0.00,0.005)
    #D = random.uniform(0,1)
    E = random.uniform(0,1)
    Q = random.uniform(-74,74) 
    
    #y = (i1 / (i2 + np.exp(-(-A*((x+Q)-B)))))*((i3-(-C*(x+Q)+D)*E))
    y = (i1 / (i2 + np.exp(-(-A*((x)-B)))))*((i3-(-C*(x)+D)*E))
    x_1= x+Q
    #plt.plot(x_1,y)
    for k,v in d.items():
        indices = np.where((x_1 >= v[0]) & (x_1 <=v[1]))
        print(y[indices]) 
        trap = np.trapz(y[indices])
        plt.plot(x_1[indices],y[indices])
        d2[k] = trap
    for k, v in d2.items():
      if v < 0:d2[k]=0
    
    #df3 = pd.DataFrame(y,columns = ['y'])
    #df3['x']  = x_1
    #print(x_1[0],x[100])
    #for k,v in d.items():
        #x=12
    #trap = np.trapz(df3['y'],x=list(d.values()))
        #trap = np.trapz(df3['y'].loc[],df3['x'].loc[val:val2])    
    #l = [d2[v], trap]
    #
        #val = val+v
#q = 5
#y_1 = y
#y_1 = y+q


