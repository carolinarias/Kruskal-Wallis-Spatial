# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
------------------------------------------------------------------------------------------------------------------
ASCII GRID TO ARRAY

File name: asciitotable.py
Description: This is a simple python script to change an ESRI ascii into a csv table
Author:Carolina Arias Munoz
Date Created: 25/08/2016 ‎
Python version: 2.7
------------------------------------------------------------------------------------------------------------------
"""

import numpy as np
import glob
import pandas as pd
from osgeo import gdal

sid =  np.linspace(1, 10000, num = 10000, endpoint=True, retstep=False, dtype=int)

data_path = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/OI_precipitazione_nov_dic_2013/gtiff/'
data_path_out = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/OI_precipitazione_nov_dic_2013/csv/'
#data_path_out = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/OI_precipitazione_nov_dic_2013/csv2/'

data_path_merge = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/csv/'
#data_path_merge = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/OI_precipitazione_nov_dic_2013/csv2/'

data_files = glob.glob(data_path + '*.tif')

for data_file in data_files:
    ts = data_file[108:118]
    date_time = ''.join([ts[0:4],'-',ts[4:6],'-', ts[6:8], 'T', ts[8:10], ':00:00+0100'])
    grid = gdal.Open(data_file)    
    #grid = gdal.Open('/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/OI_precipitazione_nov_dic_2013/gtiff/PR_2013111505UTCplus1.tif')
    array = np.array(grid.GetRasterBand(1).ReadAsArray())    
    arrayt = array.T
    arrayflip = np.fliplr(arrayt)
    datavector= np.ravel(arrayflip, order='K')
    df = pd.DataFrame()
    df['sid'] = sid
    df['date_time'] = date_time
    #df.drop(['sid'],inplace=True,axis=1)
    df['rain']= datavector
    df = df[['date_time', 'sid', 'rain']]
    df.to_csv(path_or_buf = data_path_out + ts + '.csv', sep ='\t',index = False, header = False, columns = ['date_time', 'sid', 'rain'])

# merging all created txt into one txt 
data_files_out = glob.glob(data_path_out + '*.csv')
with open(data_path_merge + 'rain.csv', 'a') as out_file:
    line_num = 0
    for csv_file in data_files_out:
        for line in open(csv_file, 'r'):
            if line is '':
                print 'Skipping line'                   
            else:
                out_file.write(line)  
            line_num = line_num + 1
            print line_num
    #file_num = file_num +1
    #print file_num

print 'enjoy! bye'




