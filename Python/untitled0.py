# -*- coding: utf-8 -*-
"""
Created on Mon May  1 09:21:28 2023

@author: alexp
"""
import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.special import gamma as gamma
for i in range(100):
    alpha=7.483
    beta=random.uniform(2,18)
    beta = 18
    sigma=random.uniform(1,3.2)
    #sigma = 3.2
    reservations_month = {}
    months = {'May':5,'June':6,'July':7,'August':8,'September':9,'October':10}
    x=np.linspace(5,10,6)
    y=(beta/(2*sigma*gamma(1/beta)))*np.exp(-(abs((x-alpha)/sigma))**beta)*4456
    plt.plot([0,1,2,3,4,5],y)