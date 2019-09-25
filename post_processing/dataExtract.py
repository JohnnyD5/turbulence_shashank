# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 17:50:39 2019

@author: sunny619
"""

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import scipy

pdf = pd.read_hdf('force.h5', key='df')
#pdf = pdf.iloc[1090000:]
pdf.drop(pdf.index[100000:500000], inplace=True)
print(pdf)
t=pdf['Time']
dp=0.01
u_inf=14.607
t=(t*u_inf)/dp
Cd=pdf['Cd']
Cl=pdf['Cl']
y=Cd
#y=y-np.mean(y)
y= abs(y)
#y=y-np.mean(y)
dt=np.diff(t)
deltaT=0.014607
#df=pd.DataFrame(dt,columns = ['dt'])
#Fs=1/dt
#n = len(y)
#k = np.arange(n)
#frq = k/dt   # two sides frequency range
#frq = frq[range(int(n/2))]  # one side frequency range
#St=frq*dp/u_inf
#Y = np.fft.fft(y)/n   # fft computing and normalization
#Y = Y[range(int(n/2))]
#fig, ax = plt.subplots(2, 1)
#ax[0].plot(t,y)
#ax[0].set_xlabel('Time')
#ax[0].set_ylabel('Amplitude')
#ax[1].plot(St,abs(Y),'r') # plotting the spectrum
#ax[1].set_xlabel('St')
#ax[1].set_ylabel('|Y(freq)|')
#ax[1].set_xlim(left = 0,right = 100)
N = len(y);
#deltaT = 0.001
Fs = 1.0/deltaT; # sampling frequency
freq = np.arange(0,N)*Fs/N
St=freq
Y = scipy.fft(y-np.mean(y))
fig, ax = plt.subplots(2,1)
ax[0].plot(t,y)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
ax[1].loglog(St, 2.0/N * np.abs(Y)) #this will have the mirror effect, abs is to take out the imaginary part
ax[1].set_xlabel('St')
ax[1].set_ylabel(r'$\hat{\omega}$')
#removing top and right borders
ax[1].spines['top'].set_visible(False)
ax[1].spines['right'].set_visible(False)
# set x limit and y limit
ax[1].set_xlim(left = 0.0001, right = 10)
ax[1].set_ylim(top = 1e-2, bottom = 1e-6)
plt.show()
plt.savefig('fft_re10k__re10k_noslip.tif', dpi=300)
#ax[1].savefig('fft_re10k_no_slip.tif', dpi=300,pad_inches=1)
