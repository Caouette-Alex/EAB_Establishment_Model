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