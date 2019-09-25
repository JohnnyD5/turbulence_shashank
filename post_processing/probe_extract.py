# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 10:02:50 2019

@author: zding5
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import time
import scipy
pd.set_option('precision', 6)
pd.set_option('expand_frame_repr', True)

class oneFile():
    def __init__(self, path = None):
        if len(path) < 1:
            path = 'C:/Users/zding5/OneDrive - Louisiana State University/work/turbulence_shashank/post_processing/probes'
        self.path = path
        #Note: if you make changes to original data, please delete U_combined.h5 
        # file first before you run the program
        try:
            self.data = pd.read_hdf(self.path + '/U_combined.h5', key='U')
        except:
            print('Assembling data...')
            df = pd.concat([pd.read_csv(self.path+'/'+folder+'/U',skiprows = 11,
                                sep='\)\s+\(|\s+\(|\s|\)\s\(',engine ='python',names = ["t", "u1", "v1", "w1",
                                           "u2", "v2", "w2", "u3", "v3", "w3", "u4", "v4", "w4",
                                           "u5", "v5", "w5","u6", "v6", "w6","u7", "v7", "w7","u8", 
                                           "v8", "w8","u9", "v9", "w9"]) for folder in os.listdir(self.path) if folder[0].isdigit()], ignore_index=True)
            df['w9'] = df['w9'].str.replace('\)', '').astype(float)
            df['vel']=(df['u1']**2+df['v1']**2+df['w1']**2)**0.5
            df.to_hdf(self.path + '/U_combined.h5',key='U')
            self.data = pd.read_hdf(self.path + '/U_combined.h5', key='U')

    def time_series(self, t = None, y = None):
        start_time = time.time()
        print("Generating the time series plot...")
        # Plot the angular velocity of the ellipse over time
        if t is None:
            t = 't'
        if y is None:
            y = 'u1'
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.plot(self.data[t], self.data[y])
        ax.set_xlabel('Time',fontweight='bold')
        ax.set_ylabel('Dimensionless Velocity',fontweight='bold')
#        #removing top and right borders
#        ax.spines['top'].set_visible(False)
#        ax.spines['right'].set_visible(False)
        # set x limit and y limit
        ax.set_xlim(left = 0, right = 10)
        plt.rcParams["font.family"] = "Times New Roman"  
        plt.show()
        
        end_time = time.time()
        print('running time: '+ str(end_time-start_time)+'s')
        return

    def u_fft(self,y, lb, rb):
        # lb: left boundary of the data you want; type: integer number
        # rb: right boundary of the data you want; type: integer number 
        start_time = time.time()
        if rb > len(self.data):
            rb = len(self.data)
        df = self.data.iloc[lb:rb]
        print('Ploting the fft figure...')
        # initial conditions block, for dimensionless
        dp=0.01
        u_inf=14.607
        # initial conditions block, for dimensionless
        df['t']=(df['t']*u_inf)/dp
        y=abs(df[y])
        deltaT=np.diff(df['t'])[0]
        N = len(y);
        Fs = 1.0/deltaT; # sampling frequency
        freq = np.arange(0,N)*Fs/N
        Y = scipy.fft(y-np.mean(y))
        df['St']=freq
        df['amp']=2.0*N * np.abs(Y)
        df = df.iloc[0:N//2+1] # #this line to take out the mirror effect,

        fig, ax = plt.subplots(figsize=(6, 5))
        ax.loglog(df['St'], df['amp'],color='k') #this will have the mirror effect, abs is to take out the imaginary part
        ax.set_xlabel('St',fontweight='bold')
        ax.set_ylabel('Amplitude',fontweight='bold')
        fig.savefig('fft_re10k__re10k_noslip.tif', dpi=300)
        
        plt.rcParams["font.family"] = "Times New Roman"  
        plt.show()
        
        end_time = time.time()
        print('running time: '+ str(end_time-start_time)+'s')
        return 0
    def test(self):
        start_time = time.time()
        print(self.data)
        end_time = time.time()
        print('running time: '+ str(end_time-start_time)+'s')
        return 0

if __name__ == '__main__':
    path = input("Please identify the path of desired folder; the folder should contain cloud.out file:\n")
    ### convert windows path to linux path
    path = list(path)
    for i, c in enumerate(path):
        if c == '\\':
            path[i] = '/'
    path = ''.join(path)
    ###
    case = oneFile(path)
    case.time_series('t','u1')
    case.u_fft('v2', 10000, 10000000000)
    #case.test()























#print(df)

#
