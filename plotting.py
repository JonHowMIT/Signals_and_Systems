import time, csv, os, requests, copy, sys

import numpy as np
from numpy.linalg import norm
from numpy.random import randn
from numpy import eye, array, asarray, exp
float_formatter = "{:.4f}".format
np.set_printoptions(formatter={'float': '{: 6.4f}'.format})
from math import sqrt

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib import rcParams
rcParams["font.serif"] = "cmr14"
rcParams['savefig.dpi'] = 300
rcParams["figure.dpi"] = 100
rcParams.update({'font.size': 18})
rcParams['axes.grid'] = True
rcParams['lines.linewidth'] = 2.0
params = {'legend.fontsize': 12,
          'legend.handlelength': 2}
plt.rcParams["figure.figsize"] = (8,5)
plt.rcParams.update(params)

import serial
from drawnow import *
import struct
 
# total arguments
if len(sys.argv) > 1:
    Nplot = int(sys.argv[1])
else:
    Nplot = 1000
print("Capturing points: "+str(Nplot))
Npts = min(200,Nplot)


if len(sys.argv) > 2:
    filename = sys.argv[2]
else:
    filename = 'file1.csv'

DEG2RAD = np.pi/180.

global etime, theta, gyro, Uinp
etime = []
theta = []
gyro = []
Uinp = []

def Serial_write(ser,U):
    # special bytes of a space and ! added for eps32 to find start
    buf = struct.pack('%sf' % len(U), *U)
    ser.write(bytearray(b' ')+bytearray(b'!')+buf)

def Request_data(ser):
    # special bytes of a space and & to request data
    ser.write(bytearray(b' ')+bytearray(b'&'))

def Reset_imu(ser):
    # special bytes of a space and + to redo calib
    ser.write(bytearray(b' ')+bytearray(b'+'))

def smootherstep(edge0, edge1, x): 
    # Scale, and clamp x to 0..1 range
    x = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    # Evaluate polynomial
    return x * x * x * (x * (x * 6 - 15) + 10)

def Read_data(ser):
    nvar = 5 # 4 floats and checksum
    str_len = 4*nvar
    found_header = False
    tic = time.time()
    data = np.zeros(7)
    for kk in range(str_len+1):     # look for header
        if (ser.read(1) == b'&'):
            if (ser.read(1) == b'!'):
                found_header = True
                break
    if found_header:
        rbytes = ser.read(str_len)
        if (len(rbytes) == str_len):
            try:
                for ii in range(nvar):
                    data[ii] = struct.unpack('f',rbytes[4*ii:4*(ii+1)])[0]
                data[5] = time.time() - tic
                data[6] = np.abs(data[4] - np.sum(data[0:4])) # checksum
                return data
            except:
                data[6] = -1
                return data
        else:
            data[6] = -2
        return data # will be zero if 
    data[6] = -3
    return data

def makeFig():
    plt.plot(etime[-Npts:],theta[-Npts:],'b-',label='theta [rad]')
    plt.plot(etime[-Npts:],gyro[-Npts:],'r--',label='gyro [rad/s]')
    plt.plot(etime[-Npts:],Uinp[-Npts:],'g:',label='U/100')
    plt.legend(loc=3)

def main():
    global etime, theta, gyro, Uinp

    try:
        ser.close()
    except:
        try:
            port = '/dev/cu.usbserial-110'
            ser = serial.Serial(port,baudrate=115200,timeout=0.001)
        except:
            port = '/dev/cu.usbserial-10'
            ser = serial.Serial(port,baudrate=115200,timeout=0.001)

    
    ser.flushInput()
    if 0:
        ser.write(bytearray(b'R'))
        time.sleep(10)

    f = open(filename, 'w')
    writer = csv.writer(f)

    fig, ax = plt.subplots(figsize=(16,8))
    for ii in range(Nplot):
        Request_data(ser)
        time.sleep(0.001)
        data = Read_data(ser)
        if data[6] > 0: # good data
            etime = np.append(etime,data[0])
            theta = np.append(theta,data[1])
            gyro = np.append(gyro,data[2]*np.pi/180.)
            Uinp = np.append(Uinp,data[3]/100)
            writer.writerow(data[0:4])
        if (ii%25 == 0): 
            drawnow(makeFig)

    # plot all data at the end        
    fig, ax = plt.subplots(figsize=(16,8))
    plt.plot(etime[-(Nplot-10):],theta[-(Nplot-10):],'b-',label='theta [rad]')
    plt.plot(etime[-(Nplot-10):],gyro[-(Nplot-10):],'r--',label='gyro [rad/s]')
    plt.plot(etime[-(Nplot-10):],Uinp[-(Nplot-10):],'g:',label='U/100')
    plt.legend(loc=3)
    plt.show()

if __name__ == '__main__':
    main()