from struct import unpack
from pandas import DataFrame
from os.path import split, join
import os
from glob import glob
#def read_grd(file_path, year, msg):
def read_grd(file_path, year):
    dir_path = split(file_path)[0]
    file_name = split(file_path)[1]
    
    write_file_path = join(dir_path, file_name[:-4]+'_grd'+'_'+str(year)+ '.txt')#r'/home/nagendra/Downloads/grd_out.txt'
    csv_file = join(dir_path, file_name[:-4]+'_grd'+ '_'+str(year)+'.csv')#r'/home/nagendra/Downloads/grd_out.csv'
    
    out_file = open(write_file_path, 'w+')
    out_file_csv = open(csv_file, 'w', newline='')
    
    
#    file_path = r'/home/nagendra/Downloads/Clim_Pred_LRF_New_GridDataDownload_Rainfall_ind2006_rfp25.grd'
    data = open(file_path,'rb')
    main_csv_data=[];main_header=[];
    ###################################################
#    cols = 135
#    rows = 129
#    interval = 0.25
#    lat_start = 6.5
#    long_start = 66.5
    #####################################################
    nd1 = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    nd2 = [0,31,29,31,30,31,30,31,31,30,31,30,31]
    if (len((year)) != 4):
        print('Give a year of 4 digit')
        return 0
    year = int(year)
    
    lo=[];la=[];
    
    
    for i in range(135):
        lo.append(long_start + i * interval)
    for i in range(129):
        la.append(lat_start + i * interval)
    
    year1 = int(year/4)
    year1 = year1*4
    
    rf=[];csv_header=[];csv_data=[];header=[];sr_no=0
    #########################################################
    main_header.append('Serial No.')
    main_header.append('Latitude')
    main_header.append('Longitude')
    main_header.append('Date')
    main_header.append('Rainfall')
    
    out_file.write('Serial No.    ')
    out_file.write('Latitude   ')
    out_file.write('Longitude   ')
    out_file.write('Date       ')
    out_file.write('Rainfall')
    out_file.write('\n')
    
    for month in range(1,13):
        nd = nd1[month]
        if (year == year1):
            nd = nd2[month]
        for date in range(1, nd+1):
            for i in range(rows): ## 129
                for j in range(cols):  ## 135
                    line = (data.read(4))
                    line_len = len(line)
                    if (line_len != 4):
    #                    line_len = 
                        line = line + b'\x00'*(4-line_len)
    #                a = (struct.unpack(str(len(line)//4+1) + 'f', ipadded_data))
                    
                    rainfall = (unpack('f', line))
                    #################################################
#                    if (rainfall[0] != -999.0 and rainfall[0] != 0.0):
                    sr_no += 1
                    out_file.write('%9d'%(sr_no))
                    out_file.write('%10.2f'%(la[i]))
                    out_file.write('%12.2f'%(lo[j]))
                    out_file.write('%5d'%(date))
                    out_file.write('%02d'%(month))
                    out_file.write('%04d'%(year))
                    out_file.write('     ')
                    out_file.write('%f'%(rainfall[0]))
                    out_file.write('\n')
                    ###############################################
                    csv_data.append(sr_no)
                    csv_data.append(la[i])
                    csv_data.append(lo[j])
                    csv_data.append(str(('%02d'%(date) + '%02d'%(month) + '%04d'%(year))))
                    csv_data.append(rainfall[0])
                    ###############################################
                    main_csv_data.append(csv_data)
                    csv_data=[];
                
#        msg.config(text='Month= '+str(month))
#        msg.update_idletasks()         
        print(month)
    out_file.close()
    
    df = DataFrame(main_csv_data, columns= main_header)
    df.to_csv(out_file_csv, index=False)
    
    data.close()
    
    out_file_csv.close()
    
#################################################################  
cols = 31
rows = 31
lat_start = 7.5
long_start = 67.5
interval = 1
###############################################################   
dir = os.getcwd()
os.chdir(dir)
files = glob('*.GRD')
print(files)
if (len(files) == 0):
    print('No any grd file in this folder')
for file in files:
    if (file[-13:-9] == 'MaxT' or file[-13:-9] == 'MinT'):
        print(file)
        year = file[-8:-4]
        read_grd(file, year)
    else:
        print('Grd filename is not proper')
        
print('Conversion done')
input('Please press Enter key')

           
        
        
        
        
        
