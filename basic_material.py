import shutil, sys, os.path, math, time

import numpy as np
float_formatter = "{:.4f}".format
np.set_printoptions(formatter={'float': '{: 8.3f}'.format})

#%matplotlib inline
import matplotlib
import matplotlib.cm as cm
from matplotlib.cm import get_cmap
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib import rcParams
rcParams["font.serif"] = "cmr14"
rcParams['savefig.dpi'] = 300
rcParams["figure.dpi"] = 100
rcParams.update({'font.size': 18})
rcParams['axes.grid'] = True
rcParams['lines.linewidth'] = 2.0
 
#font = {'family': 'arial','color':  'darkred','weight': 'normal','size': 18}
#plt.rcParams['figure.figsize'] = [12, 8.0]
#plt.rcParams['figure.dpi'] = 300
#plt.rcParams.update({"axes.grid" : True, "grid.color": "grey"})
#plt.rcParams['grid.linestyle'] = ':'


from IPython.display import display, Markdown
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from IPython.display import display
import sympy
import sympy as sym

#from pyomo.environ import *

import scipy
from scipy import optimize 
from scipy.optimize import fsolve, line_search, minimize, LinearConstraint, NonlinearConstraint, Bounds

import warnings
warnings.filterwarnings("ignore", message="delta_grad == 0.0. Check if the approximated function is linear.")

from platform import python_version
print("Running Python:",python_version())