import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

##### Replicate these lines in Python console

# read in file with better column names
signalGSR = pd.read_csv('hypo_data/31121HRGSR.csv', usecols=[1])

GSR = signalGSR.to_numpy()
GSR = np.delete(GSR, -1)
smoothGSR = savgol_filter(GSR, 2001, 3)
t=300
GSRflag = False
for i in range(0, len(smoothGSR), 300):
    subGSR = [sum(smoothGSR[i:i+t])/t]
    grad = abs(np.gradient(subGSR))
    hypoSignatures = np.array([])
    if grad[i] >= 0.025:
        valid_indicies = np.append(hypoSignatures, i)
        GSRflag = True
    else:
        GSRflag = False