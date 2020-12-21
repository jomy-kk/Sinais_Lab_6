from scipy.io import loadmat
import os
#os.chdir("D:/faculdade/5º ano/Projeto de Sensores, Sinais e Instrumentação/Labs/Lab 6") #Tive que fazer isto para conseguir usar os dados das imagens
from scipy.ndimage import median_filter as mf
import matplotlib.pyplot as plt
import numpy as np

def median_filter(signals, samples, origin, sampling_frequency, sampling_time, verbose=False, labels=()):


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

def my_median_filter(signal, samples, origin, sampling_frequency, sampling_time, verbose=False, path_to_save='.'):
    '''
        Applies the median filter to one or more signals.
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

    assert origin in ('center', 'left', 'right'), "Please give an origin to thw window: 'center', 'left', 'right'."
    assert samples%2 == 1, "Number of samples for the window size must be odd."

    if origin == 'center':
        shift = samples//2
    if origin == 'left':
        shift = +(samples-1)
    if origin == 'right':
        shift = -(samples-1)

    data_final = np.zeros(signal.shape)
    temp = []

    for i in range(len(signal)):
        # Populate window in temp
        for z in range(samples):
            indexer = i + z - shift
            if indexer < 0:
                temp.append(signal[0])
            elif indexer > signal.size - 1:
                temp.append(signal[signal.size - 1])
            else:
                temp.append(signal[indexer])

        # Sort the samples inside the window
        temp.sort()
        # The result is the middle sample of the sorted window
        data_final[i] = temp[len(temp) // 2]

        temp = []

    fig = plt.figure()
    t = np.linspace(0, sampling_time, sampling_frequency, endpoint=False)
    plt.plot(t, signal, '-b')
    plt.plot(t, data_final, '-g')

    plt.subplots_adjust(hspace=1)
    fig.savefig(path_to_save + '/My Median Filter (S=' + str(samples) + ' - ' + origin + ' ' + str(samples) + ').png',  bbox_inches='tight')
    if verbose:
        plt.show()

    return

def my_median_filter_multiple(signals, samples, origin, sampling_frequency, sampling_time, verbose=False, path_to_save='.', labels=()):
    Y = []
    for signal in signals:
        if origin == 'center':
            shift = samples//2
        if origin == 'left':
            shift = +(samples-1)
        if origin == 'right':
            shift = -(samples-1)

        data_final = np.zeros(signal.shape)
        temp = []

        for i in range(len(signal)):
            # Populate window in temp
            for z in range(samples):
                indexer = i + z - shift
                if indexer < 0:
                    temp.append(signal[0])
                elif indexer > signal.size - 1:
                    temp.append(signal[signal.size - 1])
                else:
                    temp.append(signal[indexer])

            # Sort the samples inside the window
            temp.sort()
            # The result is the middle sample of the sorted window
            data_final[i] = temp[len(temp) // 2]

            temp = []

        Y.append(data_final)

    t = np.linspace(0, sampling_time, sampling_frequency, endpoint=False)
    fig, AX = plt.subplots(len(signals))
    for i in range(len(signals)):
        AX[i].plot(t, signals[i], '-b')
        AX[i].plot(t, Y[i], '-g')
        if len(labels):
            AX[i].set_title(labels[i])

    plt.subplots_adjust(hspace=1)
    fig.savefig('results_a3/My Median Filters (S=' + str(samples) + ' - ' + origin + ').png',
                bbox_inches='tight')
    if verbose:
        plt.show()

    return

'''
sA = loadmat('sin-3.mat')['signal']
sB = loadmat('sin0.mat')['signal']
sC = loadmat('sin20.mat')['signal']

signals = [np.reshape(sA, sA.size), np.reshape(sB, sB.size), np.reshape(sC, sC.size)]
median_filter(signals, 7, 'right', 200, 2, verbose=True, labels=('Signal A', 'Signal B', 'Signal C'))
'''

'''sA = loadmat('sin-3.mat')['signal']
my_median_filter(np.reshape(sA, sA.size), 7, 'center', 200, 2, verbose=True, path_to_save='results_a3')
'''
'''
sA = loadmat('sin-3.mat')['signal']
sB = loadmat('sin0.mat')['signal']
sC = loadmat('sin20.mat')['signal']

signals = [np.reshape(sA, sA.size), np.reshape(sB, sB.size), np.reshape(sC, sC.size)]
my_median_filter_multiple(signals, 3, 'left', 200, 2, verbose=True, labels=('Signal A', 'Signal B', 'Signal C'))
my_median_filter_multiple(signals, 7, 'left', 200, 2, verbose=True, labels=('Signal A', 'Signal B', 'Signal C'))
'''

def my_median_filter_optimized(signal, samples, origin, sampling_frequency, sampling_time, verbose=False):

    assert origin in ('center', 'left', 'right'), "Please give an origin to thw window: 'center', 'left', 'right'."
    assert samples%2 == 1, "Number of samples for the window size must be odd."

    if origin == 'center':
        shift = samples//2
    if origin == 'left':
        shift = +(samples-1)
    if origin == 'right':
        shift = -(samples-1)

    data_final = np.zeros(signal.shape)
    temp = []

    # Populate window in temp for the first time
    for z in range(samples):
        indexer = z - shift
        if indexer < 0:
            temp.append(signal[0])
        else:
            temp.append(signal[indexer])

    for i in range(1, len(signal)):
        # Sort the samples inside the window
        temp_sorted = temp.copy()
        temp_sorted.sort()
        # The result is the middle sample of the sorted window
        data_final[i] = temp_sorted[len(temp_sorted) // 2]
        # Shit right of the window
        if i > signal.size - 1:
            temp = temp[1:]
            temp.append(signal[signal.size - 1])
        else:
            temp = temp[1:]
            temp.append(signal[i])

    fig = plt.figure()
    t = np.linspace(0, sampling_time, sampling_frequency, endpoint=False)
    plt.plot(t, signal, '-b')
    plt.plot(t, data_final, '-g')

    if verbose:
        plt.show()

    return

sA = loadmat('sin-3.mat')['signal']
my_median_filter(np.reshape(sA, sA.size), 7, 'center', 200, 2, verbose=True)
my_median_filter_optimized(np.reshape(sA, sA.size), 7, 'center', 200, 2, verbose=True)