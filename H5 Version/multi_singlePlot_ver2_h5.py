from pyqtgraph.Qt import  QtCore
import numpy as np
import pyqtgraph as pg
import sys
import pandas
import math
import os
import glob
import h5py
import time
from PyQt4 import QtGui
from multiprocessing import Process, Queue

def calculateAllAmps(q, ArrayR, ArrayI, begin, end, skipfirst, skiplast):
   ampArray = []
   timeArray = []
   while begin < end:
      begin += 1
      timeArray.append(begin)

      ilist = ArrayI[begin]
      rlist = ArrayR[begin]

      if skipfirst > 0:
         ilist = ilist[skipfirst:]
         rlist = rlist[skipfirst:]

      if skiplast > 0:
         ilist = ilist[:-skiplast]
         rlist = rlist[:-skiplast]

      R = calc_total(rlist)
      I = calc_total(ilist)

      point = calc_Amplitude(R, I)
      ampArray.append(point)
   q.put(ampArray)
   q.put(timeArray)

def calculateAllPhases(q, ArrayR, ArrayI, begin, end, skipfirst, skiplast):
   phaseArray = []
   timeArray = []
   while begin < end:
      begin += 1
      timeArray.append(begin)

      ilist = ArrayI[begin]
      rlist = ArrayR[begin]

      if skipfirst > 0:
         ilist = ilist[skipfirst:]
         rlist = rlist[skipfirst:]

      if skiplast > 0:
         ilist = ilist[:-skiplast]
         rlist = rlist[:-skiplast]

      R = calc_total(rlist)
      I = calc_total(ilist)

      point = calc_Phase(R, I)
      phaseArray.append(point)
   q.put(phaseArray)
   q.put(timeArray)



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
    return (np.arctan2(y, x)*(180/np.pi))
 
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
os.chdir('/home/corr/ytla/reduction')

lsbFind = '*corr1k*' + baselineNum + '*lsb.cross.h5'
usbFind = '*corr1k*' + baselineNum + '*usb.cross.h5'
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

for plotNum in range(len(lsbCheck)):
   labelStyle = {'color':'#000000', 'font-size':'10pt'}
   w1 = view.addPlot()
   wlist.append(w1)
   check = plotNum

   if calc == "Amplitude":
      if check >= int(baselineNum):
         check += 1
      wlist[plotNum].getAxis('left').setLabel(baselineNum + '-' + str(check) + " (counts)", **labelStyle)

   
      if baselineNum == 0:
         wlist[plotNum].getAxis('left').setLabel(baselineNum + '-' + str(plotNum + 1) + " (counts)", **labelStyle)

      wlist[plotNum].setLabels(bottom = "Time")
      wlist[0].setLabels(title = "Amplitude vs. Time")
   else:
      if check >= int(baselineNum):
         check += 1
      wlist[plotNum].getAxis('left').setLabel(baselineNum + '-' + str(check) + " (degrees)", **labelStyle)

   
      if baselineNum == 0:
         wlist[plotNum].getAxis('left').setLabel(baselineNum + '-' + str(plotNum + 1) + " (counts)", **labelStyle)

      wlist[plotNum].setLabels(bottom = "Time")

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

   q1 = Queue()
   q2 = Queue()
   q3 = Queue()
   q4 = Queue()

   difference = int((time_end - time_start)/2)
   
   if calc == "Amplitude":
      pl1 = Process(target=calculateAllAmps, args=(q1, thislistr, thislisti, time_start, time_start + difference, skipfirst, skiplast))
      pl2 = Process(target=calculateAllAmps, args=(q2, thislistr, thislisti, time_start + difference, time_end, skipfirst, skiplast))
      pu1 = Process(target=calculateAllAmps, args=(q3, thislistr2, thislisti2, time_start, time_start + difference, skipfirst, skiplast))
      pu2 = Process(target=calculateAllAmps, args=(q4, thislistr2, thislisti2, time_start + difference, time_end, skipfirst, skiplast))

#calculateAllAmps
   else:
      pl1 = Process(target=calculateAllPhases, args=(q1, thislistr, thislisti, time_start, time_start + difference, skipfirst, skiplast))
      pl2 = Process(target=calculateAllPhases, args=(q2, thislistr, thislisti, time_start + difference, time_end, skipfirst, skiplast))
      pu1 = Process(target=calculateAllPhases, args=(q3, thislistr2, thislisti2, time_start, time_start + difference, skipfirst, skiplast))
      pu2 = Process(target=calculateAllPhases, args=(q4, thislistr2, thislisti2, time_start + difference, time_end, skipfirst, skiplast))
   pl1.start()
   pl2.start()
   pu1.start()
   pu2.start()

   ly1 = q1.get()
   lx1 = q1.get()
   ly2 = q2.get()
   lx2 = q2.get()

   x = list(range(time_start, time_start + difference))
   x2 = list(range(time_start + difference, time_end))

   uy1 = q3.get()
   ux1 = q3.get()
   uy2 = q4.get()
   ux2 = q4.get()

   lsb[plotNum].addPoints(lx1, ly1)
   lsb[plotNum].addPoints(lx2, ly2)
   usb[plotNum].addPoints(ux1, uy1)
   usb[plotNum].addPoints(ux2, uy2)

 
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
