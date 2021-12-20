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
data = "D:\\work\\HSE\\meditation\\experiment_2021\\data\\analysis\\normalized_to_close_eyes_bl_combined_stages_combined_electrodes.csv"
df=pd.read_csv(data,sep=',')
df.columns = df.columns.str.lower()
columns = df.columns
for column in columns[7:]:
    directory = column
    parent_dir = "D:\\work\\HSE\\meditation\\experiment_2021\\data\\analysis\\plots\\"
    path = os.path.join(parent_dir, directory) 
    os.mkdir(path) 
    for name in df['subj_name'].unique():
        plt.close('all')
        group = str(df[df['subj_name'] == name]['group_number'].unique()[0])
        title = (str(name) + '_' + column + '_' + group)
        ytitle = column +'/normalized_to_baseline'
        sns.lineplot(data = df.query('subj_name == @name & time_point == 1 & stage > 0'), y = column, x = 'stage', color = 'orange').set(title = title, xlabel = 'стадия медитации', ylabel = ytitle)
        sns.lineplot(data = df.query('subj_name == @name & time_point == 0 & stage > 0'), y = column, x = 'stage', color = 'b').set(title = title, xlabel = 'стадия медитации', ylabel = ytitle)
        plt.legend(labels=['до курса','после курса'])
        plt.show()
        file_name = path +'\\' + name + '.jpg'
        print(file_name)
        plt.savefig(file_name)
    