import matplotlib.pyplot as plt
from scipy.signal import firwin, freqz, kaiserord, lfilter
from numpy import pi, absolute, arange
from scipy.io import wavfile

def linear_FIR_filter(wav_file_path, cutoff, slope, plot_interval, filter_type='', verbose=False, name =''):
    '''

    :param wav_signal:
    :param numtaps:
    :param cutoff:
    :param slope:
    :param plot_time:
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
    # Create a FIR filter and apply it to x.
    # ------------------------------------------------

    # The Nyquist rate of the signal.
    nyq_rate = samplerate / 2.0

    # The desired width of the transition from pass to stop,
    # relative to the Nyquist rate.  We'll design the filter
    # with a 5 Hz transition width.
    width = 5.0 / nyq_rate

    # The desired attenuation in the stop band, in dB.
    ripple_db = slope

    # Compute the order and Kaiser parameter for the FIR filter.
    N, beta = kaiserord(ripple_db, width)

    # The cutoff frequency of the filter.
    cutoff_hz = cutoff

    if filter_type == '': # Use firwin with a Kaiser window to create a lowpass FIR filter.
        taps = firwin(N, cutoff_hz / nyq_rate, window=('kaiser', beta))
    else: # Use firwin with a Kaiser window to create another type of FIR filter.
        taps = firwin(N, [v/nyq_rate for v in cutoff_hz], window=('kaiser', beta), pass_zero=filter_type)

    # Use lfilter to filter x with the FIR filter.
    filtered_x = lfilter(taps, 1.0, x)
    wavfile.write(name + '_filtered.filtered_wav', samplerate, filtered_x)

    # ------------------------------------------------
    # Plot the FIR filter coefficients.
    # ------------------------------------------------

    fig = plt.figure(1)
    plt.plot(taps, 'bo-', linewidth=2)
    plt.xlim(1730, 1850)
    plt.title('Filter Coefficients (%d taps)' % N)
    plt.grid(True)
    fig.savefig('results_a4/' + name + '_' + filter_type + '_filter_coefficients.png', bbox_inches='tight')

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
    plt.xlim(1800, 4000)
    plt.grid(True)
    fig.savefig('results_a4/' + name + '_' + filter_type + '_frequency_response.png', bbox_inches='tight')

    # Upper inset plot.
    ax1 = plt.axes([0.68, 0.6, .2, .25])
    plt.plot((w / pi) * nyq_rate, absolute(h), 'b-', linewidth=2)
    plt.xlim(3000, 3010)
    plt.ylim(0.9, 1.02)
    plt.grid(True)

    # Down inset plot.
    ax2 = plt.axes([0.68, 0.2, .2, .25])
    plt.plot((w / pi) * nyq_rate, absolute(h), 'b-', linewidth=2)
    plt.xlim(2980, 3000)
    plt.ylim(-0.02, 0.1)
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
    # Plot just the "good" part of the filtered signal.
    # The first N-1 samples are "corrupted" by the initial conditions.
    plt.plot(t[N - 1:] - delay, filtered_x[N - 1:], 'g', linewidth=0.5)
    plt.xlim(plot_interval[0], plot_interval[1])
    plt.ylim(-20500, 20500)
    plt.xlabel('Time (s)')
    plt.grid(True)
    plt.subplots_adjust(hspace=0.7)
    fig.savefig('results_a4/' + name + '_' + filter_type + '_filtered_output.png', bbox_inches='tight')

    if verbose:
        plt.show()

    return

#linear_FIR_filter('looneyTunes.filtered_wav', 2000, -60, (4,5), verbose=True, name='ex4')
linear_FIR_filter('looneyTunes.filtered_wav', [2000, 3000], -40, (4,5), verbose=True, name='ex5', filter_type='bandstop')