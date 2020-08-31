# meditation_data_processing
1.	Run script PSD_estimation.py
Input: Datasets in .fif format, datastes list in csv format, timing table in csv format
Output: set of tables in .csv format and set of dataframes in csv. format

2.	Run script averaging_meditation_data.py 
Input: set of dataframes in csv format
Output: table in csv format. Columns:  meditation stage, group number, subject number, columns with average values on the certain meditation stage in particular subject: delta power (* 30 channels), theta power (* 30 channels), alpha power (* 30 channels), beta power (*30 channels), gamma power (* 30 channels), alpha/theta ratio (*30 channels), alpha/beta ratio (*30 channels). The order of channels can be found in the script (channel_list)
3.	Run script normalizing_average_to_baseline.py 
Input: data file you got by using previous script
Output: table with the same columns, data for each subject are normalized to individual baseline (value of power in the same subject, band and channel on the first stage)
