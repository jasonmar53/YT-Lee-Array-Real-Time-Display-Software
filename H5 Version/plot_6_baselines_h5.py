#plot 6 baseline code
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


'''
Widgets Buttons Documentation Begins 
-------------------------------------------------------------------------------------------

Plotting Functions:

SingleplotBtn() checks which plotting type is chosen in the drop box then the appropriate function is ran

PhaseCplot() plots the phase phase closure, no antenna number needs to be chosen

SinglePlot() plots either the amplitude or phase with every baseline combination that has the antenna number chosen within it

'''
global numFiles, text2, switch

#error checks for missing UI arguments then runs phase closure code
def phaseCPlot():
    alist = []
    position = 0
    if not (text2.text().isdigit()):
       root = Tk()
       T = Text(root, height=5, width=50, font = ('Times', '15', 'bold'), wrap = WORD)
       T.pack()
       T.insert(INSERT, "Argument Error: Please type a valid Start Time")
       mainloop()
       return
    if not(text3.text().isdigit()):
       root = Tk()
       T = Text(root, height=5, width=50, font = ('Times', '15', 'bold'), wrap = WORD)
       T.pack()
       T.insert(INSERT, "Argument Error: Please type a valid End Time")
       mainloop()
       return

    time_start = int(text2.text())
    time_end = int(text3.text())
    found = "False"
    lower = "False"
    if time_start < 0 or time_start > time_end:
       print("Time Error: Not Possible To Have A Negative Time.")
       root = Tk()
       T = Text(root, height=5, width=50, font = ('Times', '15', 'bold'), wrap = WORD)
       T.pack()
       T.insert(INSERT, "Argument Error: Time Error: not possible to have a negative time argument")
       mainloop()
       return
    if time_end >= counter[0]:
       print("Time Error: We Have Not Recorded For More Than ", counter[0] - 1, " Seconds.")
       root = Tk()
       T = Text(root, height=5, width=50, font = ('Times', '15', 'bold'), wrap = WORD)
       T.pack()
       string = "Time Error: Max available end time is " + str(counter[0] - 1)  + " seconds"
       T.insert(INSERT, string)
       mainloop()

       return
    alist.append(text2.text())
    sf = str(skipfirst)
    sl = str(skiplast)
    alist.append(sf)
    alist.append(sl)
    alist.append(text3.text())
    print (alist)
    subprocess.Popen(["python3", "/home/corr/Desktop/jmarr/version2_h5/multi_phaseClosure_plot6_h5.py"] + alist)

#checks which type of graph was chosen by the user
def singlePlotBtn():
   if plotOptions.currentText() == "Choose type of plot":
      print("Please choose which type of plot in the drop down box")
      root = Tk()
      T = Text(root, height=5, width=50, font = ('Times', '15', 'bold'), wrap = WORD)
      T.pack()
      T.insert(INSERT, "Argument Error: Please choose the type of plot from the drop down box")
      mainloop()
      return
   elif plotOptions.currentText() == "Phase Closure":
      phaseCPlot()
   else:
      singlePlot()

#errors check the UI arguments then calls the single plot code
def singlePlot():
    alist = []
    baseline = dropD.currentText()
    print("baseline is ", baseline)
    position = 0
    if not (text2.text().isdigit()):
       root = Tk()
       T = Text(root, height=5, width=50, font = ('Times', '15', 'bold'), wrap = WORD)
       T.pack()
       T.insert(INSERT, "Argument Error: Please type a valid Start Time")
       mainloop()
       return
    if not(text3.text().isdigit()):
       root = Tk()
       T = Text(root, height=5, width=50, font = ('Times', '15', 'bold'), wrap = WORD)
       T.pack()
       T.insert(INSERT, "Argument Error: Please type a valid End Time")
       mainloop()
       return

    time_start = int(text2.text())
    time_end = int(text3.text())
    found = "False"
    lower = "False"
    if baseline.isdigit():
       baseline = int(baseline)
       if baseline > 6 and baseline < 0:
          return
    else:
       print ("please input a valid antenna number from 0-6")
       root = Tk()
       T = Text(root, height=5, width=50, font = ('Times', '15', 'bold'), wrap = WORD)
       T.pack()
       T.insert(INSERT, "Argument Error: Please choose a valid antenna number from the drop down box")
       mainloop()
       return
    baseline = str(baseline)
    alist.append(baseline)
    if time_start < 0 or time_start > time_end:
       print("Time Error: Not Possible To Have A Negative Time.")
       root = Tk()
       T = Text(root, height=5, width=50, font = ('Times', '15', 'bold'), wrap = WORD)
       T.pack()
       T.insert(INSERT, "Time Argument Error: not possible to have a negative time argument")
       mainloop()
       return
    if time_end >= counter[0]:
       print("Time Error: We Have Not Recorded For More Than ", counter[0] - 1, " Seconds.")
       string = "Time Error: Max available end time is " + str(counter[0] - 1) + " seconds"
       root = Tk()
       T = Text(root, height=5, width=50, font = ('Times', '15', 'bold'), wrap = WORD)
       T.pack()
       T.insert(INSERT, string)
       mainloop()
       return
    alist.append(plotOptions.currentText())
    alist.append(text2.text())
    sf = str(skipfirst)
    sl = str(skiplast)
    alist.append(sf)
    alist.append(sl)
    alist.append(text3.text())
    print (alist)
    subprocess.Popen(["python3", "/home/corr/Desktop/jmarr/version2_h5/multi_singlePlot_ver2_h5.py"] + alist)


'''
Function: Toggling between Amp and Phase

Precondition: The starting graph is Amplitude vs. Time. The variable tracking the 
change is switch in the main window. 

Postcondition: If the button is pressed, then switch is changed from True to
False, and likewise the other way around. The function will also change the 
title of the first plot to display to user of the current graph. If the graph 
is Amp, then the function invokes autorange. If the graph is Phase, then the 
function invokes setYRange and YLimits to display y values between -180 and 180.

Note list[i].clear resets the graph and timetrack[i] resets the timer for buffer
'''
def toggle_Amp_Ph():
    global switch
    if switch == "True":
        switch = "False"
        for i in range(amount):
            lsb[i].clear()
            usb[i].clear()
            timetrack[i] = 0
            wlist[i].setYRange(-180, 180, padding=0)
            wlist[i].setLimits(yMin=-180, yMax=180)
            wlist[i].getAxis('left').setLabel(namelist[i] + " (degrees)", **labelStyle)

        wlist[0].setLabels(title="Phase vs. Time")
    else:
        switch = "True"
        wlist[0].setLabels(title="Amplitude vs. Time")
        for i in range(amount):
            lsb[i].clear()
            usb[i].clear()
            timetrack[i] = 0
            wlist[i].setYRange(0, 180, padding=0)
            wlist[i].setLimits(yMin=0, yMax=180)
            wlist[i].getAxis('left').setLabel(namelist[i] + " (counts)", **labelStyle)
     
'''
Function: Toggling between Window Size - Fit or Stretch
Alternates between birds eye view and zoomed in view
'''
def toggle_Fit_Stretch():
    global switch_size
    if switch_size == "True":
        for i in range(6):
            labelStyle = {'color':'#000000', 'font-size':'6pt'}
            lsb[i].setData(size=3)
            usb[i].setData(size=3)
            wlist[i].getAxis('left').setLabel(namelist[i], **labelStyle)
        window_size = 700
        view.setFixedHeight(window_size)
        switch_size = "False"
    else:
        labelStyle = {'color':'#000000', 'font-size':'10pt'}
        for i in range(6):
            lsb[i].setData(size=5)
            usb[i].setData(size=5)
            wlist[i].getAxis('left').setLabel(namelist[i], **labelStyle)
        window_size = 1300
        view.setFixedHeight(window_size)
        switch_size = "True"


'''
Widgets Buttons Documentation Ends 
-------------------------------------------------------------------------------------------
'''

'''
Helper Functions Begins
-------------------------------------------------------------------------------------------
Function: Tail

Precondition: takes an open file and the n amount of lines from the end.

Postcondition: Using an efficient algorithm, returns the x amount of lines
from the declared n value from the end of the file to parse.  
'''
def compare_len(file1, file2):
    len1 = file_len(file1)
    len2 = file_len(file2)
    alist = [len1, len2]
    return min(alist)

 
'''
Function: File Length

Precondition: Takes a file name 

Postcondition: return how many lines the file has
'''
def file_len(fname):
    j = 0
    with open(fname) as f:
        for j, l in enumerate(f):
            pass
    return j + 1
'''
Function: Calculate Total

Precondition: Takes in a Python list. 

Postcondition: Return the mean/ average of the list contents

'''
def calc_total(alist):
    return np.mean(alist) 

'''
Function: Calculate Amplitude 

Precondition: Takes in the average of Real and Imaginary numbers
x = Real
y = Imaginary

Postcondition: return the value of the Amplitude formula
'''
def calc_Amplitude(x, y):
    if not x:
        return
    if not y:
        return
    x2 = x*x
    y2 = y*y
    z = x2+y2
    w = np.sqrt(z)
    return w
'''
Function: Calculate Phase

Precondition: Takes in the average of Real and Imaginary numbers

Postcondition: Return the value of Phase formula
'''
def calc_Phase(x, y): 
    if not x:
        return
    if not y:
        return
    return (np.arctan2(y, x)*(180/np.pi))

'''
Function: Get Arguments, from argparse

Precondition: Initialize --fb and --fl as the argument to pass from command line
--fb = skipping the x amount of channels from the beginning
--fl = skipping the x amount of channels from the ending

Postcondition: Return the values that the users pass in to main, otherwise return 0 for 
both variables. 
'''
def get_args():
    parser = argparse.ArgumentParser(description="Retrieving command line arguments for plotting purposes")
    parser.add_argument('--fb', type=int, help='Skip the first amount of channel(s)', default=-7)
    parser.add_argument('--fl', type=int, help='Skip the last amount of channel(s)', default=-7)
    args = parser.parse_args()
    fb = args.fb
    fl = args.fl
    return fb, fl
'''
Function: Insensitive Globbing

Precondition: Takes a regular glob pattern

Postcondition: algorithmically transform the glob pattern to insensitively search for the pattern
and return a list of all the objects that matched with the insensitive pattern. 
'''

def insensitive_glob(pattern):
    def either(c):
        return '[%s%s]'%(c.lower(),c.upper()) if c.isalpha() else c
    return glob.glob(''.join(map(either,pattern)))

'''
Helper Functions Ends
-------------------------------------------------------------------------------------------
'''
'''
Main Updating and Loading Function Begins
-------------------------------------------------------------------------------------------
Function: track

Precondition: Takes a file name and the position with respect to timetrack and counter list

Postcondition: Given the filen name and position. Use pandas to open and parse the data where
it updates last, given by the counter[position], and parse all the new content accordingly. 
While in the for loop, the algorithm updates the counter[position] and timetrack[position],
parse all the real and imaginary numbers, and calculates it depending the value of 
switch (Phase or Amp). 

returns 0 if a new line is not found
returns 1 if a new line has been found
'''
def track(lfile, ufile, position):
    global timetrack
    counter[position] += 1
 
 # remove below line and the other one later
    lfile = lfile[:-3]
    lfile = lfile + '.S' + str(counter[position]) + '.h5'
    ufile = ufile[:-3]
    ufile = ufile + '.S' + str(counter[position]) + '.h5'
   
    lcheck = insensitive_glob(lfile)
    ucheck = insensitive_glob(ufile)

    if len(ucheck) == 0 or len(lcheck) == 0:
       counter[position] -= 1 
       return 0
    low = h5py.File(lfile, 'r')
    upp = h5py.File(ufile, 'r')
 
    realVal = low.get('/fullDataS/real')
    imagVal = low.get('/fullDataS/imag')

    realVal2 = upp.get('/fullDataS/real')
    imagVal2 = upp.get('/fullDataS/imag')
        
    thislistr = np.array(realVal)
    thislisti = np.array(imagVal)
    thislistr2 = np.array(realVal2)
    thislisti2 = np.array(imagVal2)
 
    thislistr = np.transpose(thislistr)
    thislisti = np.transpose(thislisti)
    thislistr2 = np.transpose(thislistr2)
    thislisti2 = np.transpose(thislisti2)

    ilist = thislisti[0]
    rlist = thislistr[0]
    ilist2 = thislisti2[0]
    rlist2 = thislistr2[0]
 
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
    
    if switch == "True":
        point = calc_Amplitude(R, I)
        point2 = calc_Amplitude(R2, I2)
    else:
        point = calc_Phase(R, I)
        point2 = calc_Phase(R2, I2)

#    if point == point2:
#        print("Matching at ", counter[position])
#    if not point2:
#        print("No Point2")
#    x = [counter[position]]
#    y = [point]
#    z = [point2]
    lsb[position].addPoints([counter[position]], [point])
    usb[position].addPoints([counter[position]], [point2])

    timetrack[position] += 1
    return 1
'''
Function: preload

Loads up the most recent line available in the dataset, called in the beginning of the code

'''

def preload():
 
    #reads the last file in the list
    low = h5py.File(lowerSideband[5], 'r')
    upp = h5py.File(upperSideband[5], 'r')

    #get data from the specific columns
    realVal = low.get('/fullData/real')
    imagVal = low.get('/fullData/imag')

    errVal = low.get('/timestamp')

    realVal2 = upp.get('/fullData/real')
    imagVal2 = upp.get('/fullData/imag')

    #converts it into arrays using numpy
    thislistr = np.array(realVal)
    thislisti = np.array(imagVal)
    thislistr2 = np.array(realVal2)
    thislisti2 = np.array(imagVal2)


    #transpose it to make it the right orientation (n x 1024)
    thislistr = np.transpose(thislistr)
    thislisti = np.transpose(thislisti)
    thislistr2 = np.transpose(thislistr2)
    thislisti2 = np.transpose(thislisti2)
    

    #set the starting point for all the plots
    startLength = len(thislistr2) - 1
    startLength = 1
    print(startLength)
    counter[0] = startLength
    counter[1] = startLength
    counter[2] = startLength
    counter[3] = startLength
    counter[4] = startLength
    counter[5] = startLength

'''
Function: update

Precondition: Gets called in main with QTimer class. 

Postcondition: Update will run through 21 baselines each second.
This will update the plotting of each graph, timetrack, and 
counter accordingly to the position through the enumaration
(0,1,2,...,20) with the function track.
'''

def update():
    for i, key in enumerate(lis):
     #track returns whether or not a newline has been found 
        nlFlag = track(lowerSideband[i], upperSideband[i], i)
     #if number of points plotted exceeds buffer_points then the graph is cleared
        if timetrack[i] >= buffer_points:
           lsb[i].clear()
           usb[i].clear()
           timetrack[i] = 0
    print("finished track")
    if nlFlag == True:
        print("line ", counter[i], "found")
    else:
        print("line ", counter[i], "not found")
'''
Start of initial code
'''


skipfirst, skiplast = get_args()
print ("start", skipfirst)
print ("last", skiplast)
if skipfirst == -7 or skiplast == -7:
  if skipfirst == -7:
    print("--fb was not passed")
  if skiplast == -7:
    print("--fl was not passed")
  sys.exit("Please Pass Both '--fb=[int]' and '--fl=[int]' Arguments When Starting This Program.")

'''
Containers to keep track of data
note that:

adict_lower looks like { '01':lsb-01.cor, '02':lsb-02.cor, ... }
so that the key is the baseline and the item is the file name associated with the baseline
similarly, adict_upper will looks like that too
'''
counter=[0]*6
tracker=[0]*6
timetrack=[0]*6


lis = ['01', '02', '03', '12', '13', '23']

namelist = ['0-1', '0-2', '0-3', '1-2', '1-3', '2-3']

'''
Populating the dictionaries with upper and lower files
'''

#looks for all the correct files then sorts them in order alphabetically
os.chdir('/home/corr/ytla/reduction')
upperSideband = insensitive_glob('*usb.cross.h5')
lowerSideband = insensitive_glob('*lsb.cross.h5')
upperSideband.sort()
lowerSideband.sort()
print(upperSideband)
print(lowerSideband)
preload()

amount = len(upperSideband)
#establish how many files there are in the global variable for stretch/fit
numFiles = amount
print("There are ", amount*2 , " files in this directory.")

buffer_points = 300 #After reaching this buffer size, the graph will clear
switch = "True"
switch_size = "True"

'''
Initalizing the Main Window Application
'''

app = QtGui.QApplication(['Graphing Running']) 
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
sa = pg.QtGui.QScrollArea() #Makes it possible to scroll in window
view = pg.GraphicsLayoutWidget() #View is used to display multiple plots
w = pg.LayoutWidget() #The form application for singleplot option
w2 = pg.LayoutWidget() #The form application for toggling options
view.setFixedHeight(1000) 
view.setFixedWidth(1200)
sa.setWidget(view)
pg.setConfigOptions(antialias=True) #Makes the window response faster
sa.show()
wlist = []
lsb = []
usb = []
blist =[lsb, usb]

'''
Initalizing the widgets buttons and text area
'''
btn = QtGui.QPushButton('Plot')
btn2 = QtGui.QPushButton('Toggle Amp/Ph')
btn3 = QtGui.QPushButton('Toggle Fit/Stretch')

dropD = QtGui.QComboBox()
dropD.addItems(["Choose Antenna", "0", "1", "2", "3"])

plotOptions = QtGui.QComboBox()
plotOptions.addItems(["Choose type of plot", "Amplitude", "Phase", "Phase Closure"])

text2 = QtGui.QLineEdit('Start Time')
text3 = QtGui.QLineEdit('End Time (exclusive)')
w.addWidget(dropD)
w.nextRow()
w.addWidget(plotOptions)
w.nextRow()


w.addWidget(text2)
w.nextRow()
w.addWidget(text3)
w.nextRow()
w.addWidget(btn)

w2.addWidget(btn2)
w2.nextRow()
w2.addWidget(btn3)

'''
Generating the 6 plots and associating a ScatterPlotItem with each plot
Note that lower files are default starting data generator 
'''
print(namelist)
for i in range(amount): 
    labelStyle = {'color':'#000000', 'font-size':'10pt'}
    w1 = view.addPlot()
    wlist.append(w1)
    wlist[i].getAxis('left').setLabel(namelist[i] + " (counts)", **labelStyle)
    sc1 = pg.ScatterPlotItem(name=lis[i], size=5 , pen=pg.mkPen(None), brush=pg.mkBrush(0, 0, 0, 255))
    sc2 = pg.ScatterPlotItem(name=lis[i], size=5 , pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 0, 255))
    wlist[i].addItem(sc1)
    wlist[i].addItem(sc2)
    
    lsb.append(sc1)
    usb.append(sc2)
    view.nextRow()


wlist[0].setLabels(title='Amplitude vs. Time' ) #Set the title of the first graph
'''
Connect the button with their respective functions 
Ex:
Clicking the 'submit' button will invoke the function submit()
'''
btn.clicked.connect(singlePlotBtn)

btn2.clicked.connect(toggle_Amp_Ph)
btn3.clicked.connect(toggle_Fit_Stretch)
w2.show()
w.show()
#changes directory for the realtime plotting
os.chdir('/home/corr/ytla/reduction/RealTime')


'''
set timer as QTimer object, a thread-like object, and runs 
the function update every one minute as long as the 
Application is running.
'''
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1000)
 
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
