from scipy.io import savemat
import matplotlib.pyplot as plt
import numpy as np
from math import log10

k = 0.495
sampling_rate = 200 #Hz

def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)

def decibeis (a):
    db=20*log10(a)
    return db

t = np.linspace(0, 2, sampling_rate, endpoint=False)
sig = np.sin(100 * t) + k
snr = decibeis(signaltonoise(sig))
savemat('sin'+str(int(snr))+'.mat', {"signal": sig, "snr": snr})

plt.figure()
plt.plot(t, sig)
plt.title('SNR = ' + str(int(snr)) + ' dB dB (k=' + str(k) + ')')
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.show()
