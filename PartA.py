from scipy.io import savemat
import matplotlib.pyplot as plt
import numpy as np
from math import log10
from scipy.io import loadmat
from statistics import variance

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
plt.title('SNR = ' + str(int(snr)) + ' dB (k=' + str(k) + ')')
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.show()

def ma_filter(signal, N, sampling_frequency, sampling_time, verbose=False, label=''):
    '''
    Performs a cumulative moving average filter with window of size N

    :param signal: Ndarray representing the signal
    :param N: order, aka window size (int)
    :param sampling_frequency: sampling frequency of signal
    :param sampling_time: duration of signal acquisition

    (Optionals)
    :param verbose: if True, prints the variances
    :param label: if given, the plot will be tittled with it

    :return variance_deference: The difference of the original signal
    variance and the filtered signal variance.
    '''

    cumsum, moving_aves = [0], []

    for i, x in enumerate(signal, 1):
        cumsum.append(cumsum[i - 1] + x)
        if i >= N:
            moving_ave = (cumsum[i] - cumsum[i - N]) / N
            # can do stuff with moving_ave here
            moving_aves.append(moving_ave)

    t = np.linspace(0, sampling_time, sampling_frequency, endpoint=False)


    fig = plt.figure()
    plt.plot(t, signal, 'b-', label='Original', linewidth=0.5)
    t = np.linspace(0, 2, sampling_frequency - N + 1, endpoint=False)
    plt.plot(t, moving_aves, 'g-', label='MA Filtered')
    plt.title('Signal '+ label +' - MA filtered (N=' + str(N) + ')')
    plt.xlabel('Time (ms)')
    plt.ylim((np.min(signal), np.max(signal)))
    plt.legend(loc='best')
    plt.ylabel('Voltage (V)')
    fig.savefig('Signal '+ label +' - MA filtered (N=' + str(N) + ').png', bbox_inches = 'tight')
    if verbose:
        plt.show()


    original_var = variance(signal)
    filtered_var = variance(moving_aves)

    if verbose:
        print('Variance Original:', original_var)
        print('Variance Filtered:', filtered_var)

    return original_var - filtered_var

def find_max_variance_ma_filter_order(signal, sampling_frequency, sampling_time, verbose=False, label=''):
    variance_differences = []
    for n in range(1, signal.size):
        if verbose:
            print('Trying N =', n)
        var = float(ma_filter(signal, n, sampling_frequency, sampling_time, verbose=False, label=label))
        variance_differences.append(var)

    if verbose:
        fig = plt.figure()
        plt.plot(variance_differences)
        plt.xlabel('N')
        plt.ylabel('Var(original) - Var(filtered)')
        plt.show()

    return variance_differences.index(max(variance_differences))


for n in (11, 51):
    print("N =", n)
    for label in ('A', 'B', 'C'):
        print('Signal', label)
        signal = loadmat('signal' + label +'.mat')['signal']
        signal = np.reshape(signal, signal.size)
        print('Difference =', ma_filter(signal, n, 200, 2,
                        verbose=True, label=label), end='\n\n')

signal = loadmat('signalA.mat')['signal']
signal = np.reshape(signal, signal.size)
print('Max N =',find_max_variance_ma_filter_order(signal, 200, 2, verbose=True, label='A'))