# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 20:39:44 2019

@author: mitay
"""

import pandas as pd
import os

columns_name = ['subj_number', 'subj_name', 'group_number', 'time_point', 'iaf_open_eyes', 'iaf_close_eyes']
iaf_data = pd.DataFrame(columns=columns_name) 
DataDirectory = "D:\\work\\HSE\\meditation\\experiment_2021\\data\\analysis\\iaf\\"
os.chdir(DataDirectory) 
onlyfiles = [fi for fi in os.listdir(DataDirectory) if os.path.isfile(os.path.join(DataDirectory, fi))]
index = 0
for data in onlyfiles: 
    df=pd.read_csv(data,sep=',')
    subject_name = df.loc[0, 'subj_name']
    iaf_data.loc[index, ['subj_number', 'subj_name', 'group_number', 'time_point']] = df.loc[0, ['subj_number', 'subj_name', 'group_number', 'time_point']]
    iaf_data.loc[index, 'iaf_open_eyes'] = df.query('20 < channel < 30 & stage == 0')['alpha_IAF'].mean() # усредняем значение по париетальным и окципитальным электродам
    iaf_data.loc[index, 'iaf_close_eyes'] = df.query('20 < channel < 30 & stage == 1')['alpha_IAF'].mean() # усредняем значение по париетальным и окципитальным электродам
    index +=1         
    name = "D:\\work\\HSE\\meditation\\experiment_2021\\data\\analysis\\iaf_average.csv"
    iaf_data.to_csv(name)          
       
                
                
           
