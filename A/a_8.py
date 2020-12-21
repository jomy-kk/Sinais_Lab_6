import matplotlib.pyplot as plt
from numpy import max, min, arange, zeros
from scipy.io import wavfile
from scipy.signal import medfilt

def scipy_medfilt(wav_file_path, samples, plot_interval, verbose=False, name =''):

    samplerate, x = wavfile.read(wav_file_path)
    nsamples = x.size
    t = arange(nsamples) / samplerate
    filtered_x = medfilt(x, samples)
    wavfile.write(name + '_scipy_medfilt_' + str(samples) +'samples.wav', samplerate, filtered_x)

    fig = plt.figure()
    plt.subplot(2, 1, 1)
    plt.title('Original')
    plt.plot(t, x, '-b', linewidth=0.2)
    plt.xlim(plot_interval)
    y_upper_lim, y_lower_lim = max(x) * 1.1, min(x) * 1.1
    plt.ylim(y_lower_lim, y_upper_lim)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.title('Filtered')
    plt.plot(t, filtered_x, '-g', linewidth=0.2)
    plt.xlim(plot_interval)
    plt.ylim(y_lower_lim, y_upper_lim)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    plt.subplots_adjust(hspace=0.7)
    fig.savefig('results_a8/Median Filter SciPy (S=' + str(samples) + ') - ' + str(plot_interval) +'.png',
                bbox_inches='tight')
    if verbose:
        plt.show()

    return

'''
scipy_medfilt('tune_sapn.wav', 3, [2,2.3], verbose=True, name='ex8')
scipy_medfilt('tune_sapn.wav', 3, [2.5,3.5], verbose=True, name='ex8')

scipy_medfilt('tune_sapn.wav', 5, [2,2.3], verbose=True, name='ex8')
scipy_medfilt('tune_sapn.wav', 5, [2.5,3.5], verbose=True, name='ex8')
'''




def my_median_filter(wav_file_path, samples, plot_interval, verbose=False, name =''):
    assert samples%2 == 1, "Number of samples for the window size must be odd."

    samplerate, signal = wavfile.read(wav_file_path)
    nsamples = signal.size
    t = arange(nsamples) / samplerate

    shift = samples//2

    data_final = zeros(signal.shape)
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

    wavfile.write(name + '_my_medfilt_' + str(samples) + 'samples.wav', samplerate, data_final)

    fig = plt.figure()
    plt.subplot(2, 1, 1)
    plt.title('Original')
    plt.plot(t, signal, '-b', linewidth=0.2)
    plt.xlim(plot_interval)
    y_upper_lim, y_lower_lim = max(signal) * 1.1, min(signal) * 1.1
    plt.ylim(y_lower_lim, y_upper_lim)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.title('Filtered')
    plt.plot(t, data_final, '-r', linewidth=0.2)
    plt.xlim(plot_interval)
    plt.ylim(y_lower_lim, y_upper_lim)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    plt.subplots_adjust(hspace=0.7)
    fig.savefig('results_a8/My Median Filter (S=' + str(samples) + ') - ' + str(plot_interval) + '.png',
                bbox_inches='tight')

    if verbose:
        plt.show()

    return
'''
my_median_filter('tune_sapn.wav', 3, [2,2.3], verbose=True, name='ex8')
my_median_filter('tune_sapn.wav', 3, [2.5,3.5], verbose=True, name='ex8')
my_median_filter('tune_sapn.wav', 7, [2,2.3], verbose=True, name='ex8')
my_median_filter('tune_sapn.wav', 7, [2.5,3.5], verbose=True, name='ex8')
'''

from scipy.fftpack import fft
from numpy import abs, asanyarray, where, log10
def filtered_results_stats(signal, verbose=False, name=''):
    if verbose:
        print('Results of', name)

    # Noise
    a = signal
    a = asanyarray(a)
    m = a.mean(0)
    sd = a.std(axis=0, ddof=0)
    snr = where(sd == 0, 0, m / sd)
    if verbose:
        print('SNR =', snr)

    # Distortion
    sq_sum = 0.0
    abs_data = abs(fft(signal))
    for r in range(len(abs_data)):
        sq_sum = sq_sum + (abs_data[r]) ** 2

    sq_harmonics = sq_sum - (max(abs_data)) ** 2.0
    thd = 100 * sq_harmonics ** 0.5 / max(abs_data)

    if verbose:
        print('THD =', thd, end='\n\n')

samplerate, signal = wavfile.read('tune_sapn.wav')
filtered_results_stats(signal, True, 'Original tune_sapn.wav')

samplerate, signal = wavfile.read('ex8_my_medfilt_3samples.wav')
filtered_results_stats(signal, True, 'ex8_my_medfilt_3samples.wav')

samplerate, signal = wavfile.read('ex8_my_medfilt_7samples.wav')
filtered_results_stats(signal, True, 'ex8_my_medfilt_7samples.wav')

samplerate, signal = wavfile.read('ex8_scipy_medfilt_3samples.wav')
filtered_results_stats(signal, True, 'ex8_scipy_medfilt_3samples.wav')

samplerate, signal = wavfile.read('ex8_scipy_medfilt_5samples.wav')
filtered_results_stats(signal, True, 'ex8_scipy_medfilt_5samples.wav')