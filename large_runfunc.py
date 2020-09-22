#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np
from matplotlib import pyplot as plt
import scipy.interpolate
from matplotlib import pyplot as plt
from collections import OrderedDict
import xlrd


# In[2]:


def runfunc_ID(df1):
    #Large runfunc that puts Interpolated from Driving record Data (ID) into format 
    #that can be analysed by splitting into 0.05m chunks and linearly interpolating
    #between using the existing values
    
    # 1

    # Parsing for the required data
    interpID = df1.iloc[1:,0:2]
    interpID = interpID.dropna(how='all') 
    interpID.columns = ['depth','SRD']
    # assigining max depth of pile as last depth value from excel + 0.05m
    maxd = (interpID['depth'].iloc[-1]) + 0.05
    # creating a points list and removing all repeated values 
    plist = list(interpID['depth'])
    plist = OrderedDict((p, True) for p in plist).keys()

    # Creating the empty dataframe that requires all inputting
    interpIDfull = pd.DataFrame((np.arange(0,maxd,.05)))
    interpIDfull.insert(1,1,np.NaN)
    interpIDfull.columns = ['depth','SRD']
    #Changing the depth column from loads of dp to just 2
    decimals = 2    
    interpIDfull['depth'] = interpIDfull['depth'].apply(lambda x: round(x, decimals))
    #removing the points which will be present in interpID
    for p in plist:
        idx = (interpIDfull.loc[interpIDfull['depth']==p].index[0])
        interpIDfull = interpIDfull.drop(index=idx)      
        # interpIDfull.head

    # Merging the two: Essentially creating a row for every 0.05m interval to allow for comparison between BE, BA and
    # interpolated from DRIV graphs
    df = pd.concat([interpID,interpIDfull]).sort_values('depth')
    df = df.reset_index(drop=True).drop_duplicates()


    # 2
    #Making list of where the points are (the ones from excel with SRD values)
    a=[]
    for i in range(0,(df.shape[0])):
        #Adding exclusion if = placeholder once the dataframe gets changed later on 
        if pd.notnull(df.iloc[i,1]) and df.iloc[i,1] != -1000:
            a.append(i)


    #Creating list of dataframes
    dfnames = []
    for m in range(0,len(a)):
        name = 'dataf' + str(m)
        dfnames.append(name)
    dfnames.append('dataf' + str(m+1))

    # Making the values in the list into empty dataframes    
    df_list = [pd.DataFrame() for x in dfnames]




    # 3
    #Add one onto the end of the points list for the last point
    a.append((df.shape[0])-1)

    # Filling the list of dataframes with the values between and including points
    k=0
    for j in range(0, (len(a))):
        #using an exception in likely case that it is out of range
        try:
        #     For first frame
            if j==0:
                end = a[j]
                df_list[k] = df.iloc[:end+1, :]
                k+=1
        #     for other frames
            start = a[j]
            end = a[j+1]
            df_list[k] = df.iloc[start:end+1, :]
            k+=1   
        except IndexError:
            k+=1
            continue

    # Replacing all NaN present in SRD to allow for compatability with .loc later
    for l in range(0,len(df_list)):
    #  chosing arbitrary negative number as a fill to be changed later 
        arb = -1000
        df_list[l]['SRD'].fillna(arb, inplace=True)


    #     4

    for q in range(1,(len(df_list)-1)):


        # Taking the first frame and only the depth  and SRD columns
        vals = df_list[q].iloc[:,0:2]
        # Filtering the frame for the points with SRD values
        vals_points = vals[vals['SRD'] != arb]
        # assigning the x and y points to be used for interpolation # NEED TO USE x and y the other way round to work
        y = vals_points['SRD'].astype('float')
        x = vals_points['depth'].astype('float')


        # Interpolating the SRD for the points that are not empty by iterating through their position in individual frame

        # Defining the data to be taken from
        data = df_list[q].iloc[:,0:2]   

        # Setting up the interpolation line\
        x_interp = scipy.interpolate.interp1d(x, y)


        # For any location where the SRD is not known, interpolate using the known locations
        for i in range(0,data.shape[0]):
            if data['SRD'].iloc[i] == arb:
                found_val = x_interp(data['depth'].iloc[i])
                data['SRD'].iloc[i] = found_val

        # assigning the points from data to the original frame
        df_list[q] = data

     #deleting the first dataframes
    del df_list[0]




    # 5

    # Putting all the frames into one huge one
    prev = pd.DataFrame([[np.NaN,np.NaN]])
    prev.columns = ['depth','SRD']

    for j in range(0,len(df_list)):
        full = pd.concat([df_list[j], prev])
        prev = full

    # Dropping the repeated values and dropping the NaN rows and renaming full as fullID    
    fullID = full.sort_values('depth').dropna(how='all').drop_duplicates()

#         print(fullID)

    

    #Clearing all of the mutable objects to ensure no error after looping
    del interpID, plist, interpIDfull, df, a, dfnames, df_list, vals, vals_points, data, full, prev

    return fullID


# In[3]:


def runfunc_BE(df1):
     #Large runfunc that puts Best Estimate data (BE) into format 
    #that can be analysed by splitting into 0.05m chunks and linearly interpolating
    #between using the existing values
    
    #1
    
    interpBE = df1.iloc[1:,2:5]
    interpBE = interpBE.dropna(how='all') 
    interpBE = interpBE.drop(columns='Unnamed: 3')
    interpBE.columns = ['depth','SRD']
    # assigining max depth of pile as last depth value from excel + 0.05m
    maxd = (interpBE['depth'].iloc[-1]) + 0.05
    # creating a points list and removing all repeated values 
    plist = list(interpBE['depth'])
    plist = OrderedDict((p, True) for p in plist).keys()

    # Creating the empty dataframe that requires all inputting
    interpBEfull = pd.DataFrame((np.arange(0,maxd,.05)))
    interpBEfull.insert(1,1,np.NaN)
    interpBEfull.columns = ['depth','SRD']
    #Changing the depth column from loads of dp to just 2
    decimals = 2    
    interpBEfull['depth'] = interpBEfull['depth'].apply(lambda x: round(x, decimals))
    #removing the points which will be present in interpBE
    for p in plist:
        idx = (interpBEfull.loc[interpBEfull['depth']==p].index[0])
        interpBEfull = interpBEfull.drop(index=idx)      
        # interpBEfull.head

    # Merging the two: Essentially creating a row for every 0.05m interval to allow for comparison between BE, BA and
    # interpolated from DRIV graphs
    df = pd.concat([interpBE,interpBEfull]).sort_values('depth')
    df = df.reset_index(drop=True).drop_duplicates()


    #2
    #Making list of where the points are (the ones from excel with SRD values)
    a=[]
    for i in range(0,(df.shape[0])):
        if pd.notnull(df.iloc[i,1]):
            a.append(i)


    #Creating list of dataframes
    dfnames = []
    for m in range(0,len(a)):
        name = 'dataf' + str(m)
        dfnames.append(name)
    dfnames.append('dataf' + str(m+1))

    # Making the values in the list into empty dataframes    
    df_list = [pd.DataFrame() for x in dfnames]


    #3
    #Add one onto the end of the points list for the last point
    a.append((df.shape[0])-1)

    # Filling the list of dataframes with the values between and including points
    k=0
    for j in range(0, (len(a)-1)):
    #     For first frame
        if j==0:
            end = a[j]
            df_list[k] = df.iloc[:end+1, :]
            k+=1
    #     for other frames
        start = a[j]
        end = a[j+1]
        df_list[k] = df.iloc[start:end+1, :]
        k+=1   


    # Replacing all NaN present in SRD to allow for compatability with .loc later
    for l in range(0,len(df_list)):
    #  chosing arbitrary negative number to be changed later 
        arb = -1000
        df_list[l]['SRD'].fillna(arb, inplace=True)



    #4 
    for q in range(1,(len(df_list)-1)):


        # Taking the first frame and only the depth  and SRD columns
        vals = df_list[q].iloc[:,0:2]
        # Filtering the frame for the points with SRD values
        vals_points = vals[vals['SRD'] != arb]
        # assigning the x and y points to be used for interpolation # NEED TO USE x and y the other way round to work
        y = vals_points['SRD'].astype('float')
        x = vals_points['depth'].astype('float')


        # Interpolating the SRD for the points that are not empty by iterating through their position in individual frame

        # Defining the data to be taken from
        data = df_list[q].iloc[:,0:2]   

        # Setting up the interpolation line\
        x_interp = scipy.interpolate.interp1d(x, y)


        # For any location where the SRD is not known, interpolate using the known locations
        for i in range(0,data.shape[0]):
            if data['SRD'].iloc[i] == arb:
                found_val = x_interp(data['depth'].iloc[i])
                data['SRD'].iloc[i] = found_val

        # assigning the points from data to the original frame
        df_list[q] = data

     #deleting the first dataframe
    del df_list[0]


    #5
    # Putting all the frames into one huge one
    prev = pd.DataFrame([[np.NaN,np.NaN]])
    prev.columns = ['depth','SRD']

    for j in range(0,len(df_list)):
        full = pd.concat([df_list[j], prev])
        prev = full

    # Dropping the repeated values and dropping the NaN rows and renaming full as fullBE    
    fullBE = full.sort_values('depth').dropna(how='all').drop_duplicates()



    #Clearing all of the mutable objects to ensure no error after looping
    del interpBE, plist, interpBEfull, df, a, dfnames, df_list, vals, vals_points, data, full, prev

        
        
    return fullBE


# In[4]:


def runfunc_BA(df1):
     #Large runfunc that puts Back Analysis data (BA) into format 
    #that can be analysed by splitting into 0.05m chunks and linearly interpolating
    #between using the existing values
   
    #1
    interpBA = df1.iloc[1:,6:8]
    interpBA = interpBA.dropna(how='all')
    interpBA.columns = ['depth','SRD']
    # assigining to max depth of last depth value from excel + 0.05
    maxd = (interpBA['depth'].iloc[-1]) + 0.05
    # creating a points list and removing all repeated values 
    plist = list(interpBA['depth'])
    plist = OrderedDict((p, True) for p in plist).keys()

    # Creating the empty dataframe that requires all inputting
    interpBAfull = pd.DataFrame((np.arange(0,maxd,.05)))
    interpBAfull.insert(1,1,np.NaN)
    interpBAfull.columns = ['depth','SRD']
    #Changing the depth column from loads of dp to just 2
    decimals = 2    
    interpBAfull['depth'] = interpBAfull['depth'].apply(lambda x: round(x, decimals))
    #removing the points which will be present in interpBA
    for p in plist:
        idx = (interpBAfull.loc[interpBAfull['depth']==p].index[0])
        interpBAfull = interpBAfull.drop(index=idx)      
        # interpBAfull.head

    # Merging the two: Essentially creating a row for every 0.05m interval to allow for comparison between BE, BA and
    # interpolated from DRIV graphs
    df = pd.concat([interpBA,interpBAfull]).sort_values('depth').drop_duplicates()
    df = df.reset_index(drop=True)


    #2
    #Making list of where the points are (the ones from excel with SRD values)
    a=[]
    for i in range(0,(df.shape[0])):
        #When the values is equal to the arbitrary -1000 as defined below as placeholder or is 
        if pd.notnull(df.iloc[i,1]):
            a.append(i)


    #Creating list of dataframes
    dfnames = []
    for m in range(0,len(a)):
        name = 'dataf' + str(m)
        dfnames.append(name)
    dfnames.append('dataf' + str(m+1))

    # Making the values in the list into empty dataframes    
    df_list = [pd.DataFrame() for x in dfnames]


    #3
    #Add one onto the end of the points list for the last point
    a.append((df.shape[0])-1)

    # Filling the list of dataframes with the values between and including points
    k=0
    for j in range(0, (len(a)-1)):

    #     For first frame
        if j==0:
            end = a[j]
            df_list[k] = df.iloc[:end+1, :]
            k+=1
    #     for other frames
        start = a[j]
        end = a[j+1]
        df_list[k] = df.iloc[start:end+1, :]
        k+=1   


    # Replacing all NaN present in SRD to allow for compatability with .loc later
    for l in range(0,len(df_list)):
    #  chosing arbitrary negative number to be changed later 
        arb = -1000
        df_list[l]['SRD'].fillna(arb, inplace=True)


    #4
    for q in range(1,(len(df_list)-1)):


        # Taking the first frame and only the depth  and SRD columns
        vals = df_list[q].iloc[:,0:2]
        # Filtering the frame for the points with SRD values
        vals_points = vals[vals['SRD'] != arb]
        # assigning the x and y points to be used for interpolation # NEED TO USE x and y the other way round to work
        y = vals_points['SRD'].astype('float')
        x = vals_points['depth'].astype('float')


        # Interpolating the SRD for the points that are not empty by iterating through their position in individual frame

        # Defining the data to be taken from
        data = df_list[q].iloc[:,0:2]   

        # Setting up the interpolation line\
        x_interp = scipy.interpolate.interp1d(x, y)


        # For any location where the SRD is not known, interpolate using the known locations
        for i in range(0,data.shape[0]):
            if data['SRD'].iloc[i] == arb:
                found_val = x_interp(data['depth'].iloc[i])
                data['SRD'].iloc[i] = found_val

        # assigning the points from data to the original frame
        df_list[q] = data

     #deleting the first dataframes
    del df_list[0]



    #5
    # Putting all the frames into one huge one
    prev = pd.DataFrame([[np.NaN,np.NaN]])
    prev.columns = ['depth','SRD']

    for j in range(0,len(df_list)):
        full = pd.concat([df_list[j], prev])
        prev = full

    # Dropping the repeated values and dropping the NaN rows and renaming full as fullBA    
    fullBA = full.sort_values('depth').dropna(how='all').drop_duplicates()



    #Clearing all of the mutable objects to ensure no error after looping
    del interpBA, plist, interpBAfull, df, a, dfnames, df_list, vals, vals_points, data, full, prev
        
    return fullBA
        


# In[ ]:





# In[ ]:




