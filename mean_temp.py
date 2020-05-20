import pandas as pd
import numpy as np
import os
from glob import glob

#min_file = '/home/nagendra/python_code/freela/all_grd/_Clim_Pred_LRF_New_GridDataDownload_Mintemp_MinT_2019_grd_2019.csv'
#
#max_file = '/home/nagendra/python_code/freela/all_grd/_Clim_Pred_LRF_New_GridDataDownload_Maxtemp_MaxT_2019_grd_2019.csv'
#
#mean_file = '/home/nagendra/python_code/freela/all_grd/_Clim_Pred_LRF_New_GridDataDownload_Maxtemp_MaxT_2019_grd_mean_2019.csv'

def mean(max_file, min_file, year):
    dir_path = os.path.split(max_file)[0]
    print(dir_path)
    mean_file = os.path.join(dir_path, 'mean_temp_'+str(year)+'.csv')
    mean_file_csv = open(mean_file, 'w', newline='')
    
    df_min = pd.read_csv(min_file, low_memory=False)
    df_max = pd.read_csv(max_file, low_memory=False)
    
    df_mean = pd.DataFrame()
    df_header = list(df_min)[2:]
    
    df_mean.insert(0, 'Latitude', df_min['Latitude'][0:961])
    df_mean.insert(1, 'Longitude', df_min['Longitude'][0:961])
    
    for i in range(len(df_header)):
        a = np.array(df_min[df_header[i]])
        b = np.array(df_max[df_header[i]])
        c = (a + b)/2
        header = list(df_mean)
        df_mean.insert(len(header),  'day_'+str('%s'%(i+1)), c)
    df_mean.to_csv(mean_file_csv, index=False)
    
    mean_file_csv.close()
###########################################################################################  
years = [2004, 2019]
max_file='';min_file=''
dir = os.getcwd()
os.chdir(dir)
for year in years:
    files = glob('*'+str(year)+'.csv')
    for file in files:
        #print(file)
        if (file[-22:-18] == 'MaxT'):
            max_file = file
        if (file[-22:-18] == 'MinT'):
            min_file = file
        if (min_file != '' and max_file != ''):
            mean(max_file, min_file, year)
            break
########################################################
#dir = os.getcwd()
#os.chdir(dir)
#files = glob('*.csv')
#max_file='';min_file=''
#years = [2017, 2019]
#if (len(files) == 0):
#    print('No any csv file in this folder')
#for year in years:
#    for file in files:
#        if (file[-22:-18] == 'MaxT' and file[-8:] == str(year)+'.csv'):
#            max_file = file
#            year = file[-8:-4]
#        if (file[-22:-18] == 'MinT'):
#            min_file = file
#            year = file[-8:-4]
#        if (min_file != '' and max_file != ''):
#            mean(max_file, min_file, year)
    
    
print('Conversion done')
input('Please press Enter key')
