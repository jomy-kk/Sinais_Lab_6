from scipy.io import loadmat
import os
os.chdir("D:/faculdade/5º ano/Projeto de Sensores, Sinais e Instrumentação/Labs/Lab 6") #Tive que fazer isto para conseguir usar os dados das imagens
import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

sampling_rate = 200 #Hz
samples = 3 #number of samples to use in filter

t = np.linspace(0, 2, sampling_rate, endpoint=False)
sample_3 = loadmat('sin-3.mat')
sample0 = loadmat('sin0.mat')
sample20 = loadmat('sin20.mat')

signal_3= sample_3['signal']
signal0 = sample0['signal']
signal20 = sample20['signal']

y_3=sp.ndimage.median_filter(signal_3,samples)
y0=sp.ndimage.median_filter(signal0,samples)
y20=sp.ndimage.median_filter(signal20,samples)

fig, (ax1, ax2, ax3) = plt.subplots(3)
fig.suptitle('Isto está a fazer algo')
ax1.plot(t, signal_3[0])
ax1.plot(t, y_3[0])
ax2.plot(t, signal0[0])
ax2.plot(t, y0[0])
ax3.plot(t, signal20[0])
ax3.plot(t, y20[0])
plt.show()
