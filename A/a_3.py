from scipy.io import loadmat
import os
#os.chdir("D:/faculdade/5º ano/Projeto de Sensores, Sinais e Instrumentação/Labs/Lab 6") #Tive que fazer isto para conseguir usar os dados das imagens
from scipy.ndimage import median_filter as mf
import matplotlib.pyplot as plt
import numpy as np

def median_filter(signals, samples, origin, sampling_frequency, sampling_time, verbose=False, labels=()):
    '''
    Applied the median filter to one or more signals.
    :param signals: one or list of 2+ Ndarrays of signals
    :param samples: number of samples to use in filter
    :param origin: it controls the placement of the filter on the input signals.
    If 'center' is given, it centers the filter over the point.
    If 'left' is given, it shifts the filter to the left.
    If 'right' is given, it shifts the filter to the right.
    :param sampling_frequency: sampling frequency of signal
    :param sampling_time: duration of signal acquisition

    (Optionals)
    :param verbose: if True, prints the variances
    :param labels: if given, the plots will be tittled with them

    :return: Nothing
    '''

    t = np.linspace(0, sampling_time, sampling_frequency, endpoint=False)

    shift = None
    if origin == 'center': shift = 0
    if origin == 'left': shift = int(samples/2)
    if origin == 'right': shift = int(-samples/2)
    if shift == None:
        print('Please introduce a valid origin mode.')
        return

    Y = []
    for s in signals:
        y = mf(s, samples, origin=shift)
        Y.append(y)

    fig, AX = plt.subplots(len(signals))
    for i in range(len(signals)):
        AX[i].plot(t, signals[i], '-b')
        AX[i].plot(t, Y[i], '-g')
        if len(labels):
            AX[i].set_title(labels[i])

    plt.subplots_adjust(hspace=1)
    fig.savefig('results_a3/Median Filters (S=' + str(samples) + ' - '+ origin + ' ' + str(shift) +').png', bbox_inches='tight')
    if verbose:
        plt.show()

    return

sA = loadmat('sin-3.mat')['signal']
sB = loadmat('sin0.mat')['signal']
sC = loadmat('sin20.mat')['signal']

signals = [np.reshape(sA, sA.size), np.reshape(sB, sB.size), np.reshape(sC, sC.size)]
median_filter(signals, 7, 'right', 200, 2, verbose=True, labels=('Signal A', 'Signal B', 'Signal C'))