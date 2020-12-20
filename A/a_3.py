from scipy.io import loadmat
import os
#os.chdir("D:/faculdade/5º ano/Projeto de Sensores, Sinais e Instrumentação/Labs/Lab 6") #Tive que fazer isto para conseguir usar os dados das imagens
from scipy.ndimage import median_filter as mf
import matplotlib.pyplot as plt
import numpy as np

def median_filter(signals, samples, sampling_frequency, sampling_time, verbose=False, labels=()):
    '''
    Applied the median filter to one or more signals.
    :param signals: One or list of 2+ Ndarrays of signals
    :param samples: number of samples to use in filter
    :param sampling_frequency: sampling frequency of signal
    :param sampling_time: duration of signal acquisition

    (Optionals)
    :param verbose: if True, prints the variances
    :param labels: if given, the plots will be tittled with them

    :return: Nothing
    '''

    t = np.linspace(0, sampling_time, sampling_frequency, endpoint=False)

    Y = []
    for s in signals:
        y = mf(s, samples)
        Y.append(y)

    fig, AX = plt.subplots(len(signals))
    for i in range(len(signals)):
        AX[i].plot(t, signals[i], '-b')
        AX[i].plot(t, Y[i], '-g')
        if len(labels):
            AX[i].set_title(labels[i])

    plt.subplots_adjust(hspace=1)
    fig.savefig('results_a3/Median Filters (S=' + str(samples) + ').png', bbox_inches='tight')
    if verbose:
        plt.show()

    return

sA = loadmat('sin-3.mat')['signal']
sB = loadmat('sin0.mat')['signal']
sC = loadmat('sin20.mat')['signal']

signals = [np.reshape(sA, sA.size), np.reshape(sB, sB.size), np.reshape(sC, sC.size)]
median_filter(signals, 7, 200, 2, verbose=True, labels=('Signal A', 'Signal B', 'Signal C'))