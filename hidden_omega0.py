import random
# Actual Freq of signal
omega0 = random.uniform(omega_lower_bound+1, omega_upper_bound-1) # rads/sec
# actual phase offset
phi_true = random.uniform(0,1)*(2*np.pi)  # varied phase offset

f0 = omega0/(2*np.pi) # Hz
T0 = 1/f0  # period in secs