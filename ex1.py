import time
import matplotlib.pyplot as plt
from scipy.signal import decimate
import serial
from parser import getINI

arduino = serial.Serial('/dev/cu.usbmodem14301',9600)

iniData = getINI()
numRowsCollect = int(iniData['numRowsCollect'])
numPoints = int(iniData['numPoints'])

time.sleep(3)
dataList =[0]*numPoints
dataFile = open('dataFile.txt', 'w')

def getValues():
    arduino.write(b'g')
    arduinoData = arduino.readline().decode().split('\r\n')
    return arduinoData[0]

def printToFile(data,index):
    dataFile.write(data)
    if index != (numPoints-1):
        dataFile.write(',')
    else:
        dataFile.write('\n')

def getAverage(dataSet,row):
    dataAvg = sum(dataSet) / len(dataSet)
    print('Average for ' + str(row) + ' is: ' + str(dataAvg))


'''
# Filter - order 8 Chebyshev type I filter
data = data[1:]
data_filtered = decimate(data, 5)
'''
'''
# Plot
plt.figure()
plt.subplot(2,1,1)
plt.plot(range(0, len(data)*analogReadInterval, analogReadInterval), [(v if v != None else v) for v in data], color='blue')
plt.title('Original')
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.xticks(range(0, (acquisitionTime*1000 + 1), 1000))
#plt.yticks([0, 1, 2, 3, 4, 5,6])
plt.subplot(2, 1, 2)
plt.plot(range(0, len(data_filtered)*analogReadInterval, analogReadInterval), [(v if v != None else v) for v in data_filtered], color='blue')
plt.title('Filtered')
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.xticks(range(0, (acquisitionTime + 1) * 1000, 1000))
#plt.yticks([0,1,2,3,4,5,6])
plt.show()

'''
