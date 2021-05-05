import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

##### Replicate these lines in Python console

# read in file with better column names
signalTemp = pd.read_csv('hypo_data/bach_temp.csv', usecols=[1])

#pull out the V5 signal
temp = signalTemp.to_numpy()
temp = np.delete(temp, -1)

### pass data through weighter differiator
diffTemp = np.convolve(temp, [1, 2, -2, -1])   #I think this is incorrect as it does not look "forward" but should work

plt.plot(temp)
plt.xlabel('Time (0.1 s)')
plt.ylabel('temp')

tempReading = []
hypoTempIndex = []
hypoTempEmg = False
hypoTemp = False
i = 115
tempFrameSize = 28
while i < len(temp):
    tempFrameSize = tempFrameSize + 1
    if tempFrameSize == 29:
        baseline = sum(temp[i - 30:i])/30
        tempFrameSize = 0
    if temp[i] > (baseline + 0.3):
        hypoTemp = True
    if temp[i] < (baseline + 0.3):
        hypoTemp = False
    if hypoTemp == True:
        hypoTempIndex.append(i)
        tempReading.append(temp[i])
    if hypoTemp == False:
        hypoTempIndex.clear()
        tempReading.clear()
    if len(hypoTempIndex) > 6:
        hypoTempEmg = True
        print("Emergency")
    if len(hypoTempIndex) < 6:
        hypoTempEmg = False
    i = i + 1