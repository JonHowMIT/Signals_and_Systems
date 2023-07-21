import time, csv, os, requests, copy, sys
from datetime import date

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
    Tf = float(sys.argv[1])
else:
    Tf = 10
print("Capturing time: "+str(Tf))

if len(sys.argv) > 2:
    filename = 'data/'+sys.argv[2]
else:
    today = date.today()
    for ii in range(0,100):
        filename = 'data/file_'+str(today)+'_'+str(ii)+'.csv'
        if(not os.path.isfile(filename)):
            break

DEG2RAD = np.pi/180.

global etime, theta, gyro, Uinp
etime = []
theta = []
gyro = []
Uinp = []
Tp = 0.25 # time between plots
Npts = 200 # incremental plot to show


def Serial_write(ser,U):
    # special bytes of a space and ! added for eps32 to find start
    if (type(U) == float):
        buf = bytearray(struct.pack("f", U))
    else:
        buf = bytearray(struct.pack("f", U[0]))
        for ii in range(1,len(U)):
            buf += bytearray(struct.pack("f", U[ii]))       
    ser.write(bytearray(b' ')+bytearray(b'!')+buf)

def Request_data(ser):
    # special bytes of a space and & to request data
    ser.write(bytearray(b' ')+bytearray(b'&'))

def Reset_imu(ser):
    # special bytes of a space and + to redo calib
    ser.write(bytearray(b' ')+bytearray(b'+'))

def Start_Logging(ser):
    # special bytes of a space and L 
    ser.write(bytearray(b' ')+bytearray(b'L'))

def Stop_Logging(ser):
    # special bytes of a space and S 
    ser.write(bytearray(b' ')+bytearray(b'S'))

def Stop_Done(ser):
    # special bytes of a space and D 
    ser.write(bytearray(b' ')+bytearray(b'D'))

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


def Ref_calc(etime):
        if (elapsed_time >= 0.75*Tf): 
            return 0.0
        elif (elapsed_time >= 0.5*Tf): 
            return 0.25
        elif (elapsed_time >= 0.25*Tf): 
            return -0.25
        else:
            return 0.0


def main():
    global etime, theta, gyro, Uinp

    try:  # close it if open - don't know that this is needed, but adds some robustness
        ser.close()
    except:
        pass

    port = ['/dev/cu.usbserial-110','/dev/cu.usbserial-10','/dev/cu.usbserial-210']
    for ii in range(len(port)):
        try:
            ser = serial.Serial(port[ii],baudrate=115200,timeout=0.001)
            break
        except:
            print(ii)
            if ii == len(port)-1:
                print('No ESP32')
                sys.exit(0)

    ser.flushInput()

    # PID gains to upload
    Kp = 300.0
    Kd = 1.5*Kp/5.0
    Ki = 30.0
    Serial_write(ser,np.array([Kp,Kd,Ki])) # K's
    time.sleep(1) # approx time of the ramp up
    temp = ser.readline().decode()
    print(temp[0:-2])
    while (temp[0:2] != str("Ki")):
        temp = ser.readline().decode()
        print(temp[0:-2])

    
    # start ESP logging loop    
    ser.write(bytearray(b'R')) # need to initiate the running on the ESP32
    time.sleep(10) # approx time of the ramp up
    Start_Logging(ser)
    time.sleep(0.1) # approx time of the ramp up
    Serial_write(ser,0.0) # ref is initially 0

    # prepare local logging file
    f = open(filename, 'w')
    writer = csv.writer(f)

    # prepare plots
    fig, ax = plt.subplots(figsize=(16,8))
    first = True # first time doing loop below 
    tstart = time.time()
    elapsed_time = time.time() - tstart
    tplot = tstart

    while elapsed_time <= Tf:
        Request_data(ser) # request data
        time.sleep(0.001) # slight pause for data to be sent
        data = Read_data(ser) # read that data
        if 0 <= data[6] < 10: # good data
            if first:
                first = False
                t0_ = data[0]
            etime = np.append(etime,data[0] - t0_) # esp32 time
            theta = np.append(theta,data[1]*180/np.pi)
            gyro = np.append(gyro,data[2])
            Uinp = np.append(Uinp,data[3])
            writer.writerow(data[0:4]) # locally store data

        if (time.time() > tplot + Tp): 
            drawnow(makeFig)
            tplot = time.time()

        Uinp = Ref_calc(elapsed_time)
        Serial_write(ser,Uinp) # change ref

        elapsed_time = time.time() - tstart

    Stop_Done(ser)

    # plot all data at the end        
    fig, ax = plt.subplots(figsize=(16,8))
    Npts = len(etime) - 1
    plt.plot(etime[-Npts:],theta[-Npts:],'b-',label='theta [rad]')
    plt.plot(etime[-Npts:],gyro[-Npts:],'r--',label='gyro [rad/s]')
    plt.plot(etime[-Npts:],Uinp[-Npts:],'g:',label='U/100')
    plt.legend(loc=3)
    plt.draw()
    val = input("<Hit Enter To Close>")
    plt.close(fig)

if __name__ == '__main__':
    main()