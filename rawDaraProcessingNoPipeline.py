import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

##### Replicate these lines in Python console

# read in file with better column names
signalHR = pd.read_csv('hypo_data/31021HRGSR.csv', usecols=[0])

#pull out the V5 signal
HR = signalHR.to_numpy()
HR = np.delete(HR, -1)

plt.plot(HR)
plt.xlabel('Time (0.1 s)')
plt.ylabel('Analog Reading')

BPM = 0
i = 599
w = 0
while i < len(HR):
    avg = (sum(HR[(i-600):i]))/600
    bound = avg * 1.1
    if HR[i] > bound:
        BPM = BPM + 1
    w = w + 1
    if w == 600:
        BPM = 0
        w = 0
    i = i + 1
    print(BPM)