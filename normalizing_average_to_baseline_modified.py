# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 16:38:11 2021

@author: mitay
"""

import pandas as pd
#data = 'D:\\work\\HSE\\meditation\\experiment_2021\\data\\analysis\\average_per_stage_psd.csv'
data = 'D:\\work\\HSE\\meditation\\experiment_2021\\data\\analysis\\average_per_stage_psd_combined_stages_combined_electrodes.csv'
df=pd.read_csv(data,sep=',')
df.columns = df.columns.str.lower()
for name in df['subj_name'].unique():
    for point in range(2):
        #for i in range(0,17):
        for i in range(0,7): #for combined stages
            current_data = df.query('subj_name == @name & time_point == @point and stage == @i')
            baseline_data = df.query('subj_name == @name & time_point == @point and stage == 1')
            index = current_data.index[0]
            index_baseline = baseline_data.index[0] 
            #df.loc[index, 'fp1_delta_power':'fc2_alpha_to_beta'] = df.loc[index, 'fp1_delta_power':'fc2_alpha_to_beta']/df.loc[index_baseline, 'Fp1_delta_power':'FC2_alpha_to_beta']
            df.loc[index, 'prefrontal_delta_power':'occipital_alpha_to_beta'] = df.loc[index, 'prefrontal_delta_power':'occipital_alpha_to_beta']/df.loc[index_baseline, 'prefrontal_delta_power':'occipital_alpha_to_beta']
name = "D:\\work\\HSE\\meditation\\experiment_2021\\data\\analysis\\normalized_to_close_eyes_bl_combined_stages_combined_electrodes.csv"
df.to_csv(name) 