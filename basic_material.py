from platform import python_version
print("Running Python:",python_version())

import shutil, sys, os.path, math, time, subprocess, random

import numpy as np
from numpy import logspace, linspace
float_formatter = "{:.4f}".format
np.set_printoptions(formatter={'float': '{: 8.3f}'.format})

import matplotlib
import matplotlib.cm as cm
try:
    from matplotlib.cm import get_cmap
except:
    from matplotlib.pyplot import get_cmap
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, savefig
from matplotlib import gridspec
from matplotlib import rcParams
rcParams["font.serif"] = "cmr14"
rcParams.update({'font.size': 18})
plt.rcParams['figure.figsize'] = [8, 5.0]
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.grid'] = True
plt.rcParams["figure.autolayout"] = True

try:
    import sympy as sym
except:
    subprocess.Popen('python3 -m pip install sympy', shell=True)    
    import sympy as sym
from sympy import lambdify, oo, Symbol, integrate, Heaviside, plot, Piecewise
from sympy import exp, plot, sin, cos, printing, init_printing, simplify
from sympy.testing.pytest import ignore_warnings
print("Running Sympy:",sym.__version__)

try:
    from scipy import signal
except:
    subprocess.Popen('python3 -m pip install scipy', shell=True)    
    from scipy.fft import fft, fftfreq, fftshift, ifft

try:
    import IPython.display as ipd
except Exception as e2:
    print(e2)
    subprocess.Popen('python3 -m pip install IPython', shell=True)    
    import IPython.display as ipd

from IPython.display import display, Markdown
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

SMALL_SIZE = 10
MEDIUM_SIZE = 14
BIGGER_SIZE = 18

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

import warnings
warnings.filterwarnings("ignore")

def nicegrid(ax = plt):
    try: #if np.size(ax) > 1
        for ii in np.arange(len(ax)):
            ax[ii].grid(True, which='major', color='#666666', linestyle=':')
            ax[ii].grid(True, which='minor', color='#999999', linestyle=':', alpha=0.2)
            try:
                ax[ii].axhline(y=0, color='k', linestyle='--',lw=1)
            except:
                ax[ii].axhline(y=1, color='k', linestyle='--',lw=1)
            ax[ii].minorticks_on()
    except:
        ax.grid(True, which='major', color='#666666', linestyle=':')
        ax.grid(True, which='minor', color='#999999', linestyle=':', alpha=0.2)
        try:
            ax.axhline(y=0, color='k', linestyle='--',lw=1)
        except:
            ax.axhline(y=1, color='k', linestyle='--',lw=1)
            ax.minorticks_on()
            
def caption(txt,fig, xloc=0.5, yloc=-0.1):
    fig.text(xloc, yloc, txt, ha='center',size=MEDIUM_SIZE,color='blue')

if os.path.isdir("./data/"):
    pass
else:
    os.mkdir("./data")

if os.path.isdir("./figs/"):
    pass
else:
    os.mkdir("./figs")

try:
    import google.colab
    IN_COLAB = True
    print("\nOperating on Google Collab \n")
except:
    IN_COLAB = False

try: 
    from simple_colors import *
    colors = ['k','b','r','m','g','Brown','DarkBlue','Tomato','Violet', 'Tan','Salmon','Pink',
    'SaddleBrown', 'SpringGreen', 'RosyBrown','Silver',]
except:
    colors = ['k','b','r','m','g']

r2d = 180/np.pi

#text1 = "Clear that response closely matches input - i.e. input passes through the system"
#plt.text(0., -0.15, text1, horizontalalignment='left',verticalalignment='center',transform=ax.transAxes,bbox=dict(facecolor='blue', alpha=0.2))

try:
    from colorama import Fore, Style
except:
    subprocess.Popen('python3 -m pip install colorama', shell=True) 
    from colorama import Fore, Style

# frequently used functions
def U(t):
    u = np.zeros_like(t)
    u[t >= 0] = 1
    return u

def tri(t, p = 1):   # tri(t/p)
    if np.isscalar(t):
        if t <= -p or t > p:
            return 0
        if t < 0:
            return 1 + t/p
        else:
            return 1 - t/p
    else:  
        y = np.zeros_like(t)
        II = np.where((-1.0 < t/p)*(t/p <= 0.0))
        y[II] = 1 + t[II]/p
        II = np.where((0.0 < t/p)*(t/p <= 1.0))
        y[II] = 1 - t[II]/p
        return y  
    
def rect(t,p = 1):  # rect(t/p)
    if np.isscalar(t):
        if t <= -p/2 or t > p/2:
            return 0
        else:
            return 1
    else:
        y = np.zeros_like(t)
        y[np.where((-1/2 < t/p)*(t/p <= 1/2))] = 1.0
        return y  