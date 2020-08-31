# -*- coding: utf-8 -*-

"""
Created on Thu Mar 14 14:35:55 2019

@author: mitay
"""

import mne
import numpy as np
import scipy as sp
from numpy import genfromtxt
import csv
import pandas as pd
# datasets_list  - path to csv table with column names in the first row: subject_number,	subject_name,	group_number,	group_name,	eeg_data_path,	timing_path,	PSD_analysis_path
# eeg_data path - path to cleaned EEG dataset in .fif format
# timing path - path to csv table with column names in the first row: index_1	index_2	basic_start	basic_stop	ind_start	ind_stop
# index_1,2 - number of stage depending on two diffferent classifications, basic_start, stop - start and stop of stage according to instruction, ind_start, stop - start and stop time of good fragment in seconds 
with open(datasets_list, newline='') as datasets:
    lines = csv.reader(datasets, delimiter=';') # read datasets list
    
    for row in lines:
        if row[0] != 'subject_number': # skip the first row with column names
            columns={'subj','ind_wi_type','is_med','type','channel','delta_power', 'theta_power', 'alpha_power', 'beta_power', 'gamma_power', 'alpha_to_theta', 'alpha_to_beta','vals'}; # subj - subject number, ind_wi_type - number of segment among segments of the particular meditation stage
            df=pd.DataFrame(columns=columns)# create dataframe
            myfname = row[4]
            info = mne.io.read_info(fname = myfname)
            raw = mne.io.read_raw_fif(fname = myfname,preload=True);
            picks = mne.pick_types(raw.info, meg=True, eeg=True, stim=True)
            
            Wseconds = 1; #estimate PSD for every 1 second segment, can be changes according to your purpose and data
            some_picks = picks[:30]  # take first 30 chanels
            timing = genfromtxt(row[5], delimiter=';')
            ii = 1 
            count = 0
            stat_data = np.zeros((1442, 211)) # 1442 - the maximal number of 1 sec fragments in dataset, can be chaged accoding to your data, 210 = 30 channels * (5 eeg rythms+ 2 eeg ratios) +1 meditation stage
            for n_segment in range (17):
                count_wi_type = 0
                while ii < timing.shape[0] and int(timing[ii][0]) == n_segment: 
                    a = int(timing[ii][4]) # start of segment, sec
                    b = int(timing[ii][5]) # finish of segment, sec
                    ii += 1 
                    segment_len = b-a 
                    Nw =int(segment_len/Wseconds)
                    rythm = ('delta', 'theta', 'alpha', 'beta', 'gamma')
                    band1 = [1, 4, 8, 14, 25]
                    band2 = [4, 8, 14, 25, 40] 
                    ElName = raw.info['ch_names']
                    j = 1
                    for channel in range(30):
                        
                     # create table with date   
                        for i in range(5):
                            SegStart = a; 
                            for w in range(Nw): 
                                start, stop = raw.time_as_index([SegStart, SegStart+Wseconds]) 
                                data, times = raw[some_picks, start:stop]
                                f, Pxx_den = sp.signal.welch(data, info['sfreq'], nperseg=stop-start,nfft = 512)
                                SegStart = SegStart+Wseconds
                                stat_data[w + count, 0] = timing[ii-1][0]
                                ind1 = np.argmin(np.abs(band1[i]-f));
                                ind2 = np.argmin(np.abs(band2[i]-f));
                                stat_data[w + count, j] = np.mean(Pxx_den[channel,ind1:ind2])
                            j += 1 
                       #create dataframe with data 
                        SegStart = a; # начало временного отрезка
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
                            pandas_data = {'ind_wi_type':w + count_wi_type, 'is_med':row[2],'delta_power': np.mean(Pxx_den[channel,delta_start:delta_stop]), 'theta_power': np.mean(Pxx_den[channel,theta_start:theta_stop]), 'alpha_power': np.mean(Pxx_den[channel,alpha_start:alpha_stop]), 'beta_power': np.mean(Pxx_den[channel,beta_start:beta_stop]), 'gamma_power' : np.mean(Pxx_den[channel,gamma_start:gamma_stop]), 'alpha_to_theta':np.mean(Pxx_den[channel,alpha_start:alpha_stop])/np.mean(Pxx_den[channel,theta_start:theta_stop]), 'alpha_to_beta': np.mean(Pxx_den[channel,alpha_start:alpha_stop])/np.mean(Pxx_den[channel,beta_start:beta_stop]),'subj':row[0], 'type':timing[ii-1][0], 'channel':channel}
                            print(pandas_data)
                            df = df.append(pandas_data,ignore_index = True);
                        
                    # add eeg ratios to table
                    k = 151 
                    z = 3  
                    while k <210:
                        for w in range(Nw):
                            stat_data[w + count, k] = stat_data [w + count, z]/  stat_data [w + count, z-1] # alpha/theta
                            stat_data[w + count, k+1] = stat_data [w + count, z]/  stat_data [w + count, z+1] #alpha/beta
                        k += 2 
                        z += 5
                   
                    
                    count += Nw 
                    count_wi_type += Nw
            
            
            # csv_file_path - path to save csv files
            # df_file_path - path to save df files
            name  = csv_file_path + row[0] +'_'+ row[1]+ '_analysis.csv'
            np.savetxt(name, stat_data, delimiter=",")
            
 
            name1 = df_file_path + row[0] + '_' + row[1]+'_pandas_dataframe.csv'
            df.to_csv(name1)


