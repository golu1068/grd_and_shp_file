from os.path import split, join
from struct import unpack
from pandas import DataFrame, read_csv
import os
import pandas as pd
import numpy as np
from geopandas import GeoDataFrame
from shapely.geometry import Point
#######################################################################################
cols = 135
rows = 129
lat_start = 6.5
long_start = 66.5
interval = 0.25
########################################################################
def read_grd_rain(file_path, year, result_dir):
    result_dir = result_dir + '/Result'
    try:
        os.mkdir(result_dir)
    except:
        pass
    os.chdir(result_dir)
    curr_wd = os.getcwd()
    
#    dir_path = split(file_path)[0]
    file_name = split(file_path)[1]
    
    csv_file = join(curr_wd, file_name[:-4]+ '.csv')#r'/home/nagendra/Downloads/grd_out.csv'
    out_file_csv = open(csv_file, 'w', newline='')
    #######################################################################################
    cols = 135
    rows = 129
    lat_start = 6.5
    long_start = 66.5
    interval = 0.25
    ########################################################################
    data = open(file_path,'rb')
    main_csv_data=[];main_header=[];
################################################################
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
    
    rf=[];csv_header=[];csv_data=[];header=[];sr_no=0;again=0;date_list=[];
    #########################################################
    main_header.append('Serial No.')
    main_header.append('Latitude')
    main_header.append('Longitude')
    main_header.append('Date')
    main_header.append('Rainfall')
    
    for month in range(1,13):
        nd = nd1[month]
        if (year == year1):
            nd = nd2[month]
        for date in range(1, nd+1):
            again=0
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
                    sr_no += 1###########################
                    csv_data.append(sr_no)
                    csv_data.append(la[i])
                    csv_data.append(lo[j])
                    csv_data.append(str(('%02d'%(date) + '%02d'%(month) + '%04d'%(year))))
                    csv_data.append(rainfall[0])
                    if (again==0):
                        date_list.append(str(('%02d'%(date) + '%02d'%(month) + '%04d'%(year))))
                        again=1
                    ###############################################
                    main_csv_data.append(csv_data)
                    csv_data=[];
                
#        msg.config(text='Month= '+str(month))
#        msg.update_idletasks()         
        print(month)
#    print(date_list)
    df = DataFrame(main_csv_data, columns= main_header)
    ##############################################################
    df.to_csv(out_file_csv, index=False)
    
    data.close()
    
    out_file_csv.close()
    ############################################################
    df = read_csv(csv_file, low_memory=False)
    df11 = DataFrame()
    
    df11.insert(0, 'Latitude', df['Latitude'][0:17415])
    
    df11.insert(1, 'Longitude', df['Longitude'][0:17415])
    grp = df.groupby('Date')
    for i in range(0,len(date_list)):
        day = grp.get_group(int(date_list[i]))
        var = list(day.Rainfall)
        header = list(df11)
        df11.insert(len(header), 'day_'+str('%s'%(i+1)), var)
       
    ############################################################
    out_file_csv = open(csv_file, 'w', newline='')
#    df11.to_csv(out_file_csv, index=False)

    out_file_csv.close()
    
    return df11
###########################################################################################
def read_grd_temp(file_path, year, result_dir):
    result_dir = result_dir + '/Result'
    try:
        os.mkdir(result_dir)
    except:
        pass
    os.chdir(result_dir)
    curr_wd = os.getcwd()
    
#    dir_path = split(file_path)[0]
    file_name = split(file_path)[1]
    
    csv_file = join(curr_wd, file_name[:-4]+ '.csv')
    
    out_file_csv = open(csv_file, 'w', newline='')
    #######################################################################################
    cols = 31
    rows = 31
    lat_start = 7.5
    long_start = 67.5
    interval = 1
    ########################################################################
    data = open(file_path,'rb')
    main_csv_data=[];main_header=[];

    nd1 = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    nd2 = [0,31,29,31,30,31,30,31,31,30,31,30,31]
    if (len((year)) != 4):
        print('Give a year of 4 digit')
        return 0
    year = int(year)
    
    lo=[];la=[];rainfall=[];
    
    
    for i in range(135):
        lo.append(long_start + i * interval)
    for i in range(129):
        la.append(lat_start + i * interval)
    
    year1 = int(year/4)
    year1 = year1*4
    
    rf=[];csv_header=[];csv_data=[];header=[];sr_no=0;again=0;date_list=[];
    #########################################################
    main_header.append('Serial No.')
    main_header.append('Latitude')
    main_header.append('Longitude')
    main_header.append('Date')
    main_header.append('Rainfall')
    
    for month in range(1,13):
        nd = nd1[month]
        if (year == year1):
            nd = nd2[month]
        for date in range(1, nd+1):
            again=0
            for i in range(rows): ## 129
                for j in range(cols):  ## 135
                    line = (data.read(4))
                    line_len = len(line)
                    if (line_len != 4):
    #                    line_len = 
                        line = line + b'\x00'*(4-line_len)
    #                a = (struct.unpack(str(len(line)//4+1) + 'f', ipadded_data))
                    
                    rainfall_data = (unpack('f', line))
                    if (round(rainfall_data[0], 2) == 99.9):
                        rainfall.append(-999.0)
                    rainfall.append(rainfall_data[0])
                    #################################################
#                    if (rainfall[0] != -999.0 and rainfall[0] != 0.0):
                    sr_no += 1
                    ###############################################
                    csv_data.append(sr_no)
                    csv_data.append(la[i])
                    csv_data.append(lo[j])
                    csv_data.append(str(('%02d'%(date) + '%02d'%(month) + '%04d'%(year))))
                    csv_data.append(rainfall[0])
                    if (again==0):
                        date_list.append(str(('%02d'%(date) + '%02d'%(month) + '%04d'%(year))))
                        again=1
                    ###############################################
                    main_csv_data.append(csv_data)
                    csv_data=[];
                    rainfall=[];
                
#        msg.config(text='Month= '+str(month))
#        msg.update_idletasks()         
        print(month)
    
    df = DataFrame(main_csv_data, columns= main_header)
    df.to_csv(out_file_csv, index=False)
    print(df)
    data.close()
    
    out_file_csv.close()
    ############################################################
    df = read_csv(csv_file, low_memory=False)
    print(df)
    df11 = DataFrame()
    
    df11.insert(0, 'Latitude', df['Latitude'][0:961])
    
    df11.insert(1, 'Longitude', df['Longitude'][0:961])
    grp = df.groupby('Date')
    for i in range(0,len(date_list)):
        day = grp.get_group(int(date_list[i]))
        var = list(day.Rainfall)
        header = list(df11)
        df11.insert(len(header), 'day_'+str('%s'%(i+1)), var)
       
    ############################################################
    out_file_csv = open(csv_file, 'w', newline='')
#    df11.to_csv(out_file_csv, index=False)

    out_file_csv.close()
    
    return df11
########################################################################################
def csv2shp(df, result_dir, year, name):
    result_dir = result_dir + '/Result'
    try:
        os.mkdir(result_dir)
    except:
        pass
    os.chdir(result_dir)
    curr_wd = os.getcwd()

    try:
        os.mkdir('shapefile_'+str(year))
    except:
        pass
    curr_wd = curr_wd + r'/shapefile_' + str(year)

    geometry = [Point(xy) for xy in zip(df.Longitude, df.Latitude)] 
    
    
    # 5 Define coordinate reference system on which to project your resulting shapefile
    crs = {'init': 'epsg:4326'}
    
    # 6 Convert pandas object (containing your csv) to geodataframe object using geopandas
    gdf = GeoDataFrame(df, crs = crs, geometry=geometry)
    
    # 7 Save file to local destination
    output_filename = curr_wd + r'/equation_'+ name + '_' + str(year) + ".shp"
    gdf.to_file(filename= output_filename, driver='ESRI Shapefile')
    print('csv to shp conversion complete for '+name)
