"""
------------------------------------------------------------------------------------------------------------------
KRUSKAL-WALLIS TEST
File name: krustall_wallismap.py
Description: This script prepares the data fro the anova analisis in R.
Author:Carolina Arias Munoz
Date Created: 30/07/2016
Date Last Modified: 30/07/2016
Python version: 2.7
------------------------------------------------------------------------------------------------------------------
"""
import glob
import pandas
import scipy
import numpy as np
from scipy import stats
import csv


#data_path_norm: where you have your normalized data
data_path = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/4anova/'
data_path_out = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/4anova/kruskal/'



#---------------------------------------------------#
#  ANALISYS BY RAIN LEVELS
#---------------------------------------------------#
data_files = glob.glob(data_path + '*.csv')

for data_file in data_files:
    #obtainning just the name of the variable
    varname = data_file[100:120]
    # eliminating '.txt'
    varname = varname.replace('_anova.csv', '')
    #variables.append(varname)
    with open(data_file, 'rb') as data_file:
        #Importing data
        df = pandas.read_table(data_file, sep=',') 
        df.drop([ varname +'nout', varname +'log','d_type', 'weekday', 'lu_type'],inplace=True,axis=1)      
        #creating a dataframe for each cell
        cellid = np.linspace(1, 10000, num = 10000, endpoint=True, retstep=False, dtype=int)     
        
        d = {}     
        dheavy = {}
        dnorain = {}
        dmod = {}
        dslight = {}
        dkruskal = {}
        dpvalues = {}
        dstat = {}
        dnorainmed = {}
        dmodmed = {}
        dslightmed = {}
        count_passed = 0
        count_failed = 0
        count_suitable = 0
        count_nan = 0        
        
        for i in cellid:
            d[i] = df[(df.cellid == i)]
            dheavy[i] = d[i][(d[i].r_levels == 'heavy')]  
            dnorain[i] = d[i][(d[i].r_levels == 'no_rain')] 
            dmod[i] = d[i][(d[i].r_levels == 'moderate')] 
            dslight[i] = d[i][(d[i].r_levels == 'slight')] 
            check_dnorain = len(set(dnorain[i][varname])) > 1
            check_dmod = len(set(dmod[i][varname])) > 1
            check_dmod2 = len(dmod[i][varname]) >= 5
            check_dslight = len(set(dslight[i][varname])) > 1
            if check_dnorain and check_dmod2 and check_dmod and check_dslight:
                count_suitable = count_suitable + 1     
                kruskallwallis_result = scipy.stats.mstats.kruskalwallis(dnorain[i][varname],dmod[i][varname],dslight[i][varname])
                if kruskallwallis_result[1] > 0.05:
                    # pvalue is greater than 0.05
                    # test didn't pass
                    dkruskal[i] = 0
                    dpvalues[i]= np.nan
                    count_failed = count_failed + 1
                else:
                    # pvalue is less or equal than 0.05
                    # test passed!
                    dkruskal[i] = 1
                    dpvalues[i]= kruskallwallis_result[1]
                    dstat[i]= kruskallwallis_result[0]
                    dnorainmed[i]= np.median(dnorain[i][varname].values)
                    dmodmed[i]= np.median(dmod[i][varname].values)
                    dslightmed[i]= np.median(dslight[i][varname].values)
                    count_passed = count_passed + 1 
                print 'Test executed'                           
            else :
                count_nan = count_nan + 1 
                dkruskal[i] = np.nan
                dpvalues[i]= np.nan
                                
                print('Checks on index %d failed: dnorain:%s dmod:%s dmod2:%s dslight:%s. Skipping' % (i, check_dnorain, check_dmod, check_dmod2, check_dslight) )
        print ''
        print varname
        print ''  
        print('Suitable: %d' % count_suitable)
        print('Passed: %d' % count_passed)  
        print('Failed: %d' % count_failed)        
        print('cells with gropus with equal values or mod>=5 : %d' % count_nan)  
        
        dmed = dnorainmed,dmodmed,dslightmed,dkruskal,dpvalues,dstat
        with open(data_path_out + varname + '_rainmode.csv', 'wb') as ofile:
            writer = csv.writer(ofile, delimiter='\t')
            writer.writerow(['ID', 'norainmed', 'modmed', 'slightmed', 'kruskal','pvalue','H'])
            for key in dmodmed.iterkeys():
                writer.writerow([key] + [dic[key] for dic in dmed]) 
        
                
#        with open(data_path_out + varname + '_kruskal_rain.csv','wb') as f:
#            w = csv.writer(f)
#            w.writerows(dkruskal.items())     
#        
#        with open(data_path_out + varname + '_kruskal_rainpval.csv','wb') as f:
#            w = csv.writer(f)
#            w.writerows(dpvalues.items())
          
#---------------------------------------------------#
#  ANALISYS BY DAY OF THE WEEK
#---------------------------------------------------#
for data_file in data_files:
    #obtainning just the name of the variable
    varname = data_file[100:120]
    # eliminating '.txt'
    varname = varname.replace('_anova.csv', '')
    #variables.append(varname)
    with open(data_file, 'rb') as data_file:
        #Importing data
        df = pandas.read_table(data_file, sep=',') 
        df.drop([ varname +'nout', varname +'log','d_type', 'weekday', 'lu_type'],inplace=True,axis=1)
        #creating a dataframe for each cell
        cellid = np.linspace(1, 10000, num = 10000, endpoint=True, retstep=False, dtype=int)     
        
        d = {}     
        dmon = {}
        dtue = {}
        dwed = {}
        dthu = {}
        dfri = {}
        dsat = {}
        dsun = {}
        dmonmed = {}
        dtuemed = {}
        dwedmed = {}
        dthumed = {}
        dfrimed = {}
        dsatmed = {}
        dsunmed = {}       
        dkruskal = {}
        dpvalues = {}
        dstat = {}
        count_passed = 0
        count_failed = 0
        count_nan = 0        
        
        for i in cellid:
            d[i] = df[(df.cellid == i)]
            dmon[i] = d[i][(d[i].day_week == 'monday')]  
            dtue[i] = d[i][(d[i].day_week == 'tuesday')] 
            dwed[i] = d[i][(d[i].day_week == 'wednesday')] 
            dthu[i] = d[i][(d[i].day_week == 'thursday')]
            dfri[i] = d[i][(d[i].day_week == 'friday')]
            dsat[i] = d[i][(d[i].day_week == 'saturday')]
            dsun[i] = d[i][(d[i].day_week == 'sunday')]
            check_dmon = len(set(dmon[i][varname])) > 1
            check_dtue = len(set(dtue[i][varname])) > 1
            check_dwed = len(set(dwed[i][varname])) > 1
            check_dthu = len(set(dthu[i][varname])) > 1  
            check_dfri = len(set(dfri[i][varname])) > 1
            check_dsat = len(set(dsat[i][varname])) > 1
            check_dsun = len(set(dsun[i][varname])) > 1
                                                
            if check_dmon and check_dtue and check_dwed and check_dthu and check_dfri and check_dsat and check_dsun :       
                #groups = (dnorain[i][varname],dheavy[i][varname],dmod[i][varname],dslight[i][varname])]
                #dkruskal[i] = scipy.stats.mstats.kruskalwallis(groups)     
                kruskallwallis_result = scipy.stats.mstats.kruskalwallis(dmon[i][varname],dtue[i][varname],dwed[i][varname],dthu[i][varname],dfri[i][varname],dsat[i][varname],dsun[i][varname])
                if kruskallwallis_result[1] > 0.05:
                    # pvalue is greater than 0.05
                    # test didn't pass
                    dkruskal[i] = 0
                    count_failed = count_failed + 1
                else:
                    # pvalue is less or equal than 0.05
                    # test passed!
                    dkruskal[i] = 1
                    dmonmed[i]= np.median(dmon[i][varname].values)
                    dtuemed[i]= np.median(dtue[i][varname].values)
                    dwedmed[i]= np.median(dwed[i][varname].values)
                    dthumed[i]= np.median(dthu[i][varname].values)
                    dfrimed[i]= np.median(dfri[i][varname].values)
                    dsatmed[i]= np.median(dsat[i][varname].values)
                    dsunmed[i]= np.median(dsun[i][varname].values)
                    dpvalues[i]= kruskallwallis_result[1]
                    dstat[i]= kruskallwallis_result[0]                    
                    count_passed = count_passed + 1
                          
            else : 
                dkruskal[i] = np.nan
                count_nan = count_nan + 1
                print('Checks on index %d failed: dmon:%s dtue:%s dwed:%s dthu:%s dfri%s dsat%s dsun%s. Skipping' % (i, check_dmon, check_dtue, check_dwed, check_dthu, check_dfri, check_dsat, check_dsun ) )
                
        print('Passed: %d' % count_passed)  
        print('Failed: %d' % count_failed) 
        
        dmed = dmonmed,dtuemed,dwedmed,dthumed,dfrimed,dsatmed,dsunmed,dkruskal,dpvalues,dstat
        with open(data_path_out + varname + '_dmode.csv', 'wb') as ofile:
            writer = csv.writer(ofile, delimiter='\t')
            writer.writerow(['ID', 'monmed', 'tuemed', 'wedmed', 'wedmed', 'thumed', 'frimed','satmed','sunmed','kruskal','pvalue','H'])
            for key in dmonmed.iterkeys():
                writer.writerow([key] + [dic[key] for dic in dmed]) 
                
#        with open(data_path_out + varname + '_kruskal_dweek.csv','wb') as f:
#            w = csv.writer(f)
#            w.writerows(dkruskal.items())        


for data_file in data_files:
    #obtainning just the name of the variable
    varname = data_file[100:120]
    # eliminating '.txt'
    varname = varname.replace('_anova.csv', '')
    #variables.append(varname)
    with open(data_file, 'rb') as data_file:
        #Importing data
        df = pandas.read_table(data_file, sep=',') 
        df.drop([ varname +'nout', varname +'log','d_type', 'weekday', 'lu_type'],inplace=True,axis=1)
        #creating a dataframe for each cell
        cellid = np.linspace(1, 10000, num = 10000, endpoint=True, retstep=False, dtype=int)     
        
        d = {}     
#        dmon = {}
#        dtue = {}
#        dwed = {}
        dthu = {}
        dfri = {}
#        dsat = {}
#        dsun = {}
#        dmonmed = {}
#        dtuemed = {}
#        dwedmed = {}
        dthumed = {}
        dfrimed = {}
#        dsatmed = {}
        dsunmed = {}       
        dkruskal = {}
        dpvalues = {}
        dstat = {}
        count_passed = 0
        count_failed = 0
        count_nan = 0        
        
        for i in cellid:
            d[i] = df[(df.cellid == i)]
#            dmon[i] = d[i][(d[i].day_week == 'monday')]  
#            dtue[i] = d[i][(d[i].day_week == 'tuesday')] 
#            dwed[i] = d[i][(d[i].day_week == 'wednesday')] 
            dthu[i] = d[i][(d[i].day_week == 'thursday')]
            dfri[i] = d[i][(d[i].day_week == 'friday')]
#            dsat[i] = d[i][(d[i].day_week == 'saturday')]
#            dsun[i] = d[i][(d[i].day_week == 'sunday')]
#            check_dmon = len(set(dmon[i][varname])) > 1
#            check_dtue = len(set(dtue[i][varname])) > 1
#            check_dwed = len(set(dwed[i][varname])) > 1
            check_dthu = len(set(dthu[i][varname])) > 1  
            check_dfri = len(set(dfri[i][varname])) > 1
#            check_dsat = len(set(dsat[i][varname])) > 1
#            check_dsun = len(set(dsun[i][varname])) > 1
                                                
#            if check_dmon and check_dtue and check_dwed and check_dthu and check_dfri and check_dsat and check_dsun :  
            if check_dthu and check_dfri :  

                #groups = (dnorain[i][varname],dheavy[i][varname],dmod[i][varname],dslight[i][varname])]
                #dkruskal[i] = scipy.stats.mstats.kruskalwallis(groups)     
                #kruskallwallis_result = scipy.stats.mstats.kruskalwallis(dmon[i][varname],dtue[i][varname],dwed[i][varname],dthu[i][varname],dfri[i][varname],dsat[i][varname],dsun[i][varname])
                kruskallwallis_result = scipy.stats.mstats.kruskalwallis(dthu[i][varname],dfri[i][varname])                
                if kruskallwallis_result[1] > 0.05:
                    # pvalue is greater than 0.05
                    # test didn't pass
                    dkruskal[i] = 0
                    count_failed = count_failed + 1
                else:
                    # pvalue is less or equal than 0.05
                    # test passed!
                    dkruskal[i] = 1
#                    dmonmed[i]= np.median(dmon[i][varname].values)
#                    dtuemed[i]= np.median(dtue[i][varname].values)
#                    dwedmed[i]= np.median(dwed[i][varname])
                    dthumed[i]= np.median(dthu[i][varname])
                    dfrimed[i]= np.median(dfri[i][varname])
#                    dsatmed[i]= np.median(dsat[i][varname].values)
#                    dsunmed[i]= np.median(dsun[i][varname].values)
                    dpvalues[i]= kruskallwallis_result[1]
                    dstat[i]= kruskallwallis_result[0]                    
                    count_passed = count_passed + 1

            else : 
                dkruskal[i] = np.nan
                count_nan = count_nan + 1
                print('Checks on index %d failed: dthu:%s dfri%s. Skipping' % (i, check_dthu, check_dfri) )
                
        print('Passed: %d' % count_passed)  
        print('Failed: %d' % count_failed) 
        
#        dmed = dmonmed,dtuemed,dwedmed,dthumed,dfrimed,dsatmed,dsunmed,dkruskal,dpvalues,dstat
#        with open(data_path_out + varname + '_dmode.csv', 'wb') as ofile:
#            writer = csv.writer(ofile, delimiter='\t')
#            writer.writerow(['ID', 'monmed', 'tuemed', 'wedmed', 'thumed', 'frimed','satmed','sunmed','kruskal','pvalue','H'])
#            for key in dmonmed.iterkeys():
#                writer.writerow([key] + [dic[key] for dic in dmed]) 

        dmed = dthumed,dfrimed,dkruskal,dpvalues,dstat
        with open(data_path_out + varname + '_dmode2days.csv', 'wb') as ofile:
            writer = csv.writer(ofile, delimiter='\t')
            writer.writerow(['ID', 'frimed', 'thumed','kruskal','pvalue','H'])
            for key in dthumed.iterkeys():
                writer.writerow([key] + [dic[key] for dic in dmed]) 

print 'enjoy! bye'
