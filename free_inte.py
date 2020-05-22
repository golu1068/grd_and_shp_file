import requests
from selenium import webdriver
from struct import unpack
from pandas import DataFrame, read_csv
from os.path import split, join
import os
import tempfile
from glob import glob
import pandas as pd
from free_function import read_grd_rain, read_grd_temp, mean
from selenium.webdriver.support.ui import Select
import numpy as np
#############################################################################
result_dir = os.getcwd()
###################################
t = tempfile.TemporaryDirectory(dir = tempfile.gettempdir())
print(t.name)

rainfall_url = 'http://www.imdpune.gov.in/Clim_Pred_LRF_New/rainfall.php'
maxtemp_url = 'http://www.imdpune.gov.in/Clim_Pred_LRF_New/maxtemp.php'
mintemp_url = 'http://www.imdpune.gov.in/Clim_Pred_LRF_New/mintemp.php'

url = 'http://www.imdpune.gov.in/Clim_Pred_LRF_New/Grided_Data_Download.html'

##driver = webdriver.Chrome()
##
##driver.get(url)

headers = {
    'Host': 'www.imdpune.gov.in',
    'Connection': 'keep-alive',
    'Content-Length': '12',
    'Cache-Control': 'max-age=0',
    'Origin': 'http://www.imdpune.gov.in',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://www.imdpune.gov.in/Clim_Pred_LRF_New/Grided_Data_Download.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9'
    }

print ('AutoHydro-Basic version of Hydrology tools package')
print('Contact for further clarifications :Dr Karan Gupta, karang.abohar@gmail.com ')
rainfall = input("Do you need Rainfall data[y/n]? ")
if rainfall.lower() == 'y':
    rainfall_start = input("Please enter start year for Rainfall : ")
    rainfall_stop = input("Please enter stop year for Rainfall : ")
    
maxtemp = input("Do you need . Temp. data[y/n]? ")
if maxtemp.lower() == 'y':
    maxtemp_start = input("Please enter start year for Max. Temp. : ")
    maxtemp_stop = input("Please enter stop year for Max. Temp. : ")
    
mintemp = input("Do you need Min. Temp. data[y/n]? ")
if mintemp.lower() == 'y':
    mintemp_start = input("Please enter start year for Min. Temp. : ")
    mintemp_stop = input("Please enter stop year for Min. Temp. : ")
###########################################################
temp_range = list(range(maxtemp_start, maxtemp_stop+1))
#######################################################
if rainfall == 'y':
    for x in range(int(rainfall_start),int(rainfall_stop)+1):
        data = {'rain':str(x)}
        res = requests.post(rainfall_url, headers=headers, data=data, timeout=15)
        os.chdir(t.name)
        with open('rain_'+str(x)+'.grd','wb')as file:
            file.write(res.content)
        print('Downloaded Rainfall - '+str(x))
    

if maxtemp == 'y':
    for x in range(int(maxtemp_start),int(maxtemp_stop)+1):
        data = {'maxtemp':str(x)}
        res = requests.post(maxtemp_url, headers=headers, data=data, timeout=15)
        with open('maxtemp_'+str(x)+'.GRD','wb')as file:
            file.write(res.content)
        print('Downloaded Max. Temp. - '+str(x))
        

if mintemp == 'y':
    for x in range(int(mintemp_start),int(mintemp_stop)+1):
        data = {'mintemp':str(x)}
        res = requests.post(mintemp_url, headers=headers, data=data, timeout=15)
        with open('mintemp_'+str(x)+'.GRD','wb')as file:
            file.write(res.content)
        print('Downloaded Min. Temp. - '+str(x))


###############################################################################################
####  For rainfall
##dir = os.getcwd()
os.chdir(t.name)
curr_wd = os.getcwd()
files = glob(curr_wd + r'\rain*.grd')  

if (len(files) == 0):
    print('No any grd file in this folder')
for file in files:
    if (os.path.split(file)[1][0:4] == 'rain'):
        print(file)
        year = file[-8:-4]
        print(year)
        read_grd_rain(file, year, result_dir)

print('Conversion for Rainfall complete')
##################################################################################################
####  For temp
####dir = os.getcwd()
os.chdir(t.name)
curr_wd = os.getcwd()
files_max = glob(curr_wd + r'\maxtemp*.GRD')
files_min = glob(curr_wd + r'\mintemp*.GRD')
if (len(files_max) == 0):
    print('No any grd file in this folder')
for file in files_max:
    ### For max temp file
    file_name = os.path.split(file)[1]
    year = file_name[-8:-4]
    df_max = read_grd_temp(file, year, result_dir)
    print('max comp')
    ###########################################################################
    ## For min temp file
    file = curr_wd + '\mintemp_'+ file[-8:]
    if ((file in files_min) == True):
        df_min = read_grd_temp(file, year, result_dir)
        print('min comp')
    else:
        print('Mintemp file is not there for '+file[-8:-4]+' year')
    ##############################################################################
    ### For Mean
    curr_wd = os.getcwd()
    
    mean_file = os.path.join(curr_wd, 'mean_temp_'+str(year)+'.csv')
    mean_file_csv = open(mean_file, 'w', newline='')
    
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
    ###############################################################################
    print('Conversion to mean complete')
    
print('Conversion for Temp complete')
############################################################################################  
 
