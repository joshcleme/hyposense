import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

##### Replicate these lines in Python console

# read in file with better column names
signalHR = pd.read_csv('hypo_data/31021HRGSR.csv', usecols=[0])

#pull out the V5 signal
HR = signalHR.to_numpy()
HR = np.delete(HR, -1)

### pass data through LOW PASS FILTER (fs=250Hz, fc=15, N=6) ###
low_passHR = np.convolve(HR, [0.023834522, 0.093047634, 0.232148599, 0.301938491, 0.232148599, 0.093047634, 0.023834522])

### pass data through HIGH PASS FILTER (fs=250Hz, fc=5Hz, N=6) to create BAND PASS result ###
band_passHR = np.convolve(low_passHR, [-0.000798178, -0.003095487, -0.007692586, 0.989209446, -0.007692586, -0.003095487, -0.000798178])

### pass data through weighter differiator
diffHR = np.convolve(band_passHR, [1, 2, -2, -1])   #I think this is incorrect as it does not look "forward" but should work

## pass data through square function
squaredHR = diffHR * diffHR

plt.plot(squaredHR)
plt.xlabel('Time (0.1 s)')
plt.ylabel('Analog Reading')

BPM = 0
w = 0
i = 59
while i < len(squaredHR):
    avg = (sum(squaredHR[(i-60):i]))/60
    averageWeightedLower = avg * 0.70
    averageWeightedHigher = avg * 1.10
    if squaredHR[i-30] >= averageWeightedLower and squaredHR[i-30] <= averageWeightedHigher:
        BPM = BPM + 1
    w = w + 1
    if w == 600:
        print(BPM)
        BPM = 0
        w = 0
    i = i + 1