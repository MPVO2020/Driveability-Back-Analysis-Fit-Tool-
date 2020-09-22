#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np
from matplotlib import pyplot as plt


# In[2]:


def eval_error_BE(fullBE, meanID):
    
    #Defining the difference frame
    difft_BE = pd.DataFrame(columns = ['depth','SRD_BE-SRD_ID'])
    
    
    # FOR BE
    # Creating a list of the difference between the BE line and the Interpolated from Driving Record
    diff1_list = []
    # Finding the difference
    for i in fullBE['depth']:
        s1 = fullBE.loc[fullBE['depth']==i]['SRD']
        s0 = meanID.loc[meanID['depth']==i]['SRD']

        #Changing the format to a frame for compat
        s1 = s1.to_frame()
        s0 = s0.to_frame()

        #In case the interpolated from Driv SRD is empty, no diff is calculated
        #In case of interval, some BE have 2 SRD for one location, both are calculated
        if s0.empty:
            continue
        else:
            diffv1 = (s1-s0.iloc[0])['SRD']
            diffi1 = diffv1.tolist()
            [diff1_list.append(item) for item in diffi1]
             
            
    # calculating Mean Squared Error and Root Mean Squared Error for the BE line 
    diffsq1_list = [number**2 for number in diff1_list]
    total = sum(diffsq1_list)
    MSE_BE = total / (len(diff1_list))
    RMSE_BE = np.sqrt(MSE_BE)
#       print('The Mean Squared Error is for BE:', str(MSE_BE),'The Root Mean Squared Error for BE is:', str(RMSE_BE))



    return MSE_BE, RMSE_BE


# In[3]:


def eval_error_BA(fullBA, meanID):

    #Defining the difference frames
    difft_BA = pd.DataFrame(columns = ['depth','SRD_BA-SRD_ID'])
  

    # FOR BA
    # Creating a list of the difference between the BA line and the Interpolated from Driving Record
    diff2_list = []
    # Finding the difference
    for i in fullBA['depth']:
        s2 = fullBA.loc[fullBA['depth']==i]['SRD']
        s0 = meanID.loc[meanID['depth']==i]['SRD']

        #Changing the format to a frame for compat
        s2 = s2.to_frame()
        s0 = s0.to_frame()

        #In case the interpolated from Driv SRD is empty, no diff is calculated
        #In case of interval, some BE have 2 SRD for one location, both are calculated
        if s0.empty:
            continue
        else:
            diffv2 = (s2-s0.iloc[0])['SRD']
            diffi2 = diffv2.tolist()
            [diff2_list.append(item) for item in diffi2]



    # calculating Mean Squared Error and Root Mean Squared Error for the BA line 
    diffsq2_list = [number**2 for number in diff2_list]
    total = sum(diffsq2_list)
    MSE_BA = total / (len(diff2_list))
    RMSE_BA = np.sqrt(MSE_BA)
#   print('The Mean Squared Error for BA is:', str(MSE_BA),'The Root Mean Squared Error for BA is:', str(RMSE_BA))

    return  MSE_BA, RMSE_BA


# In[ ]:




