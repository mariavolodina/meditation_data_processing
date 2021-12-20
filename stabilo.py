# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 11:50:32 2021

@author: mitay
"""
#!pip install -U seaborn

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os 
data = "D:\\work\\HSE\\meditation\\experiment_2021\\data\\pretesting\\pretesting_Lazareva_210521\\stabilo_Lazareva_250521\\romberg_lazareva.csv"
df=pd.read_csv(data,sep=';')
df.columns = df.columns.str.lower()
def distance_count(input_data):
    sum_distance = 0
    for i in range (input_data.index[0]+1, input_data.index[-1]+1):
        x1 = input_data.loc[i-1, 'x']
        y1 = input_data.loc[i-1, 'y']
        x2 = input_data.loc[i, 'x']
        y2 = input_data.loc[i, 'y']
        distance = ((x2-x1)**2 + (y2-y1)**2)**0.5
        sum_distance += distance
        return sum_distance
'''
input_data = df.query('condition == 1')
print(distance_count(input_data))
input_data = df.query('condition == 2')
print(distance_count(input_data))
'''

dataset = "D:\\work\\HSE\\meditation\\experiment_2021\\data\\datasets_list_2021.csv"
df=pd.read_csv(dataset,sep=';')
data = df.loc[:, ['subject_number', 'subject_name', 'group_number', 'time_point']]
columns = ['subject_number', 'subject_name', 'group_number', 'time_point']
romberg_data = pd.DataFrame(data = data, columns = columns)
romberg_data['distance_open_eyes'] = 0
romberg_data['distance_close_eyes'] = 0
romberg_data['mass'] = 0
romberg_data['A_per_sec_open_eyes'] = 0
romberg_data['A_per_sec_close_eyes'] = 0
for i in range(len(df)):
    stabilo_data = pd.read_csv(df.loc[i, 'romberg_path'],sep=';')
    stabilo_data.columns = stabilo_data.columns.str.lower()
    input_data_open = stabilo_data.query('condition == 1')
    input_data_close = stabilo_data.query('condition == 2')
    romberg_data.loc[i, 'distance_open_eyes'] = distance_count(input_data_open)
    romberg_data.loc[i, 'distance_close_eyes'] = distance_count(input_data_close)
    romberg_data.loc[i, 'mass'] = stabilo_data.loc[:, 'mass'].mean()
    romberg_data.loc[i, 'A_per_sec_open_eyes'] = romberg_data.loc[i, 'mass']*romberg_data.loc[i, 'distance_open_eyes']
    romberg_data.loc[i, 'A_per_sec_close_eyes'] = romberg_data.loc[i, 'mass']*romberg_data.loc[i, 'distance_close_eyes']

name = 'D:\\work\\HSE\\meditation\\experiment_2021\\data\\analysis\\romberg.csv'
romberg_data.to_csv(name)                
                    
    

    