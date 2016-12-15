"""
------------------------------------------------------------------------------------------------------------------
WEATHER  AND TELECOM DATA PREPROCESSING

File name: pre_kw.py
Description: This script prepares the data for kruskal wallis.
Author:Carolina Arias Munoz
Date Created: 30/07/2016
Date Last Modified: 30/07/2016
Python version: 2.7
------------------------------------------------------------------------------------------------------------------
"""
import glob
import pandas


#data_path_norm: where you have your normalized data
data_path_norm = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/csvnorm/'
data_path_rain = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/csv/'
data_path_landuse = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/dusaf/'
data_path_out = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/4anova/'
data_path_out_week = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/4anova/byweek/'

#importing landuse data
landuse = pandas.read_csv(data_path_landuse + 'cellid_dusaf.csv', names=['cellid','level1', 'level2','level3', 'level4','level5'], sep = ',', header=0 )
landuse = landuse.set_index('cellid')
landuse = landuse.drop(['level1','level3', 'level4','level5'], axis = 1)
#Filtering by land use level2 
lutypes_l1 = [11,12,13,14,21,22,23,31,32,41,51]
landuse = landuse.loc[landuse['level2'].isin(lutypes_l1)]
landuse['lulevel2'] = landuse['level2'].apply(lambda x: 'lu11' if x == 11 else x)
landuse['lulevel2'] = landuse['lulevel2'].apply(lambda x: 'lu12' if x == 12 else x)
landuse['lulevel2'] = landuse['lulevel2'].apply(lambda x: 'lu13' if x == 13 else x)
landuse['lulevel2'] = landuse['lulevel2'].apply(lambda x: 'lu14' if x == 14 else x)
landuse['lulevel2'] = landuse['lulevel2'].apply(lambda x: 'lu21' if x == 21 else x)
landuse['lulevel2'] = landuse['lulevel2'].apply(lambda x: 'lu22' if x == 22 else x)
landuse['lulevel2'] = landuse['lulevel2'].apply(lambda x: 'lu23' if x == 23 else x)
landuse['lulevel2'] = landuse['lulevel2'].apply(lambda x: 'lu31' if x == 31 else x)
landuse['lulevel2'] = landuse['lulevel2'].apply(lambda x: 'lu32' if x == 32 else x)
landuse['lulevel2'] = landuse['lulevel2'].apply(lambda x: 'lu41' if x == 41 else x)
landuse['lulevel2'] = landuse['lulevel2'].apply(lambda x: 'lu51' if x == 51 else x)
landuse.head(10)

#importing rain data
rain = pandas.read_table(data_path_rain + 'rain.csv', sep='\t', names=['date_time','cellid', 'rain'])
#organizing the dataframe
rain = rain.sort_values(by =['cellid','date_time'], axis=0, ascending=True)
rain = rain.set_index(['cellid'], drop = False)
rainmean = pandas.pivot_table(rain, values='rain', columns=['cellid'], aggfunc='mean')
rainmax = pandas.pivot_table(rain, values='rain', columns=['cellid'], aggfunc='max')
rainmean.to_csv(data_path_rain + 'rainmean.csv', sep=',',index=True)
rainmax.to_csv(data_path_rain + 'rainmax.csv', sep=',',index=True)
pandas.pivot_table(rain, values='rain', columns=['cellid'], aggfunc='count')


#Some info on rain
#rain['rain'].describe()
#count    1.411000e+07
#mean     1.225480e-01
#std      5.194279e-01
#min      0.000000e+00
#25%      0.000000e+00
#50%      0.000000e+00
#75%      0.000000e+00
#max      1.826593e+01
#Name: rain, dtype: float64
#---------------------------------------------------#
# CREATING RAIN RANGES : slight, moderate, heavy
#---------------------------------------------------#
#Creating ranges
rain['r_levels'] = rain['rain'].apply(lambda x: 'no_rain' if x == 0 else x)
rain['r_levels'] = rain['r_levels'].apply(lambda x: 'slight' if 0<x<2.6 else x)
rain['r_levels'] = rain['r_levels'].apply(lambda x: 'moderate' if 2.6<=x<7.6 else x)
rain['r_levels'] = rain['r_levels'].apply(lambda x: 'heavy' if 7.6<=x<=100 else x)


#pandas.pivot_table(rain, values='rain', columns=['r_levels'], aggfunc=numpy.count_nonzero)
a.plot.bar()
a = pandas.pivot_table(rain, values='rain', columns=['cellid','r_levels'], aggfunc='count')
a.to_csv(data_path_rain + 'pivotrain.csv', sep=',',index=True)

b = pandas.pivot_table(rain, values='rain', columns=['r_levels'], aggfunc='mean')
b.to_csv(data_path_rain + 'pivotrain.csv', sep=',',index=True)

pandas.pivot_table(rain, values='rain', columns=['r_levels'], aggfunc='count')
#r_levels
#heavy           4928
#moderate      140570
#no_rain     11605373
#slight       2889129
#Name: rain, dtype: int64

rain = rain.sort_values(by =['cellid','date_time'], axis=0, ascending=True)
rain = rain.set_index(['cellid','date_time'], drop = False)
#rain = rain.reset_index(drop=True)

#---------------------------------------------------#
# CHECKING OUTLIERS WITH RESPECT TO RAIN DATA 
#---------------------------------------------------#
#cellid	Date	Max value
#6064	16 December 2013, 10:00	2014,73 Incoming calls 
#6064	16 December 2013, 9:00	2593,10 Outgoing calls
#5059	23 December 2013, 15:00	1753,81 Incoming calls 
#5059	23 December 2013, 11:00	2065,26 Outgoing calls
#5059	31 December 2013, 23:00	2163,85 Outgoing calls
#5059	23 December 2013, 23:00	6283,78 Incoming sms
#5059	31 December 2013, 23:00	3834,38 Outgoing sms
#5161	7 December 2013, 15:00	2093,45 Incoming calls 
#5161	7 December 2013, 16:00	2244,25 Outgoing calls
#5161	1 December 2013, 15:00	40252,5 Internet traffic
#5161	1 December 2013, 16:00	37046,81 Internet traffic
#5161	30 November 2013, 16:00	35350,90 Internet traffic
#5160	31 December 2013, 23:00	4268,76 Incoming sms
#4874	19 November 2013, 17:00	2269,72 Outgoing sms
#4874	27 November 2013, 7:00	3595,38 Outgoing sms

#
#o1 = rain.loc[6064,'2013-12-16T10:00:00+0100']
#print o1
#o1 = rain.loc[6064,'2013-12-16T09:00:00+0100']
#print o1
#o1 = rain.loc[5059,'2013-12-23T15:00:00+0100']
#print o1
#o1 = rain.loc[5059,'2013-12-23T11:00:00+0100']
#print o1
#o1 = rain.loc[5059,'2013-12-31T23:00:00+0100']
#print o1
#o1 = rain.loc[5059,'2013-12-23T23:00:00+0100']
#print o1
#o1 = rain.loc[5161,'2013-12-07T15:00:00+0100']
#print o1
#o1 = rain.loc[5161,'2013-12-07T16:00:00+0100']
#print o1
#o1 = rain.loc[5161,'2013-12-01T15:00:00+0100']
#print o1
#o1 = rain.loc[5161,'2013-12-01T16:00:00+0100']
#print o1
#o1 = rain.loc[5161,'2013-12-30T16:00:00+0100']
#print o1
#o1 = rain.loc[5160,'2013-12-31T23:00:00+0100']
#print o1
#o1 = rain.loc[4874,'2013-11-19T17:00:00+0100']
#print o1
#o1 = rain.loc[4874,'2013-11-27T07:00:00+0100']
#print o1

#---------------------------------------------------#
# PREPARING DATA FOR ANOVA
#---------------------------------------------------#

data_files = glob.glob(data_path_norm + '*.csv')

for data_file in data_files:
    #obtainning just the name of the variable
    varname = data_file[101:120]
    # eliminating '.txt'
    varname = varname.replace('.csv', '')
    #variables.append(varname)
    with open(data_file, 'rb') as data_file:
        #Importing data
        df = pandas.read_table(data_file, sep=',', names=['date_time','cellid', varname, varname + 'log', varname + 'nout'], header = 0) #log: variable with Ln; nout: variable with Ln and no outliers
        # Setting date_time as data frame index
        df = df.sort_values(by =['cellid','date_time'], axis=0, ascending=True)
        df = df.set_index(['cellid','date_time'], drop = False)
        #df = df.reset_index(drop=True) 
        #---------------------------------------------------#
        # CREATING TYPE OF DAYS CATEGORY : weekend, workdays
        #---------------------------------------------------#
        df['date_time'] = pandas.to_datetime(df['date_time'])
        #creating a column with codes of weekdays workday = [0,1,2,3,4]; weekends = [5,6]
        df['weekday'] = pandas.DatetimeIndex(df['date_time']).weekday
        #Creating categories
        df['d_type'] = df['weekday'].apply(lambda x: 'weekend' if x == 5 or x==6 else 'workdays')
        df['day_week'] = df['weekday'].apply(lambda x: 'monday' if x == 0 else x)
        df['day_week'] = df['day_week'].apply(lambda x: 'tuesday' if x == 1 else x)
        df['day_week'] = df['day_week'].apply(lambda x: 'wednesday' if x == 2 else x)
        df['day_week'] = df['day_week'].apply(lambda x: 'thursday' if x == 3 else x)
        df['day_week'] = df['day_week'].apply(lambda x: 'friday' if x == 4 else x)
        df['day_week'] = df['day_week'].apply(lambda x: 'saturday' if x == 5 else x)
        df['day_week'] = df['day_week'].apply(lambda x: 'sunday' if x == 6 else x)
        #eliminating unnecessary columns
        #df.drop(['weekday'],inplace=True,axis=1)
        pandas.pivot_table(df, values= varname +'log', columns=['d_type', 'day_week'], aggfunc='count')
        #---------------------------------------------------#
        # CREATING LANDUSE CATEGORIES
        #---------------------------------------------------#
        #Adding landuse data
        df['lu_type'] = df.cellid.map(landuse['lulevel2'])
#        lutypes_l1 = ['lu11','lu12','lu13','lu14']
#        df = df.loc[df['lu_type'].isin(lutypes_l1)]
        # Showing firt 10 rows
        df.head(n=10)
        df.tail(n=10)
        #---------------------------------------------------#
        # MERGING telecom data and rain data
        #---------------------------------------------------#
        #eliminating unnecessary columns
        #df.drop([varname],inplace=True,axis=1)
        #setting indexes for merging        
        df.index.levels[0].name = 'dfcellid'
        df.index.levels[1].name = 'dfdate_time'
        
        df = pandas.merge(df, rain, right_on = ['cellid','date_time'], how = 'inner', left_index=True)
             
        # Showing firt 10 rows
        df.head(n=10)
        df.tail(n=10)
        #use a pivot table to check everthing is ok
        pandas.pivot_table(df, values= varname +'log', columns=['d_type', 'lu_type', 'r_levels'], aggfunc='count')
        #eliminating unnecessary columns
        df.drop(['cellid_y', 'date_time_y', 'cellid_x', 'date_time_x','rain'], inplace=True, axis=1) 
        #save data into a csv
        df.to_csv(path_or_buf = data_path_out + varname + '_anova.csv', sep=',',index=False)
        #------------------------------#
        # TAKING A RANDOM SAMPLE (20% PIXELS)
        #------------------------------# 
        sdf1 = df.sample(frac=0.2, replace=True)
        sdf1.to_csv(path_or_buf = data_path_out + varname + '_anovarandom.csv', sep=',',index=False) 
        #------------------------------#
        # DIVIDING DATA BY WEEK
        #------------------------------# 
        df = df.sort_values(by =['cellid','date_time'], axis=0, ascending=True)
        df = df.set_index(['date_time'], drop = False)
        # 1 - 3 NOV
        mask = (df['date_time'] >= '2013-11-01T00:00:00+0100') & (df['date_time'] < '2013-11-04T00:00:00+0100')
        sdf1 = df.loc[mask]
        sdf1.to_csv(path_or_buf = data_path_out_week + '1_3nov' + varname + '.csv', sep=',', index = False)       
       # 4 - 10 NOV 
        mask = (df['date_time'] >= '2013-11-04T00:00:00+0100') & (df['date_time'] < '2013-11-10T00:00:00+0100')
        sdf2 = df.loc[mask]
        sdf2.to_csv(path_or_buf = data_path_out_week + '4_10nov' + varname + '.csv', sep=',', index = False)
        # 11 - 17 NOV
        mask = (df['date_time'] >= '2013-11-11T00:00:00+0100') & (df['date_time'] < '2013-11-18T00:00:00+0100')
        sdf3 = df.loc[mask]
        sdf3.to_csv(path_or_buf = data_path_out_week + '11_17nov' + varname + '.csv', sep=',', index = False)
        # 18 - 24 NOV
        mask = (df['date_time'] >= '2013-11-18T00:00:00+0100') & (df['date_time'] < '2013-11-25T00:00:00+0100')
        sdf4 = df.loc[mask]
        sdf4.to_csv(path_or_buf = data_path_out_week + '18_24nov' + varname + '.csv', sep=',', index = False)
        # 25 - 1 DIC
        mask = (df['date_time'] >= '2013-11-25T00:00:00+0100') & (df['date_time'] < '2013-12-02T00:00:00+0100')
        sdf5 = df.loc[mask]
        sdf5.to_csv(path_or_buf = data_path_out_week + '25_1dic' + varname + '.csv', sep=',', index = False)
        # 2 - 8 DIC
        mask = (df['date_time'] >= '2013-12-02T00:00:00+0100') & (df['date_time'] < '2013-12-09T00:00:00+0100')
        sdf6 = df.loc[mask]
        sdf6.to_csv(path_or_buf = data_path_out_week + '2_8dic' + varname + '.csv', sep=',', index = False)
        # 9 - 15 DIC
        mask = (df['date_time'] >= '2013-12-09T00:00:00+0100') & (df['date_time'] < '2013-12-16T00:00:00+0100')
        sdf7 = df.loc[mask]
        sdf7.to_csv(path_or_buf = data_path_out_week + '9_15dic' + varname + '.csv', sep=',', index = False)
        # 16 - 22 DIC
        mask = (df['date_time'] >= '2013-12-16T00:00:00+0100') & (df['date_time'] < '2013-12-23T00:00:00+0100')
        sdf8 = df.loc[mask]
        sdf8.to_csv(path_or_buf = data_path_out_week + '16_22dic' + varname + '.csv', sep=',', index = False)     
        # 23 - 29 DIC
        mask = (df['date_time'] >= '2013-12-23T00:00:00+0100') & (df['date_time'] < '2013-12-30T00:00:00+0100')
        sdf9 = df.loc[mask]
        sdf9.to_csv(path_or_buf = data_path_out_week + '23_29dic' + varname + '.csv', sep=',', index = False) 
        # 30 - 31 DIC
        mask = (df['date_time'] >= '2013-12-30T00:00:00+0100') & (df['date_time'] < '2014-01-01T00:00:00+0100')
        sdf10 = df.loc[mask]
        sdf10.to_csv(path_or_buf = data_path_out_week + '30_31dic' + varname + '.csv', sep=',', index = False) 
        print ' '

print 'enjoy! bye'
