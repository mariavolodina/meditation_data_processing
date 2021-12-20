# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 20:39:44 2019

@author: mitay
"""

import pandas as pd
data = 'D:\\work\\HSE\\meditation\\experiment_2021\\data\\analysis\\average_per_stage_psd_combined_stages.csv'
df=pd.read_csv(data,sep=',')
df.columns = df.columns.str.lower()
band_list = ['delta_power', 'theta_power', 'alpha_power', 'beta_power', 'gamma_power', 'alpha_to_theta', 'alpha_to_beta']
chanel_list = ['fp1', 'fp2', 'f7', 'f3', 'fz', 'f4', 'f8', 't7', 'c3', 'cz', 'c4', 't8', 'p7', 'p3', 'pz', 'p4', 'p8', 'o1', 'o2', 'oz', 'fc5', 'fc6', 'cp5', 'cp1', 'cp2', 'cp6', 'po3', 'po4', 'fc1', 'fc2']
chanel_group_names = ['prefrontal_', 'left_frontal_', 'right_frontal_', 'frontal_', 'central_', 'parietal_', 'left_temporal_', 'right_temporal_', 'left_central_', 'right_central_', 'left_parietal_', 'right_parietal_', 'occipital_']
columns = ['subj_number', 'subj_name', 'group_number', 'time_point', 'stage']
chan_band_names = []
for band in band_list:
    for chanel in chanel_group_names:
        columns.append(chanel+band)
        chan_band_names.append(chanel+band)
combined_electrodes_data = pd.DataFrame(columns = columns)

prefrontal_channel_list = [0,  1]
left_frontal_channel_list = [3, 2]
right_frontal_channel_list = [5, 6]
frontal_channel_list = [4]
central_channel_list = [28, 29, 9, 23, 24]
parietal_channel_list = [14]
left_temporal_channel_list = [7]
right_temporal_channel_list = [11]
left_central_channel_list = [20, 8, 22]
right_central_channel_list = [21, 10, 25]
left_parietal_channel_list = [12, 13, 26]
right_parietal_channel_list = [15, 16, 27]
occipital_channel_list = [17, 19, 18]
channel_group_list = [prefrontal_channel_list, left_frontal_channel_list, right_frontal_channel_list, frontal_channel_list, central_channel_list, parietal_channel_list, left_temporal_channel_list, right_temporal_channel_list, left_central_channel_list, right_central_channel_list, left_parietal_channel_list, right_parietal_channel_list, occipital_channel_list]

for i in range(len(df)):
    combined_electrodes_data.loc[i, 'subj_number': 'stage'] = df.loc[i, 'subj_number': 'stage']
    for group_index in range(13):
        for band in band_list:
            columns_of_interest = []
            for chan_number in channel_group_list[group_index]:
                columns_of_interest.append(chanel_list[chan_number] +'_'+ band)
            combined_electrodes_data.loc[i, chanel_group_names[group_index]+band] = df.loc[i, columns_of_interest].mean()
                
    
    
name = 'D:\\work\\HSE\\meditation\\experiment_2021\\data\\analysis\\average_per_stage_psd_combined_stages_combined_electrodes.csv'
combined_electrodes_data.to_csv(name)                
                
           
