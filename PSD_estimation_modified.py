# -*- coding: utf-8 -*-

"""
Created on Thu Mar 14 14:35:55 2019

@author: mitay
"""

import mne
import numpy as np
import scipy as sp
import pandas as pd
import scipy.signal

#datasets_list_csv = 'D:\\work\\HSE\\meditation\\experiment_2021\\data\\datasets_list_2021.csv'
datasets_list_csv = 'D:\\work\\HSE\\meditation\\experiment_2021\\data\\test.csv'
datasets_list = pd.read_csv(datasets_list_csv, delimiter=';')
# datasets_list  - path to csv table with column names in the first row: subject_number,	subject_name,	group_number,	group_name,	eeg_data_path,	timing_path,	PSD_analysis_path
# eeg_data path - path to cleaned EEG dataset in .fif format
# timing path - path to csv table with column names in the first row: index_1	index_2	basic_start	basic_stop	ind_start	ind_stop
# index_1,2 - number of stage depending on two diffferent classifications, basic_start, stop - start and stop of stage according to instruction, ind_start, stop - start and stop time of good fragment in seconds 
 # read datasets list
    
for i in range(len(datasets_list)):
    columns={'subj_number', 'subj_name', 'group_number','time_point', 'stage','channel','delta_power', 'theta_power', 'alpha_power', 'beta_power', 'gamma_power', 'alpha_to_theta', 'alpha_to_beta'}; # subj - subject number, ind_wi_type - number of segment among segments of the particular meditation stage
    df=pd.DataFrame(columns=columns)# create dataframe
    myfname = datasets_list.loc[i, 'eeg_data_path']
    info = mne.io.read_info(fname = myfname)
    raw = mne.io.read_raw_fif(fname = myfname,preload=True);
    picks = mne.pick_types(raw.info, meg=True, eeg=True, stim=True)
            
    Wseconds = 1; #estimate PSD for every 1 second segment, can be changes according to your purpose and data
    some_picks = picks[:30]  # take first 30 chanels
    timing = pd.read_csv(datasets_list.loc[i, 'timing_path'], delimiter=';')
    ii = 0 
    count = 0
    #stat_data = np.zeros((2280, 211)) # 2280 sec - (38 min) - the maximal number of 1 sec fragments in dataset, can be chaged accoding to your data, 210 = 30 channels * (5 eeg rythms+ 2 eeg ratios) +1 meditation stage
    for n_segment in range (17):
        count_wi_type = 0
        while ii < len(timing) and timing.loc[ii, 'index_1'] == n_segment: 
            start_segment = timing.loc[ii, 'ind_start'] # start of segment, sec
            stop_segment = timing.loc[ii, 'ind_stop'] # finish of segment, sec
            segment_len = stop_segment - start_segment
            Nw = int(segment_len/Wseconds)
            rythm = ('delta', 'theta', 'alpha', 'beta', 'gamma')
            band1 = [1, 4, 8, 14, 25]
            band2 = [4, 8, 14, 25, 40] 
            ElName = raw.info['ch_names']
            j = 1
            for channel in range(30):
                #create dataframe with data 
                SegStart = start_segment; # начало временного отрезка
                for w in range(Nw): # для каждого секундного отрезка во фрагменте, без перекрытия, потому что в тайминге есть фрагменты длинной в 1 сек
                    start, stop = raw.time_as_index([SegStart, SegStart+Wseconds]) 
                    data, times = raw[some_picks, start:stop]
                    f, Pxx_den = sp.signal.welch(data, info['sfreq'],  nperseg=stop-start,nfft = 512)
                    SegStart = SegStart+Wseconds
                    
                    delta_start = np.argmin(np.abs(band1[0]-f));
                    delta_stop = np.argmin(np.abs(band2[0]-f));
                    theta_start = np.argmin(np.abs(band1[1]-f));
                    theta_stop = np.argmin(np.abs(band2[1]-f));
                    alpha_start = np.argmin(np.abs(band1[2]-f));
                    alpha_stop = np.argmin(np.abs(band2[2]-f));
                    beta_start = np.argmin(np.abs(band1[3]-f));
                    beta_stop = np.argmin(np.abs(band2[3]-f));
                    gamma_start = np.argmin(np.abs(band1[4]-f));
                    gamma_stop = np.argmin(np.abs(band2[4]-f));
                    
                    pandas_data = {'group_number':datasets_list.loc[i, 'group_number'], 'time_point': datasets_list.loc[i, 'time_point'], 'delta_power': np.mean(Pxx_den[channel,delta_start:delta_stop]), 'theta_power': np.mean(Pxx_den[channel,theta_start:theta_stop]), 'alpha_power': np.mean(Pxx_den[channel,alpha_start:alpha_stop]), 'beta_power': np.mean(Pxx_den[channel,beta_start:beta_stop]), 'gamma_power' : np.mean(Pxx_den[channel,gamma_start:gamma_stop]), 'alpha_to_theta':np.mean(Pxx_den[channel,alpha_start:alpha_stop])/np.mean(Pxx_den[channel,theta_start:theta_stop]), 'alpha_to_beta': np.mean(Pxx_den[channel,alpha_start:alpha_stop])/np.mean(Pxx_den[channel,beta_start:beta_stop]),'subj_number':datasets_list.loc[i, 'subject_number'], 'subj_name':datasets_list.loc[i, 'subject_name'], 'stage':timing.loc[ii, 'index_1'], 'channel':channel, 'channel_name':raw.ch_names[channel]}
                    print(ii, pandas_data)
                    df = df.append(pandas_data, ignore_index = True);
        
            ii += 1                         
                   
            
            
            
 
        name1 = datasets_list.loc[i, 'PSD_analysis_path']
        df.to_csv(name1)


