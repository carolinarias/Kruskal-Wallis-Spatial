#!/usr/bin/env python

"""
------------------------------------------------------------------------------------------------------------------
TELECOM DATA PREPROCESSING AND EXPLORATION

File name: exploration.py 
Description: This script makes data exploration for telecom Open data 2013.
Author:Carolina Arias Munoz
Date Created: 30/07/2016
Date Last Modified: 30/07/2016
Python version: 2.7
------------------------------------------------------------------------------------------------------------------
"""
#import sys
import pandas
import numpy
import matplotlib
matplotlib.rcParams['agg.path.chunksize'] = 10000
import matplotlib.pyplot as plt
import glob
matplotlib.style.use('ggplot')

#path for the csv files
log_path = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/scripts/2exploration/'
data_path = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/'
data_path_outliers = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/stats/outliers/'
plots_path = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/stats/fig/'
stats_path = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/stats/'
#path for the normalized csv files
data_path_norm = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/csvnorm/'
data_path_norm_week = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/csvnorm/byweek/'




#strings of paths
data_files = glob.glob(data_path + '*.txt')

##Creating log file
#sys.stdout = open (log_path + 'explorationlog.txt', 'w')

#------------------------------------------TELECOM DATA -----------------------------------------------------  
for data_file in data_files:
    #obtainning just the name of the variable
    varname = data_file[93:110]
    # eliminating '.txt'
    varname = varname.replace('.txt', '')
    #variables.append(varname)
    with open(data_file, 'rb') as data_file:
        #Importing data
        df = pandas.read_table(data_file, sep='\t', names=['date_time','cellid', varname]) 
        # Setting date_time as data frame index
        df = df.sort_values(by ='date_time', axis=0, ascending=True)
        df = df.reset_index(drop=True) 
        df = df.set_index(['date_time'], drop = False)
        #------------------------------#
        # STATISTICS AND PLOTS
        #------------------------------#
        #some info on the data
#        print 'Some info on ' + varname + ' dataframe'
#        print ''
#        #df.info()
#        print 'Creating time index... it will take a while...'
#        #creating time index
#        df = df.set_index(pandas.DatetimeIndex(df['date_time']))
#        print 'Time index created for ' + varname
#        print ''
        print 'Statitics on ' + varname + ':'
        #calculate statistics
        statistics = df[varname].describe()
        print statistics
#        print ''
#        #saving the statistics in a csv file
#        statistics.to_csv(stats_path + varname + '.csv', sep=',')
#        print 'Plots on ' + varname
#        #simple plot
        mask = (df['date_time'] >= '2013-11-01T00:00:00+0100') & (df['date_time'] < '2013-12-01T00:00:00+0100')
        dfnov = df.loc[mask]
        line = dfnov['sms_outlog'].plot(kind='line', title = varname + ' 2013', figsize = (30,10))
        fig1 = line.get_figure()
        fig1.savefig(plots_path + 'sms_outlog_line.png',dpi=300)
        plt.close(fig1)
        #density plot
#        density = df[varname].plot(kind='density', title = varname + ' 2013. Density Plot')
#        fig2 = density.get_figure()
#        fig2.savefig(plots_path + varname + '_density.png',dpi=300)
#        plt.close(fig2)
#        #histogram
#        histplot = df[varname].plot(kind='hist',title = varname + ' 2013. Histogram') 
#        fig3 = histplot.get_figure()
#        fig3.savefig(plots_path + varname + '_hist.png',dpi=300)
#        plt.close(fig3)
#        #boxplot
#        boxplot = df[varname].plot(kind='box', title = varname + ' 2013. Boxplot')
#        fig4 = boxplot.get_figure()
#        fig4.savefig(plots_path + varname + '_boxplot.png',dpi=300)
#        plt.close(fig4)
        #Checking data for an specific location
#        cellid = 5999
#        dfcell = df[(df.cellid == cellid)]        
#        line = dfcell[varname].plot(kind='line', title = varname + ''+ ' cellid' +' 2013', figsize = (40,20))
#        fig1 = line.get_figure()
#        fig1.savefig(plots_path + varname + '_line.png',dpi=300)
#        plt.close(fig1)
        #print boxplot
        #---------------------------------------------------#
        # Cheking OUTLIERS
        #---------------------------------------------------#
        #standard deviaton of data
        std = df[varname].std()
        #Interquartile range
        iqr = 1.35 * std
        #25% quartile
        q1 = statistics.ix['25%']
        #75% quartile
        q3 = statistics.ix['75%']
        #superior outer fence limit
        sup_out_lim = q3 + (25 * iqr)
        mask = df[varname] >= sup_out_lim 
        df_so = df.loc[mask]
        df_so.to_csv(path_or_buf = data_path_outliers + varname + 'so.csv', sep=',', index = False)
        #------------------------------#
        # NORMALIZING DATA
        #------------------------------# 
        print 'Normalizing data for ' + varname  + '...'       
        #setting values cero to 0.1: log (0) = undefined
        df = df.replace(0, 0.1)
        #df = df.replace(0, numpy.nan)
        #Transforming data into log 
        df[varname + 'log'] = df[varname].apply(lambda x: numpy.log(x))
        #Cheking normality
#        histplot = df[varname + 'log'].plot(kind='hist',logy=False, title = varname + ' 2013 Normalized [log(x)]. Histogram')
#        fig5 = histplot.get_figure()
#        fig5.savefig(plots_path + varname + '_histlogx.png') 
#        plt.close(fig5)
        df.info()
        boxout = df[varname + 'log'].plot(kind='box',logy=False, title = varname + ' 2013 Normalized [log(x)] Boxplot')
        fig6 = boxout.get_figure()
        fig6.savefig(plots_path + varname + '_boxplotlogx.png',dpi=300) 
        plt.close(fig6)

        #---------------------------------------------------#
        # Cheking OUTLIERS on normalized data
        #---------------------------------------------------#
        print 'Checking outliers for ' + varname + '...'
        statslog = df[varname + 'log'].describe()
        print statslog
        #saving the statistics in a csv file
#        statslog.to_csv(stats_path + varname + 'log.csv', sep=',')
        #standard deviaton of data
        std = df[varname + 'log'].std()
        #Interquartile range
        iqr = 1.35 * std
        #25% quartile
        q1 = statslog.ix['25%']
        #75% quartile
        q3 = statslog.ix['75%']
        #inferior outer fence limit
        inf_out_lim = q1 - (3 * iqr)
        #superior outer fence limit
        sup_out_lim = q3 + (3 * iqr)
        #detecting mayor outliers
        df['i_outliers'] = df[varname + 'log'].apply(lambda x: 'inf_major_outlier' if x<inf_out_lim else 'NO') #inferior outliers
        df['s_outliers'] = df[varname + 'log'].apply(lambda x: 'sup_major_outlier' if x>sup_out_lim else 'NO') #superior outliers
        print ''        
        print 'Interquartile range:' 
        print iqr
        print '25% quartile: '
        print q1
        print '75% quartile: '
        print q3
        print 'inferior outer fence limit: '
        print inf_out_lim
        print 'superior outer fence limit: '
        print sup_out_lim
        print ''        
        #pivot table to count the number of ouliers
        print 'Pivot table to count the number of ouliers'
        print ''
        pivot = pandas.pivot_table(df, values=varname + 'log', columns=['i_outliers', 's_outliers'], aggfunc=numpy.count_nonzero)
        print pivot  
        print ''
        df.drop(['i_outliers','s_outliers'],inplace=True,axis=1) 
        #create a new dataset without the outliers
        df[varname + 'nout'] = df[varname + 'log'].apply(lambda x: numpy.nan if x<inf_out_lim else x)
        df[varname + 'nout'] = df[varname + 'nout'].apply(lambda x: numpy.nan if x>sup_out_lim else x)
        #------------------------------------------------#
        # CHECKING OUTLIERS BEHAVIOUR on normalized data
        #------------------------------------------------# 
        # superior outliers       
        mask = df[varname +'log'] >= sup_out_lim 
        df_so = df.loc[mask]
        df_so.to_csv(path_or_buf = data_path_outliers + varname + 'solog.csv', sep=',', index = False)
        # inferior outliers       
        mask = df[varname +'log'] <= inf_out_lim
        df_info = df.loc[mask]
        df_info.to_csv(path_or_buf = data_path_outliers + varname + 'infolog.csv', sep=',', index = False)
        #check the new dataset
        print 'Some info on the new normalized, no outlier dataset of ' + varname
        print ''
        df.info()
        histout = df[varname + 'nout'].plot(kind='hist',logy=False, title = varname + ' 2013 Normalized [log(x)] and no outliers. Histogram')
        fig6 = histout.get_figure()
        fig6.savefig(plots_path + varname + '_histoutlogx.png',dpi=300)
        plt.close(fig6)
        boxout = df[varname + 'nout'].plot(kind='box',logy=False, title = varname + ' 2013 Normalized [log(x)] and no outliers')
        fig7 = boxout.get_figure()
        fig7.savefig(plots_path + varname + '_lboxplotoutlogx.png',dpi=300) 
        plt.close(fig7)
        #saving file into a csv  
        df.to_csv(path_or_buf = data_path_norm + varname + '.csv', sep=',', index = False)    
        #------------------------------#
        # DIVIDING DATA BY WEEK
        #------------------------------# 
#        # 1 - 3 NOV
#        mask = (df['date_time'] >= '2013-11-01T00:00:00+0100') & (df['date_time'] < '2013-11-04T00:00:00+0100')
#        sdf1 = df.loc[mask]
#        sdf1.to_csv(path_or_buf = data_path_norm_week + '1_3nov' + varname + '.csv', sep=',', index = False)       
#       # 4 - 10 NOV 
#        mask = (df['date_time'] >= '2013-11-04T00:00:00+0100') & (df['date_time'] < '2013-11-10T00:00:00+0100')
#        sdf2 = df.loc[mask]
#        sdf2.to_csv(path_or_buf = data_path_norm_week + '4_10nov' + varname + '.csv', sep=',', index = False)
#        # 11 - 17 NOV
#        mask = (df['date_time'] >= '2013-11-11T00:00:00+0100') & (df['date_time'] < '2013-11-18T00:00:00+0100')
#        sdf3 = df.loc[mask]
#        sdf3.to_csv(path_or_buf = data_path_norm_week + '11_17nov' + varname + '.csv', sep=',', index = False)
#        # 18 - 24 NOV
#        mask = (df['date_time'] >= '2013-11-18T00:00:00+0100') & (df['date_time'] < '2013-11-25T00:00:00+0100')
#        sdf4 = df.loc[mask]
#        sdf4.to_csv(path_or_buf = data_path_norm_week + '18_24nov' + varname + '.csv', sep=',', index = False)
#        # 25 - 1 DIC
#        mask = (df['date_time'] >= '2013-11-25T00:00:00+0100') & (df['date_time'] < '2013-12-02T00:00:00+0100')
#        sdf5 = df.loc[mask]
#        sdf5.to_csv(path_or_buf = data_path_norm_week + '25_1dic' + varname + '.csv', sep=',', index = False)
#        # 2 - 8 DIC
#        mask = (df['date_time'] >= '2013-12-02T00:00:00+0100') & (df['date_time'] < '2013-12-09T00:00:00+0100')
#        sdf6 = df.loc[mask]
#        sdf6.to_csv(path_or_buf = data_path_norm_week + '2_8dic' + varname + '.csv', sep=',', index = False)
#        # 9 - 15 DIC
#        mask = (df['date_time'] >= '2013-12-09T00:00:00+0100') & (df['date_time'] < '2013-12-16T00:00:00+0100')
#        sdf7 = df.loc[mask]
#        sdf7.to_csv(path_or_buf = data_path_norm_week + '9_15dic' + varname + '.csv', sep=',', index = False)
#        # 16 - 22 DIC
#        mask = (df['date_time'] >= '2013-12-16T00:00:00+0100') & (df['date_time'] < '2013-12-23T00:00:00+0100')
#        sdf8 = df.loc[mask]
#        sdf8.to_csv(path_or_buf = data_path_norm_week + '16_22dic' + varname + '.csv', sep=',', index = False)     
#        # 23 - 29 DIC
#        mask = (df['date_time'] >= '2013-12-23T00:00:00+0100') & (df['date_time'] < '2013-12-30T00:00:00+0100')
#        sdf9 = df.loc[mask]
#        sdf9.to_csv(path_or_buf = data_path_norm_week + '23_29dic' + varname + '.csv', sep=',', index = False) 
#        # 30 - 31 DIC
#        mask = (df['date_time'] >= '2013-12-30T00:00:00+0100') & (df['date_time'] < '2014-01-01T00:00:00+0100')
#        sdf10 = df.loc[mask]
#        sdf10.to_csv(path_or_buf = data_path_norm_week + '30_31dic' + varname + '.csv', sep=',', index = False) 
#        print ' '
        print '__________________________________________'
        print ' '
        print ' '
        print '__________________________________________'
        print ' '

#------------------------------------------ARPA DATA -----------------------------------------------------  

#sys.stdout.close()
print 'enjoy! bye'
