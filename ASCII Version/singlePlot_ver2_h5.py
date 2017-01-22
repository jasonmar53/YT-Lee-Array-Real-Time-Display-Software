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
 
baselineNum = str(mylist[0])  #baseline attenna being used
time_start = int(mylist[2])   #start range
calc = mylist[1]             #is it phase or amplitude
skipfirst = int(mylist[3])    #skip stuff?
skiplast = int(mylist[4])     #skip stuff?
time_end = int(mylist[5])     #finish range

print('ts', time_start)
print('ts', time_end)

lsbFind = 'lsb*' + baselineNum + '*'
usbFind = 'usb*' + baselineNum + '*'
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

view.setFixedHeight(800)
view.setFixedWidth(1250)
sa.setWidget(view)
sa.show()

wlist  = []
lsb = []
usb = []
print (lsbCheck)
print (len(lsbCheck))

for plotNum in range(len(lsbCheck)):
   labelStyle = {'color':'#000000', 'font-size':'10pt'}
   w1 = view.addPlot()
   wlist.append(w1)
   check = plotNum
   if check >= int(baselineNum):
      check += 1
   wlist[plotNum].getAxis('left').setLabel(baselineNum + '-' + str(check), **labelStyle)

   
   if baselineNum == 0:
      wlist[plotNum].getAxis('left').setLabel(baselineNum + '-' + str(plotNum + 1), **labelStyle)

   wlist[plotNum].setLabels(bottom = "Time(s)")
   wlist[0].setLabels(title = "Amplitude vs. Time")
   if calc  != "Amplitude":
      wlist[plotNum].setYRange(-180,180,padding=0)
      wlist[0].setLabels(title = "Phase vs. Time")
 
   sc1 = pg.ScatterPlotItem(name=baselineNum + '-' + str(plotNum + 1), size=5, pen=pg.mkPen(None), brush=pg.mkBrush(0, 0, 0, 255))
   sc2 = pg.ScatterPlotItem(name=baselineNum + '-' + str(plotNum + 1), size=5, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 0, 255))
   lsb.append(sc1)
   usb.append(sc2)
   wlist[plotNum].addItem(sc1)
   wlist[plotNum].addItem(sc2)
   view.nextRow()
   

time_start = time_start - 1  
# time_end = time_end - time_start
print ('time start',time_start)
print ('time end',time_end)


for plotNum in range(len(lsbCheck)):

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




   counter = time_start
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
         rlist2 = ilist2[skipfirst:]

      if skiplast > 0:
         ilist = ilist[:-skiplast]
         rlist = rlist[:-skiplast]
    
         ilist2 = ilist2[:-skiplast]
         rlist2 = rlist2[:-skiplast]

      R = calc_total(rlist)
      I = calc_total(ilist)
      R2 = calc_total(rlist2)
      I2 = calc_total(ilist2)
      if calc == "Amplitude":
         point = calc_Amplitude(R, I)
         point2 = calc_Amplitude(R2, I2)
      else: 
         point = calc_Phase(R, I) 
         point2 = calc_Phase(R2, I2)
      x = [counter]
      y = [point]
      z = [point2]
      lsb[plotNum].addPoints(x, y)
      usb[plotNum].addPoints(x, z)

 
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
