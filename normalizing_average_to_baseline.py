# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 14:58:51 2019

@author: mitay
"""
# change x, y, number of stages, numebr of subjects to your values

import numpy as np
from numpy import genfromtxt
data = genfromtxt('path to summary psd file', delimiter=',')
x = 1+ number of subjects*number of stages
y = number of channels*7+3
stat_data = np.zeros((x, y)) 
for n in range(3,y):
    for c in range (0, number of subjects):
        for i in range (1, number of stages+1):
            print(data[i + c*number of stages][n]/data[1+c*number of stages][n])
            val = data[i + c*number of stages][n]/data[1 + c*number of stages][n] 
            stat_data[i + c*number of stages][n] = val
np.savetxt('name of file with data normalized to baseline', stat_data, delimiter=",")
         