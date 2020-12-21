import matplotlib.pyplot as plt
import numpy as np
from numpy import arange
from scipy.io import wavfile
from scipy.signal import freqz, lfilter, ellip, ellipord, cheb1ord, cheby1


def highPassIIRellip(wav_file_path, plot_interval, verbose=False):
    # ------------------------------------------------
    # Create a signal.
    # ------------------------------------------------

    samplerate, x = wavfile.read(wav_file_path)
    nsamples = x.size
    t = arange(nsamples) / samplerate

    # ------------------------------------------------
    # Create a IIR filter and apply it to x.
    # ------------------------------------------------

    N, Wn = ellipord(wp=0.5, ws=0.45, gstop=60, gpass=1)
    b, a = ellip(N, 1, 60, Wn, btype='high')
    w, h = freqz(b, a, fs=240000)

    fig = plt.figure()
    h_dB = 20 * np.log10(np.abs(h))
    plt.plot(w, h_dB, 'b-')
    #plt.ylim(-150, 5)
    plt.ylabel('Magnitude (dB)')
    plt.xlabel('Frequency (Hz)')
    plt.grid(True)
    fig.savefig('results_a6/ellip_frequency_response.png', bbox_inches='tight')


    # Apply filtfilt to signal
    filtered_x = lfilter(b, a, x)
    wavfile.write('ex6_ellip_filtered.wav', samplerate, filtered_x)

    fig = plt.figure()
    # Plot the original signal.
    plt.subplot(2, 1, 1)
    plt.title('Original')
    plt.plot(t, x, 'b-', linewidth=0.5)
    plt.xlabel('Time (s)')
    plt.xlim(plot_interval)
    plt.ylim(-20500, 20500)
    plt.grid(True)
    # Plot the filtered signal, shifted to compensate for the phase delay.
    plt.subplot(2, 1, 2)
    plt.title('Filtered')
    plt.plot(t, filtered_x, 'g', linewidth=0.5)
    plt.xlim(plot_interval)
    plt.ylim(-20500, 20500)
    plt.xlabel('Time (s)')
    plt.grid(True)
    plt.subplots_adjust(hspace=0.7)
    fig.savefig('results_a6/ellip_filtered_output.png', bbox_inches='tight')

    if verbose:
        plt.show()


# HP IIR filter using ellip
highPassIIRellip('looneyTunes.wav', plot_interval=(4,5), verbose=True)


def bandPassIIRchebyI(wav_file_path, plot_interval, verbose=False):
    # ------------------------------------------------
    # Create a signal.
    # ------------------------------------------------

    samplerate, x = wavfile.read(wav_file_path)
    nsamples = x.size
    t = arange(nsamples) / samplerate

    # ------------------------------------------------
    # Create a IIR filter and apply it to x.
    # ------------------------------------------------

    N, Wn = cheb1ord(wp=[0.55, 0.65], ws= [0.5, 0.7], gstop=80, gpass=1)
    b, a = cheby1(N, 1, Wn, btype='bandpass')
    w, h = freqz(b, a, fs=200000)

    fig = plt.figure()
    h_dB = 20 * np.log10(np.abs(h))
    plt.plot(w, h_dB, 'b-')
    #plt.ylim(-150, 5)
    plt.ylabel('Magnitude (dB)')
    plt.xlabel('Frequency (Hz)')
    plt.grid(True)
    fig.savefig('results_a6/chebyI_frequency_response.png', bbox_inches='tight')


    # Apply filtfilt to signal
    filtered_x = lfilter(b, a, x)
    wavfile.write('ex6_chebyI_filtered.wav', samplerate, filtered_x)

    fig = plt.figure()
    # Plot the original signal.
    plt.subplot(2, 1, 1)
    plt.title('Original')
    plt.plot(t, x, 'b-', linewidth=0.5)
    plt.xlabel('Time (s)')
    plt.xlim(plot_interval)
    plt.ylim(-20500, 20500)
    plt.grid(True)
    # Plot the filtered signal, shifted to compensate for the phase delay.
    plt.subplot(2, 1, 2)
    plt.title('Filtered')
    plt.plot(t, filtered_x, 'g', linewidth=0.5)
    plt.xlim(plot_interval)
    plt.ylim(-20500, 20500)
    plt.xlabel('Time (s)')
    plt.grid(True)
    plt.subplots_adjust(hspace=0.7)
    fig.savefig('results_a6/chebyI_filtered_output.png', bbox_inches='tight')

    if verbose:
        plt.show()


bandPassIIRchebyI('looneyTunes.wav', plot_interval=(4,5), verbose=True)
