import requests
from selenium import webdriver
from struct import unpack
##from pandas import DataFrame, read_csv
from os.path import split, join
import os
import tempfile
from glob import glob
##import pandas as pd
##from free_function import read_grd_rain, read_grd_temp
from selenium.webdriver.support.ui import Select
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
files = glob('*.grd')  
if (len(files) == 0):
    print('No any grd file in this folder')
for file in files:
    if (file[0:4] == 'rain'):
        print(file)
        year = file[-8:-4]
        print(year)
        read_grd_rain(file, year, result_dir)
    else:
        print('Grd filename is not proper')
    break
print('Conversion for Rainfall complete')
###################################################################################################
####  For temp
####dir = os.getcwd()
os.chdir(t.name)
files = glob('*.GRD')
if (len(files) == 0):
    print('No any grd file in this folder')
for file in files:
    if (file[0:7] == 'maxtemp' or file[0:7] == 'mintemp'):
        print(file)
        year = file[-8:-4]
        read_grd_temp(file, year, result_dir)
    else:
        print('Grd filename is not proper')
    
print('Conversion for Temp complete')
############################################################################################
####   Temp mean
years = temp_range
max_file='';min_file=''
dir = result_dir + '/Result'
os.chdir(dir)
for year in years:
    files = glob('*'+str(year)+'.csv')
    for file in files:
        #print(file)
        if (file[0:7] == 'maxtemp'):
            max_file = file
        if (file[0:7] == 'mintemp'):
            min_file = file
        if (min_file != '' and max_file != ''):
            mean(max_file, min_file, year)
            break
