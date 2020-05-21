import requests
from selenium import webdriver



rainfall_url = 'http://www.imdpune.gov.in/Clim_Pred_LRF_New/rainfall.php'
maxtemp_url = 'http://www.imdpune.gov.in/Clim_Pred_LRF_New/maxtemp.php'
mintemp_url = 'http://www.imdpune.gov.in/Clim_Pred_LRF_New/mintemp.php'

url = 'http://www.imdpune.gov.in/Clim_Pred_LRF_New/Grided_Data_Download.html'

driver = webdriver.Chrome()

driver.get(url)

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


if rainfall == 'y':
    for x in range(int(rainfall_start),int(rainfall_stop)+1):
        data = {'rain':str(x)}
        res = requests.post(rainfall_url, headers=headers, data=data, timeout=15)
        with open('rain_'+str(x)+'.grd','wb')as file:
            file.write(res.content)
        print('Downloaded Rainfall - '+str(x))
    

if maxtemp == 'y':
    for x in range(int(maxtemp_start),int(maxtemp_stop)+1):
        data = {'maxtemp':str(x)}
        res = requests.post(maxtemp_url, headers=headers, data=data, timeout=15)
        with open('maxtemp_'+str(x)+'.grd','wb')as file:
            file.write(res.content)
        print('Downloaded Max. Temp. - '+str(x))
        

if mintemp == 'y':
    for x in range(int(mintemp_start),int(mintemp_stop)+1):
        data = {'mintemp':str(x)}
        res = requests.post(mintemp_url, headers=headers, data=data, timeout=15)
        with open('mintemp_'+str(x)+'.grd','wb')as file:
            file.write(res.content)
        print('Downloaded Min. Temp. - '+str(x))