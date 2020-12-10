ini_data_result = {}

def getINI():
    ini_data = {}
    dataFile_ini = open('dataSetup.ini', 'r')
    iniHeader = dataFile_ini.readline().split(':')
    print(iniHeader[0] + ' ' + iniHeader[1].rstrip())
    iniReadLines = int(iniHeader[1].rstrip())

    for i in range(0,iniReadLines):
        variable = dataFile_ini.readline().split(':')
        ini_data[variable[0]] = variable[1].rstrip()
    dataFile_ini.close()
    return ini_data

ini_data_result = getINI()
print(ini_data_result)