# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 20:39:44 2019

@author: mitay
"""

import numpy as np
import pandas as pd
from operator import itemgetter
import os
columns={'subj', 'is_med','type','channel','delta_power', 'theta_power', 'alpha_power', 'beta_power', 'gamma_power', 'alpha_to_theta', 'alpha_to_beta'}
df=pd.DataFrame(columns=columns) 
DataDirectory = 'D:\\work\\HSE\\meditation\\data\\ica_artifacts_clean\\cleaned data\\pandas_df_ind_PSD'
os.chdir(DataDirectory) 
onlyfiles = [fi for fi in os.listdir(DataDirectory) if os.path.isfile(os.path.join(DataDirectory, fi))]
onlyfiles_srt = sorted(onlyfiles, key=itemgetter(0,1));
stat_data = np.zeros((449, 213))
w = 0
count = 0
for data in onlyfiles_srt: 
#data = 'D:\\work\\HSE\\meditation\\data\\ica_artifacts_clean\\cleaned data\\Pandas_analysis_final\Aleksentsev_pandas_dataframe.csv'
    df=pd.read_csv(data,sep=',')
    type_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    band_list = ['delta_power', 'theta_power', 'alpha_power', 'beta_power', 'gamma_power', 'alpha_to_theta', 'alpha_to_beta']
    channel_list = ['Fp1',  'Fp2',  'F7',  'F3',  'Fz',  'F4',  'F8',  'T7',  'C3',  'Cz',  'C4',  'T8',  'P7',  'P3',  'Pz',  'P4',  'P8',  'O1',  'O2',  'Oz',  'Fc5',  'Fc6',  'Cp5',  'Cp1',
 'Cp2',  'Cp6',  'Po3',  'Po4',  'Fc1',  'Fc2']
    subject_name = str(data)[0:-21]
    print(subject_name)
    
    k = 3
    for band in band_list:
         w = 0
         for channel in range(30):
            df_channel = df.loc[df['channel'] == channel]
            
            for i in range(1,17):
                val = df_channel.loc[df['type'] == i][band].mean()
                stat_data[w + i + count, k] = val # среднее значение для данного этапа
                stat_data[w + i + count, 0] = i # номер этапа медитации
                stat_data[w + i + count, 1] = df.iloc[1]['is_med'] # группа (медитатор/контр)
                stat_data[w + i + count, 2] = df.iloc[1]['subj'] # номер испытуемого 
                
                #print(val)
            k += 1
    count += 16 

np.savetxt('D:\\work\\HSE\\meditation\\data\\ica_artifacts_clean\\cleaned data\\average_for_further_processing.csv', stat_data, delimiter=",")        
                
                
           
