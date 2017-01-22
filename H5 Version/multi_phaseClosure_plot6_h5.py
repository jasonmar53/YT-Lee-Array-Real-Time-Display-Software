from pyqtgraph.Qt import  QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import sys
import pandas
import math
import os
import glob
import h5py
from multiprocessing import Process, Queue

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


def calc_phaseClosure(val1, val2, val3):
    if val1 is None or val2 is None or val3 is None:
       return
    total = val1 + val2 - val3
    if total > 180:
       total -= 360
    elif total < -180:
       total += 360
    return total
     
def calculateAllPhaseC(q, lphase1, lphase2, lphase3, uphase1, uphase2, uphase3, begin, end): 
    upperC = []
    lowerC = []
    i = 0
    print(len(lphase1))
    while i < (end - begin):
       lowerC.append(calc_phaseClosure(lphase1[i], lphase2[i], lphase3[i]))
       upperC.append(calc_phaseClosure(uphase1[i], uphase2[i], uphase3[i]))
       i += 1
    q.put(lowerC)
    q.put(upperC)
       

def calculateAllPhases(q, ArrayR, ArrayI, begin, end, skipfirst, skiplast):
   phaseArray = []
   while begin < end:
      begin += 1
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

 
mylist = sys.argv[1:]
for pos, i in enumerate(mylist):
  print("At ", pos, " the item is ", i)
 
time_start = int(mylist[0])   #start range
skipfirst = int(mylist[1])    #skip stuff?
skiplast = int(mylist[2])     #skip stuff?
time_end = int(mylist[3])     #finish range
os.chdir('/home/corr/ytla/reduction')

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

view.setFixedHeight(800)
view.setFixedWidth(1000)
sa.setWidget(view)
sa.show()

wlist  = []
lsb = []
usb = []


#creates correct number of plots should be 15
labelStyle = {'color':'#000000', 'font-size':'10pt'}
w1 = view.addPlot()
wlist.append(w1)
wlist[0].getAxis('left').setLabel('0-1-2' + " (degrees)", **labelStyle)
view.nextRow()
w1 = view.addPlot()
wlist.append(w1)
wlist[1].getAxis('left').setLabel('0-1-3' + "(degrees)", **labelStyle)
view.nextRow()
w1 = view.addPlot()
wlist.append(w1)
wlist[2].getAxis('left').setLabel('1-2-3' + "(degrees)", **labelStyle)
view.nextRow()

for plotNum in range(3):
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
   q1 = Queue()
   q2 = Queue()
   q3 = Queue()
   q4 = Queue()

   difference = int((time_end - time_start)/2)
  
   pl1 = Process(target=calculateAllPhases, args=(q1, thislistr, thislisti, time_start, time_start + difference, skipfirst, skiplast))
   pl2 = Process(target=calculateAllPhases, args=(q2, thislistr, thislisti, time_start + difference, time_end, skipfirst, skiplast))
   pu1 = Process(target=calculateAllPhases, args=(q3, thislistr2, thislisti2, time_start, time_start + difference, skipfirst, skiplast))
   pu2 = Process(target=calculateAllPhases, args=(q4, thislistr2, thislisti2, time_start + difference, time_end, skipfirst, skiplast))
   pl1.start()
   pl2.start()
   pu1.start()
   pu2.start()
 

   print("step 1, ", len(lsbPhaseStorage[plotNum]))  
   lsbPhaseStorage[plotNum].extend(q1.get())
   print("step 2, ", len(lsbPhaseStorage[plotNum])) 
   lsbPhaseStorage[plotNum].extend(q2.get())
   print("step 3, ", len(lsbPhaseStorage[plotNum])) 
   usbPhaseStorage[plotNum].extend(q3.get())
   usbPhaseStorage[plotNum].extend(q4.get()) 
   
#at this point we should have 6 sets of phase data x 2 for lsb and usb

counter = time_start


p1 = Process(target=calculateAllPhaseC, args=(q1, lsbPhaseStorage[0], lsbPhaseStorage[3], lsbPhaseStorage[1],
                                                     usbPhaseStorage[0], usbPhaseStorage[3], usbPhaseStorage[1],
                                                     time_start, time_end))
   #y1 = [calc_phaseClosure(lsbPhaseStorage[0][valNum], lsbPhaseStorage[3][valNum], lsbPhaseStorage[1][valNum])]
   #y2 = [calc_phaseClosure(usbPhaseStorage[0][valNum], usbPhaseStorage[3][valNum], usbPhaseStorage[1][valNum])]

p2 = Process(target=calculateAllPhaseC, args=(q2, lsbPhaseStorage[0], lsbPhaseStorage[4], lsbPhaseStorage[2],
                                                  usbPhaseStorage[0], usbPhaseStorage[4], usbPhaseStorage[2],
                                                  time_start, time_end))

   #z1 = [calc_phaseClosure(lsbPhaseStorage[0][valNum], lsbPhaseStorage[4][valNum], lsbPhaseStorage[2][valNum])]
   #z2 = [calc_phaseClosure(usbPhaseStorage[0][valNum], usbPhaseStorage[4][valNum], usbPhaseStorage[2][valNum])]

p3 = Process(target=calculateAllPhaseC, args=(q3, lsbPhaseStorage[3], lsbPhaseStorage[5], lsbPhaseStorage[4],
                                                  usbPhaseStorage[3], usbPhaseStorage[5], lsbPhaseStorage[4],
                                                  time_start, time_end))

   #w1 = [calc_phaseClosure(lsbPhaseStorage[3][valNum], lsbPhaseStorage[5][valNum], lsbPhaseStorage[4][valNum])]
   #w2 = [calc_phaseClosure(usbPhaseStorage[3][valNum], usbPhaseStorage[5][valNum], usbPhaseStorage[4][valNum])]

p1.start()
p2.start()
p3.start()

x = list(range(time_start, time_end))
y1 = q1.get()
y2 = q1.get()

z1 = q2.get()
z2 = q2.get()

w1 = q3.get()
w2 = q3.get()
  
lsb[0].addPoints(x, y1)
usb[0].addPoints(x, y2)
lsb[1].addPoints(x, z1)
usb[1].addPoints(x, z2)
lsb[2].addPoints(x, w1)
usb[2].addPoints(x, w2)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
