import numpy as np

def my_func(t,fs):
    y = np.sin(2*np.pi*fs*t)
    return y