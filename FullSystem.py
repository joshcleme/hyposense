import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

#reading the vital sign and scale data
signalHR = pd.read_csv('hypo_data/31021HRGSR.csv', usecols=[0])
signalGSR = pd.read_csv('hypo_data/31121HRGSR.csv', usecols=[1])
signalWeight = pd.read_csv('hypo_data/31021HRGSR.csv', usecols=[2])
signalTemp = pd.read_csv('hypo_data/bach_temp.csv', usecols=[1])

#removing blank column from data
HR = signalHR.to_numpy()
HR = np.delete(HR, -1)
weight = signalWeight.to_numpy()
weight = np.delete(weight, -1)
temp = signalTemp.to_numpy()
temp = np.delete(temp, -1)

### pass data through LOW PASS FILTER (fs=250Hz, fc=15, N=6) ###
low_passHR = np.convolve(HR, [0.023834522, 0.093047634, 0.232148599, 0.301938491, 0.232148599, 0.093047634, 0.023834522])

### pass data through HIGH PASS FILTER (fs=250Hz, fc=5Hz, N=6) to create BAND PASS result ###
band_passHR = np.convolve(low_passHR, [-0.000798178, -0.003095487, -0.007692586, 0.989209446, -0.007692586, -0.003095487, -0.000798178])

### pass data through weighter differiator
diffHR = np.convolve(band_passHR, [1, 2, -2, -1])

## pass data through square function
squaredHR = diffHR * diffHR

#GSR Data Prep
GSR = signalGSR.to_numpy()
GSR = np.delete(GSR, -1)
smoothGSR = savgol_filter(GSR, 2001, 3)

#Some set-up to convert the HR data from analog to BPM
signalWeight = 1
heartRateList = []
beatIndex = []
BPM = 0
q = 1
w = 0
i = 59 #Time length
for i in range(len(squaredHR)):
    if i > 59:
        avg = (sum(squaredHR[(i-60):i]))/60
        averageWeightedLower = avg * 0.70
        averageWeightedHigher = avg * 1.10
        if q < 1 or q > len(beatIndex):
            q = 1
        if squaredHR[i-30] >= averageWeightedLower and squaredHR[i-30] <= averageWeightedHigher: #counting spikes in analog data using range
            beatIndex.append(i-30)
            if w <= 600:
                if len(beatIndex) > 2:
                    if beatIndex[q] == (1 + beatIndex[q-1]) or beatIndex == (beatIndex[q-1] - 1):
                        del beatIndex[q-1]
        q = q + 1
        w = w + 1
        if w == 600: #after 60 seconds print the BPM reading for that pinute
            BPM = len(beatIndex)
            heartRateList.append(BPM)
            beatIndex.clear()
            BPM = 0
            w = 0
            q = 1

#set up for the flagging system
fivetimer = 0 #timers if a hypoglycemic event is detected
seventimer = 0
t=300
hypoHR = False
hypoHRIndex = []
hypoHRReading = []
frameSweepHR = 3
hypoHRFlag = False
tempReading = []
hypoTempIndex = []
hypoTempEmg = False
hypoTemp = False
tempFrameSize = 28

#main flagging algorithm
for i in range(len(GSR)):
    subGSR = [sum(smoothGSR[i:i + t]) / t] #filtering the GSR data further
    grad = abs(np.gradient(subGSR))
    hypoSignatures = np.array([])
    if grad[i] >= 0.025: #finding GSR changes over time to triger flag
        valid_indicies = np.append(hypoSignatures, i)
        GSRflag = True
    else:
        GSRflag = False
    if i >= 6000 and (i % 6000) == 0: #flagging system for HR
        hrTime = i/6000
        frameSweepHR = frameSweepHR + 1
        if frameSweepHR == 4:
            avgHR = (sum(heartRateList[hrTime:hrTime + 5])) / 5
            frameSweepHR = 0
        if heartRateList[hrTime] > (avgHR + 15):
            hypoHR = True
        if heartRateList[hrTime] < (avgHR + 15):
            hypoHR = False
        if hypoHR == True:
            hypoHRIndex.append(hrTime)
            hypoHRReading.append(heartRateList[hrTime])
        if hypoHR == False:
            hypoHRIndex.clear()
            hypoHRReading.clear()
        if len(hypoHRIndex) >= 2:
            hypoHRFlag = True
            print("OMG Heart Rate Alert")
        if len(hypoHRIndex) < 2:
            hypoHRFlag = False
        if i >= 15000 and (i % 1000) == 0: #flagging system for temperature
            tempTime = i/1000
            tempFrameSize = tempFrameSize + 1
            if tempFrameSize == 29:
                baseline = sum(temp[tempTime - 30:tempTime]) / 30
                tempFrameSize = 0
            if temp[tempTime] > (baseline + 0.3):
                hypoTemp = True
            if temp[i] < (baseline + 0.3):
                hypoTemp = False
            if hypoTemp == True:
                hypoTempIndex.append(tempTime)
                tempReading.append(temp[tempTime])
            if hypoTemp == False:
                hypoTempIndex.clear()
                tempReading.clear()
            if len(hypoTempIndex) > 6:
                hypoTempEmg = True
                print("Emergency")
            if len(hypoTempIndex) < 6:
                hypoTempEmg = False
            i = i + 1
        #####The start of the weight triggering system
        if hypoTempEmg == True and GSRflag == True:
            fivetimer = fivetimer + 1
            print("Snack Time! Call the user")
            if signalWeight == 0:
                print("All Clear")
            if signalWeight != 0 and fivetimer == 2999:
                print("Calling Emergency Contact")
            if signalWeight != fivetimer == 5999:
                print("Calling EMS")
        if hypoHRFlag == True and GSRflag == True:
            fivetimer = fivetimer + 1
            print("Snack Time! Call the user")
            if signalWeight == 0:
                print("All Clear")
            if signalWeight != 0 and fivetimer == 2999:
                print("Calling Emergency Contact")
            if signalWeight != fivetimer == 5999:
                print("Calling EMS")
        if hypoHRFlag == True and hypoTempEmg == True:
            fivetimer = fivetimer + 1
            print("Snack Time! Call the user")
            if signalWeight == 0:
                print("All Clear")
            if signalWeight != 0 and fivetimer == 2999:
                print("Calling Emergency Contact")
            if signalWeight != fivetimer == 5999:
                print("Calling EMS")
        if hypoHRFlag == True and hypoTempEmg == True and GSRflag == True:
            seventimer = seventimer + 1
            print("Snack Time! Call the user and their Emergency Contact")
            if signalWeight == 0:
                print("All Clear")
            if signalWeight != 0 and fivetimer == 6999:
                print("Calling EMS")