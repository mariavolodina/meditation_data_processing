# -*- coding: utf-8 -*-

"""
Created on Thu Mar 14 14:35:55 2019

@author: mitay
"""

import mne
import numpy as np
import scipy as sp
import pandas as pd


datasets_list_csv = 'D:\\work\\HSE\\meditation\\experiment_2021\\data\\test.csv'
datasets_list = pd.read_csv(datasets_list_csv, delimiter=';')

    
for i in range(len(datasets_list)):
    columns={'subj_number', 'subj_name', 'group_number','time_point', 'stage','channel', 'alpha_IAF'}; # subj - subject number, ind_wi_type - number of segment among segments of the particular meditation stage
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
    for n_segment in range (2):
        count_wi_type = 0
        while ii < len(timing) and timing.loc[ii, 'index_1'] == n_segment: 
            start_segment = timing.loc[ii, 'ind_start'] # start of segment, sec
            stop_segment = timing.loc[ii, 'ind_stop'] # finish of segment, sec
            segment_len = stop_segment - start_segment
            Nw = int(segment_len/Wseconds)
            ElName = raw.info['ch_names']
            j = 1
            for channel in range(30):
                #create dataframe with data 
                alpha_iaf = []
                SegStart = start_segment; # начало временного отрезка
                for w in range(Nw): # для каждого секундного отрезка во фрагменте, без перекрытия, потому что в тайминге есть фрагменты длинной в 1 сек
                    start, stop = raw.time_as_index([SegStart, SegStart+Wseconds]) 
                    data, times = raw[some_picks, start:stop]
                    f, Pxx_den = sp.signal.welch(data, info['sfreq'],  nperseg=stop-start, nfft = 512)
                    SegStart = SegStart+Wseconds
                    alpha_start = np.argmin(np.abs(8-f));
                    alpha_stop = np.argmin(np.abs(14-f))                            
                    alpha_iaf.append(f[alpha_start + np.argmax(Pxx_den[channel,alpha_start:alpha_stop])])
                    
                    
                pandas_data = {'group_number':datasets_list.loc[i, 'group_number'], 'time_point': datasets_list.loc[i, 'time_point'], 'alpha_IAF': np.mean(alpha_iaf), 'subj_number':datasets_list.loc[i, 'subject_number'], 'subj_name':datasets_list.loc[i, 'subject_name'], 'stage':timing.loc[ii, 'index_1'], 'channel':channel, 'channel_name':raw.ch_names[channel]}
                print(ii, pandas_data)
                df = df.append(pandas_data, ignore_index = True);
            ii += 1                         
                   
            
            
            
 
        name1 = datasets_list.loc[i, 'iaf_analysis_path']
        df.to_csv(name1)


