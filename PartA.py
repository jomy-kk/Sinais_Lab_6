from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy.stats
from math import log10

k=0.495 #
sampling_rate = 500 #Hz


def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)

def decibeis (a):
    db=20*log10(a)
    return db


t = np.linspace(0, 2, sampling_rate, endpoint=False)
plt.figure()
sig = np.sin(100 * t)+ k*random.random()
plt.plot(t,sig)
print(signaltonoise(sig))
print(decibeis(signaltonoise(sig)))
plt.show()
