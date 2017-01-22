from pyqtgraph.Qt import  QtCore
import numpy as np
import pyqtgraph as pg
import sys
import pandas
import math
import os
import glob
import h5py
from PyQt4 import QtGui



def insensitive_glob(pattern):
    def either(c):
        return '[%s%s]'%(c.lower(),c.upper()) if c.isalpha() else c
    return glob.glob(''.join(map(either,pattern)))
 
def file_len(fname):
    j = 0
    with open(fname) as f:
        for j, l in enumerate(f):
            pass
    return j + 1
 
def calc_Phase(x, y):
    if not x:
        return
    if not y:
        return
    return (np.arctan2(x, y)*(180/np.pi))
 
def calc_total(alist):
    return np.mean(alist)

def calc_phaseClosure(val1, val2, val3):
    if val1 is None or val2 is None or val3 is None:
       return
    total = val1 + val2 - val3
    if total > 180:
       total -= 360
    elif total < -180:
       total += 360
    return total
 
def calc_Amplitude(x, y):
    if not x:
       return
    if not y:
       return
    x2 = x*x
    y2 = y*y
    z = x2+y2
    w = math.sqrt(z)
    return w
 
mylist = sys.argv[1:]
for pos, i in enumerate(mylist):
  print("At ", pos, " the item is ", i)
 
time_start = int(mylist[0])   #start range
skipfirst = int(mylist[1])    #skip stuff?
skiplast = int(mylist[2])     #skip stuff?
time_end = int(mylist[3])     #finish range

os.chdir('/home/corr/4ant1k/reduction')

lsbFind = '*lsb.cross.h5'
usbFind = '*usb.cross.h5'
lsbCheck = insensitive_glob(lsbFind)
usbCheck = insensitive_glob(usbFind)
lsbCheck.sort()
usbCheck.sort()



pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
app = QtGui.QApplication([])
sa = pg.QtGui.QScrollArea() #Makes it possible to scroll
view = pg.GraphicsLayoutWidget() #displaying multiple plots
#win = pg.GraphicsWindow(title="Graph: for baselines" + baselineNum)
#win.resize(1000,600)

view.setFixedHeight(3000)
view.setFixedWidth(1000)
sa.setWidget(view)
sa.show()

wlist  = []
lsb = []
usb = []


#creates correct number of plots should be 15
for plotNum in range(15):
   labelStyle = {'color':'#000000', 'font-size':'10pt'}
   w1 = view.addPlot()
   wlist.append(w1)
   if(plotNum < 5):
      wlist[plotNum].getAxis('left').setLabel('0-1-' + str(plotNum + 2), **labelStyle)
   elif(plotNum < 9):
      wlist[plotNum].getAxis('left').setLabel('1-2-' + str(plotNum - 2), **labelStyle)
   elif(plotNum < 12):
      wlist[plotNum].getAxis('left').setLabel('2-' + str(plotNum - 6) + '-'  +str(plotNum - 5), **labelStyle)
   elif(plotNum < 14):
      wlist[plotNum].getAxis('left').setLabel('3-' + str(plotNum - 8) + '-' + str(plotNum - 7), **labelStyle)
   else:
      wlist[plotNum].getAxis('left').setLabel('4-5-6', **labelStyle)
   wlist[plotNum].setLabels(bottom = "Time(s)")
   wlist[0].setLabels(title = "Phase Closure")
   wlist[plotNum].setYRange(-180,180,padding=0)
 
   sc1 = pg.ScatterPlotItem(name=None, size=3, pen=pg.mkPen(None), brush=pg.mkBrush(0, 0, 0, 255))
   sc2 = pg.ScatterPlotItem(name=None, size=3, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 0, 255))
   lsb.append(sc1)
   usb.append(sc2)
   wlist[plotNum].addItem(sc1)
   wlist[plotNum].addItem(sc2)
   view.nextRow()
   

lsbPhaseStorage = []
usbPhaseStorage = []

#makes arrays of phase information that's calculated then stored into lsb/usbPhaseStorage
for plotNum in range(len(lsbCheck)):
   lsbPhaseStorage.append([])
   usbPhaseStorage.append([])
   counter = time_start
   low = h5py.File(lsbCheck[plotNum], 'r')
   upp = h5py.File(usbCheck[plotNum], 'r')

   realVal = low.get('/fullData/real')
   imagVal = low.get('/fullData/imag')

   realVal2 = upp.get('/fullData/real')
   imagVal2 = upp.get('/fullData/imag')

   thislistr = np.array(realVal)
   thislisti = np.array(imagVal)

   thislistr2 = np.array(realVal2)
   thislisti2 = np.array(imagVal2)

   thislistr = np.transpose(thislistr)
   thislisti = np.transpose(thislisti)

   thislistr2 = np.transpose(thislistr2)
   thislisti2 = np.transpose(thislisti2)

   #assumes that there's a same number of lsb files as usb files here
   while counter < time_end:
      counter += 1
      ilist = thislisti[counter]
      rlist = thislistr[counter]
      ilist2 = thislisti2[counter]
      rlist2 = thislistr2[counter]

      if skipfirst > 0:
         ilist = ilist[skipfirst:]
         rlist = rlist[skipfirst:]
 
         ilist2 = ilist2[skipfirst:]
         rlist2 = rlist2[skipfirst:]

      if skiplast > 0:
         ilist = ilist[:-skiplast]
         rlist = rlist[:-skiplast]
    
         ilist2 = ilist2[:-skiplast]
         rlist2 = rlist2[:-skiplast]

      R = calc_total(rlist)
      I = calc_total(ilist)

      R2 = calc_total(rlist2)
      I2 = calc_total(ilist2)
      
      p1 = calc_Phase(R, I)
      p2 = calc_Phase(R2, I2)
      lsbPhaseStorage[plotNum].append(calc_Phase(R, I))
      usbPhaseStorage[plotNum].append(calc_Phase(R2, I2))
 
#at this point we should have 21 sets of phase data x 2 for lsb and usb


for plotNum in range(15):
   counter = time_start

   for valNum in range(time_end - time_start):
      if plotNum < 5:
         y1 = calc_phaseClosure(lsbPhaseStorage[0][valNum], lsbPhaseStorage[plotNum + 6][valNum], lsbPhaseStorage[plotNum + 1][valNum])
         y2 = calc_phaseClosure(usbPhaseStorage[0][valNum], usbPhaseStorage[plotNum + 6][valNum], usbPhaseStorage[plotNum + 1][valNum]) 
      elif plotNum < 9:
         y1 = calc_phaseClosure(lsbPhaseStorage[6][valNum], lsbPhaseStorage[plotNum + 6][valNum], lsbPhaseStorage[plotNum + 2][valNum])
         y2 = calc_phaseClosure(usbPhaseStorage[6][valNum], usbPhaseStorage[plotNum + 6][valNum], usbPhaseStorage[plotNum + 2][valNum])

      elif plotNum < 12:
         if plotNum == 9:
            y1 = calc_phaseClosure(lsbPhaseStorage[plotNum + 2][valNum], lsbPhaseStorage[plotNum + 6][valNum], lsbPhaseStorage[plotNum + 3][valNum])
            y2 = calc_phaseClosure(usbPhaseStorage[plotNum + 2][valNum], usbPhaseStorage[plotNum + 6][valNum], usbPhaseStorage[plotNum + 3][valNum])
         else:
            y1 = calc_phaseClosure(lsbPhaseStorage[plotNum + 2][valNum], lsbPhaseStorage[plotNum + 8 + plotNum%10][valNum], lsbPhaseStorage[plotNum + 3][valNum])
            y2 = calc_phaseClosure(usbPhaseStorage[plotNum + 2][valNum], usbPhaseStorage[plotNum + 8 + plotNum%10][valNum], usbPhaseStorage[plotNum + 3][valNum])

      elif plotNum < 14:
         y1 = calc_phaseClosure(lsbPhaseStorage[plotNum + 3][valNum], lsbPhaseStorage[plotNum + 6 + plotNum%12][valNum], lsbPhaseStorage[plotNum + 4][valNum])
         y2 = calc_phaseClosure(usbPhaseStorage[plotNum + 3][valNum], usbPhaseStorage[plotNum + 6 + plotNum%12][valNum], usbPhaseStorage[plotNum + 4][valNum])

      else:
         y1 = calc_phaseClosure(lsbPhaseStorage[18][valNum], lsbPhaseStorage[20][valNum], lsbPhaseStorage[19][valNum])
         y2 = calc_phaseClosure(usbPhaseStorage[18][valNum], usbPhaseStorage[20][valNum], usbPhaseStorage[19][valNum])
      x = [counter]
      y = [y1]
      z = [y2]
      lsb[plotNum].addPoints(x, y)
      usb[plotNum].addPoints(x, z)
      counter += 1

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
