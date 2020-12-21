import os
os.chdir("D:/faculdade/5º ano/Projeto de Sensores, Sinais e Instrumentação/Labs/Lab 6") #Tive que fazer isto para conseguir usar os dados das imagens

from scipy.io import loadmat
from scipy.ndimage import median_filter as mf
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import firwin, freqz, kaiserord, lfilter, ellip, iirdesign,freqs
from numpy import log10, unwrap, angle, cos, sin, pi, absolute, arange
from scipy.io import wavfile

def HighPassIIRellip(wav_file_path, cutoff, slope, plot_interval, verbose=False, name =''):
    '''
    :param wav_signal:
    :param numtaps:
    :param cutoff:
    :param slope:
    :param plot_interval:
    :param verbose:
    :return:
    '''

    # ------------------------------------------------
    # Create a signal.
    # ------------------------------------------------

    samplerate, x = wavfile.read(wav_file_path)
    nsamples = x.size
    t = arange(nsamples) / samplerate

    # ------------------------------------------------
    # Create a IIR filter and apply it to x.
    # ------------------------------------------------

    # The Nyquist rate of the signal.
    nyq_rate = samplerate / 2.0

    # The desired width of the transition from pass to stop,
    # relative to the Nyquist rate.  We'll design the filter
    # with a 5 Hz transition width.
    width = 5.0 / nyq_rate

    # The desired attenuation in the stop band, in dB.
    ripple_db = slope

    # Compute the order and Kaiser parameter for the IIR filter.
    N, beta = kaiserord(ripple_db, width)
    # The cutoff frequency of the filter.
    cutoff_hz = cutoff

    # Use ellip with a Kaiser window to create a highpass IIR filter.
    taps=ellip(N, 0.5, -slope, cutoff_hz, btype='high', analog=True)

    # Use lfilter to filter x with the FIR filter.
    filtered_x = lfilter(taps, 1.0, x)
    # ------------------------------------------------
    # Plot the IIR filter coefficients.
    # ------------------------------------------------
    fig = plt.figure(1)
    plt.plot(taps, 'b', linewidth=2)
    plt.xlim(5000, 7000)
    plt.title('Filter Coefficients (%d taps)' % N)
    plt.grid(True)
    #fig.savefig('results_a4/' + name + '_filter_coefficients.png', bbox_inches='tight')
    plt.show()
    # ------------------------------------------------
    # Plot the magnitude response of the filter.
    # ------------------------------------------------

    fig = plt.figure(2)
    plt.clf()
    w, h = freqz(taps, worN=8000)
    plt.plot((w / pi) * nyq_rate, absolute(h), 'b-', linewidth=2)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.title('Frequency Response')
    plt.ylim(-0.05, 1.05)
    plt.xlim(5993, 6010)
    plt.grid(True)
    fig.savefig('results_a6/' + name + '_frequency_response.png', bbox_inches='tight')

    # Upper inset plot.
    ax1 = plt.axes([0.5, 0.6, .4, .25])
    plt.plot((w / pi) * nyq_rate, absolute(h), 'b-', linewidth=2)
    plt.xlim(6001, 6003)
    plt.ylim(0, 0.2)
    plt.ylim(0.9985, 1.001)
    plt.grid(True)

    # ------------------------------------------------
    # Plot the original and filtered signals.
    # ------------------------------------------------

    # The phase delay of the filtered signal.
    delay = 0.5 * (N - 1) / samplerate

    fig = plt.figure(3)
    # Plot the original signal.
    plt.subplot(2,1,1)
    plt.title('Original')
    plt.plot(t, x, 'b-', linewidth=0.5)
    plt.xlabel('Time (s)')
    plt.xlim(plot_interval[0], plot_interval[1])
    plt.ylim(-20500, 20500)
    plt.grid(True)
    # Plot the filtered signal, shifted to compensate for the phase delay.
    plt.subplot(2,1,2)
    plt.title('Filtered')
    plt.plot(t - delay, filtered_x, 'r-', linewidth=0.5)
     #Plot just the "good" part of the filtered signal.
     #The first N-1 samples are "corrupted" by the initial conditions.
    plt.plot(t[N - 1:] - delay, filtered_x[N - 1:], 'g', linewidth=0.5)
    plt.xlim(plot_interval[0], plot_interval[1])
    plt.ylim(-20500, 20500)
    plt.xlabel('Time (s)')
    plt.grid(True)
    plt.subplots_adjust(hspace=0.7)
    fig.savefig('results_a4/' + name + '_filtered_output.png', bbox_inches='tight')

    if verbose:
        plt.show()

    return

HighPassIIRellip('looneyTunes.wav', 6000, -60, (4,5), verbose=True, name='ex6')
