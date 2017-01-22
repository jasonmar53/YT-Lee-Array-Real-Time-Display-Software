from pyqtgraph.Qt import QtGui, QtCore
import sys
import re
import glob
import os
import pyqtgraph as pg
import numpy as np
import time
import pandas
import subprocess
import argparse
import gc
import h5py
from tkinter import *
from tkinter import messagebox

arr = np.array([[1, 2, 3],[4, 5, 6]])
print(arr.shape)
print(arr)
print("array 0", arr[0])
np.delete(arr, [0], axis=0)
print(arr.shape) 
print(arr)
