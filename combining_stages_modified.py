# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 15:48:06 2021

@author: mitay
"""
import pandas as pd
import os

stage_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
timing_combined_3 = [[0], [1], [2,3,4,5], [6,7,8], [9,10,11], [12,13,14,15],[16]]

##### create empty dataframe
band_list = ['delta_power', 'theta_power', 'alpha_power', 'beta_power', 'gamma_power', 'alpha_to_theta', 'alpha_to_beta']
channel_list = ['Fp1',  'Fp2',  'F7',  'F3',  'Fz',  'F4',  'F8',  'T7',  'C3',  'Cz',  'C4',  'T8',  'P7',  'P3',  'Pz',  'P4',  'P8',  'O1',  'O2',  'Oz',  'FC5',  'FC6',  'CP5',  'CP1',
 'CP2',  'CP6',  'PO3',  'PO4',  'FC1',  'FC2']
columns_name = ['subj_number', 'subj_name', 'group_number', 'time_point', 'stage']
for band in band_list:
    for channel in channel_list:
        columns_name.append(str(channel)+ '_' + str(band))
average_data = pd.DataFrame(columns=columns_name) 
DataDirectory = "D:\\work\\HSE\\meditation\\experiment_2021\\data\\analysis\\psd\\"
os.chdir(DataDirectory) 
onlyfiles = [fi for fi in os.listdir(DataDirectory) if os.path.isfile(os.path.join(DataDirectory, fi))]
index = 0
for data in onlyfiles: 
    df=pd.read_csv(data,sep=',')
    subject_name = df.loc[0, 'subj_name']
    for i in range(len(timing_combined_3)):
        stages = timing_combined_3[i]
        average_data.loc[index, ['subj_number', 'subj_name', 'group_number', 'time_point']] = df.loc[0, ['subj_number', 'subj_name', 'group_number', 'time_point']]
        average_data.loc[index, 'stage'] = i
        for band in band_list:
            print(subject_name, i, band)
            for channel in channel_list:
                name_of_column = str(channel)+ '_' + str(band)
                average_data.loc[index, name_of_column] = df.query('channel_name == @channel & @stages[0] <= stage <= @stages[-1]')[band].mean()               
                   
        index +=1         
              
        name = "D:\\work\\HSE\\meditation\\experiment_2021\\data\\analysis\\average_per_stage_psd_combined_stages.csv"
        average_data.to_csv(name)          