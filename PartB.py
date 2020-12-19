import matplotlib.pyplot as plt
import serial

'''
arduino = serial.Serial('/dev/cu.usbmodem14301', 9600)


data = []
while arduino.available() > 0:
    value = arduino.read()
    if value != None:
        data.append(value)

# Plot
plt.figure()
plt.subplot(1,1,1)
plt.plot(range(0, len(data)),data, color='blue')
plt.title('Aliasing Filtered Signal')
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.show()
'''

values = open('b2', 'r').readlines()
values = [int(v.split('\n')[0]) for v in values]

plt.figure(figsize=(15,6))
plt.plot(range(0, len(values)), values, color='blue')
plt.yticks((400, 500, 600, 700, 800, 900))
plt.title('Aliasing Filtered Signal')
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (mV)')
plt.show()

from scipy.signal import iirdesign, freqz, filtfilt
from numpy import log10, unwrap, angle

b, a = iirdesign(wp = [0.1, 0.2], ws = [0.05, 0.25], gstop= 60, gpass=1, ftype='cheby2')

w, h = freqz(b, a)

fig, ax1 = plt.subplots()
ax1.set_title('Digital filter frequency response')
ax1.plot(w, 20 * log10(abs(h)), 'b')
ax1.set_ylabel('Amplitude [dB]', color='b')
ax1.set_xlabel('Frequency [rad/sample]')
ax1.grid()
ax1.set_ylim([-130, 30])
ax2 = ax1.twinx()
angles = unwrap(angle(h))
ax2.plot(w, angles, 'g')
ax2.set_ylabel('Angle (radians)', color='g')
ax2.grid()
ax2.axis('tight')
ax2.set_ylim([-10, 10])
plt.show()

fgust = filtfilt(b, a, values, method="gust")
fpad = filtfilt(b, a, values, padlen=50)
plt.show()

# Apply filtfilt to sig, once using the Gustafsson method,
# and once using padding, and plot the results for comparison.
plt.figure(figsize=(15,6))
#plt.plot(range(0, len(y)), y, color='blue')
#plt.plot(values, 'k-', label='input')
plt.plot(fgust, 'b-', linewidth=4, label='gust')
plt.plot(fpad, 'c-', linewidth=1.5, label='pad')
plt.legend(loc='best')
plt.yticks((-150, -100, -50, 0, 50, 100, 150))
plt.title('Digital Filtered Output')
plt.xlabel('Time (ms)')
plt.ylabel('Magnitude')
plt.show()
