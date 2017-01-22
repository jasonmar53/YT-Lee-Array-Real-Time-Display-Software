from pyqtgraph.Qt import QtGui, QtCore
import itertools as it
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
#from PyQt4 import QtGui


'''
Widgets Buttons Documentation Begins 
-------------------------------------------------------------------------------------------

Submit Function:

Precondition: Display the single plot zooming option widget as a form 
text should be 'Baseline' and text2 should be 'Time relative to Now'

Postcondition: The user should select the baseline and time in minutes
and press the submit button. The arguments will be checked for errors and passed into the
main program and then invoke to, in this example, /home/corr/Desktop/RealTimePlotting/singlePlot.py
to display a singular graph of the selected baseline relative to the starting time.
'''
global text, text2    #used in the submit

def submit():
    alist = []
    baseline = text.text()
    print("baseline is ", baseline)
    position = 0
    time_start = int(text2.text())
    time_end = int(text3.text())
    found = "False"
    lower = "False"
    if baseline.isdigit():
       baseline = int(baseline)
       if baseline > 6 and baseline < 0:
          return
    else:
       print ("please input a valid baseline number from 0-6")
       return
    baseline = str(baseline)
    alist.append(baseline)
    if time_start < 0:
       print("Time Error: Not Possible To Have A Negative Time.")
       return
    #if time_end > counter[0]:
    #   print("Time Error: We Have Not Recorded For More Than ", time_end, " Seconds.")
       return
    if switch == "True":
        alist.append("AMP")
    else:
        alist.append("PH")
    alist.append(text2.text())
    sf = str(skipfirst)
    sl = str(skiplast)
    alist.append(sf)
    alist.append(sl)
    alist.append(text3.text())
    alist.append(baseline)
    print (alist)
    subprocess.Popen(["python", "/home/corr/Desktop/jmarr/version2/singlePlot_ver2.py"] + alist) 

'''
Function: Toggling between Amp and Phase

Precondition: The starting graph is Amplitude vs. Time. The variable tracking the 
change is switch in the main window. 

Postcondition: If the button is pressed, then switch is changed from True to
False, and likewise the other way around. The function will also change the 
title of the first plot to display to user of the current graph. If the graph 
is Amp, then the function invokes autorange. If the graph is Phase, then the 
function invokes setYRange and YLimits to display y values between -180 and 180.
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
            #wlist[i].enableAutoRange()
'''
Function: Toggling between Upper Baseline or Lower Baseline

Precondition: The starting baseline is Lower. The variable tracking 
the change between baseline is switch_UL.
-If switch_UL = "True", then graph is displaying Lower Baseline files
-If switch_UL = "False", then graph is displaying Upper Baseline files

Postcondition: When the button is clicked, switch_UL will change 
from "True" to "False", or the other way around. The label text will
also change to display USB or LSB names in different font size depending
on window size. The window will clear off all points and depending on
whether is Phase or Amplitude graph, the graph will autorange or
remains between -180 and 180 y range.
'''
def toggle_USB_LSB():
    global switch_UL, update 
    if switch_UL == "True":
        switch_UL = "False"
        if switch_size == "True":
            labelStyle = {'color':'#000000', 'font-size':'10pt'}
        else:
            labelStyle = {'color':'#000000', 'font-size':'6pt'} 
        for i in range(amount):
            wlist[i].getAxis('left').setLabel(llis[i], **labelStyle) 
    else:
        switch_UL = "True"
        if switch_size == "True":
            labelStyle = {'color':'#000000', 'font-size':'10pt'}
        else:
            labelStyle = {'color':'#000000', 'font-size':'6pt'}
        for i in range(amount):
            wlist[i].getAxis('left').setLabel(ulis[i], **labelStyle)
    for i in range(amount):
        lsb[i].clear()
        timetrack[i] = 0
        if switch == "True":
	   #print ("1")
           wlist[i].setYRange(0, 180, padding=0)
           wlist[i].setLimits(yMin=0, yMax=180)
           #wlist[i].enableAutoRange() 
'''
Function: Toggling between Window Size - Fit or Stretch

Precondition: The starting window size is 4000. The variable
tracking the between fit or stretch is switch_size.
switch_size = "True" then the window size is 4000
switch_size = "False" then the windowsize is 940

Postcondition: When the button is clicked, switch_size
changes from "True" to "False", or the other way around.
Labels will also get change accordingly to the screen size
for readability. If window size is 4000, then the font size
is 10pt. If window size is 940, then font size is 6pt.
'''

def toggle_Fit_Stretch():
    global switch_size
    if switch_size == "True":
        for i in range(21):
            labelStyle = {'color':'#000000', 'font-size':'6pt'}
            lsb[i].setData(size=3)
            usb[i].setData(size=3)
            wlist[i].getAxis('left').setLabel(namelist[i], **labelStyle)
        window_size = 940
        view.setFixedHeight(window_size)
        switch_size = "False"
    else:
        labelStyle = {'color':'#000000', 'font-size':'10pt'}
        for i in range(21):
            lsb[i].setData(size=5)
            usb[i].setData(size=5)
            wlist[i].getAxis('left').setLabel(namelist[i], **labelStyle) 
        window_size = 4000
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

def tail(f, lines, _buffer=20000000000):
    # place holder for the lines found
    lines_found = []
 
    # block counter will be multiplied by buffer
    # to get the block size from the end
    block_counter = -1
 
    # loop until we find X lines
    while len(lines_found) < lines:
        try:
            f.seek(block_counter * _buffer, os.SEEK_END)
        except IOError:  # either file is too small, or too many lines requested
            f.seek(0)
            lines_found = f.readlines()
            break
 
        lines_found = f.readlines()
 
        # we found enough lines, get out
        if len(lines_found) > lines:
            break
 
        # decrement the block counter to get the
        # next X bytes
        block_counter -= 1
 
    return lines_found[-lines:]
 
'''
Function: File Length

Precondition: Takes a file name 

Postcondition: return how many lines the file hasattr
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
    if not alist:
       return
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

Note - Position is which baseline it is, 0-20
     -  .addPoint requires an array, but it'll plot all values within that array
	make sure arrays are of same size ex: x can't have 2 items while y has 1 
	- Y is LSB
	- Z is USB
	- X is time for the x axis of plot
'''
def track(lfile, ufile, position):
    global counter, timetrack 
    try:
        dataframe = pandas.read_csv(lfile, skiprows=counter[position], low_memory = False, na_filter = False, engine='c')
        dataframe2 = pandas.read_csv(ufile, skiprows=counter[position], low_memory = False, na_filter = False, engine='c')
        thislist = list(dataframe.values.flatten())
        thislist2 = list(dataframe2.values.flatten())
    except ValueError as e:
        print(e)
    except OSError as o:
        sys.exit("Finished Reading. Exiting.")
    try:
        if not thislist:
            return
    except UnboundLocalError as u:
        return
    len1 = len(thislist)
    len2 = len(thislist2)
    if len1 > len2:
        size = len2
    else:
        size = len1
    for j in range(size):
        l = thislist[j]
        l2 = thislist2[j]
        l.replace('\n', '')
        l2.replace('\n', '')
        data = l.replace('i', 'j').split()
        data2 = l2.replace('i', 'j').split()
        data = list(map(complex, data))
        data2 = list(map(complex, data2))
        a = np.array(data)
        a2 = np.array(data2)
        counter[position]= counter[position]+1
        ilist = list(a.imag) 
        rlist = list(a.real) 
        ilist2 = list(a.imag)
        rlist2 = list(a.real)
        if skipfirst > 0:
            ilist = ilist[skipfirst:]
            rlist = rlist[skipfirst:]
            ilist2 = ilist2[skipfirst:]
            rlist2 = rlist2[skipfirst:]
        if skiplast > 0:
            ilist = ilist[:-skiplast]
            rlist = rlist[:-skiplast] 
            ilist = ilist2[:-skiplast]
            rlist = rlist2[:-skiplast]
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

        if point == point2:
            print("Matching at ", counter[position])
        if not point2:
            print("No Point2")
        x = [counter[position]]
        y = [point]
        z = [point2]


        lsb[position].addPoints(x, y)
        usb[position].addPoints(x, z)
        timetrack[position] = timetrack[position] + 1
'''
Function: Load

Precondition: Takes a file name and a position

Postcondition: Using the file name and position, it will refresh
all the content of timetrack and counter list, accordingly
to the position with the help of the tail function to get the
last 15 point values and graph it out. The program will 
start from the there. 
'''
def load(lfile, ufile, position):
    global counter, timetrack 
    flist = [lfile, ufile]
    trail = 0
    len = compare_len(lfile, ufile) 
    if len < 15:
        counter[position] = 0 
        trail = 0 
    else:
        counter[position] = len - 15   
        trail = 15
    with  open(lfile, 'r') as f, open(ufile, 'r') as f2:
      alist = tail(f, trail)
      blist = tail(f2, trail)
      for l, l2 in zip(alist, blist):
        l.replace('\n', '')
        l2.replace('\n', '')
        data = l.replace('i', 'j').split()
        data2 = l2.replace('i', 'j').split()
        data = list(map(complex, data))
        data2 = list(map(complex, data2))
        a = np.array(data)
        a2 = np.array(data2)
        counter[position]= counter[position]+1
        ilist= list(a.imag)
        ilist2 = list(a2.imag)
        rlist = list(a.real)
        rlist2 = list(a2.real)
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
        point = calc_Amplitude(R, I)
        point2 = calc_Amplitude(R2, I2)
        x = [counter[position]]
        y = [point]
        z = [point2]
	# you can only plot arrays of points not individual values

        lsb[position].addPoints(x, y)
        usb[position].addPoints(x, z)
        timetrack[position] += 1

'''
Function: update

Precondition: Gets called in main with QTimer class. 

Postcondition: Update will run through 21 baselines each second.
This will update the plotting of each graph, timetrack, and 
counter accordingly to the position through the enumaration
(0,1,2,...,20) with the function track. And depending on switch_UL,
it will pass the names of lower or upper baselines. It also clears all
the figures after 150 time integrations through timetrack.
'''
def update():
    for i, key in enumerate(lis):
        track(adict_lower[key], adict_upper[key], i)
        if timetrack[i] >= 300: 
           lsb[i].clear() 
           usb[i].clear()
           timetrack[i] = 0
          # if switch == "False":
         #     usb[i].addPoints(timecounter[i], usbPhase[i])
         #     lsb[i].addPoints(timecounter[i], lsbPhase[i])
         #     wlist[i].setYRange(-180, 180, padding=0)
         #     wlist[i].setLimits(yMin=-180, yMax=180)
        #   else:
        #      usb[i].addPoints(timecounter[i], usbAmp[i])
        #      lsb[i].addPoints(timecounter[i], lsbAmp[i])
         #     wlist[i].setYRange(0, 180, padding=0)
         #     wlist[i].setLimits(0, yMax=180)

#Beginning of the code and runs first before main - turn into init later
skipfirst, skiplast = get_args() 
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

adict_lower = {}
adict_upper = {}
counter=[0]*21
tracker=[0]*21
timetrack=[0]*21

lis = ['01', '02', '03', '04', '05', '06', '12', '13', '14', '15',
 '16', '23', '24', '25', '26', '34', '35', '36', '45', '46', '56']

namelist = ['0-1', '0-2', '0-3', '0-4', '0-5', '0-6', '1-2'
, '1-3', '1-4', '1-5', '1-6', '2-3', '2-4', '2-5', '2-6', 
'3-4', '3-5', '3-6', '4-5', '4-6', '5-6']

'''
Populating the dictionaries with upper and lower files
'''

os.chdir('read21baselines')
upper_sideline = insensitive_glob('*usb*')
lower_sideline = insensitive_glob('*lsb*')

upper_sideline.sort()
lower_sideline.sort()

print ('post sorting upper', upper_sideline)
print ('post sorting lower', lower_sideline)

amount = len(upper_sideline)

print("There are ", amount, " files in this directory.")
print("Upper Sideline Files: ") 
for stri in upper_sideline:
    print(stri) 
    li = re.findall(r'\d+', stri)
    adict_upper[li[0]] = stri
print("Lower Sidelines Files: ")
for stri in lower_sideline:
    print(stri)
    li = re.findall(r'\d+', stri)
    adict_lower[li[0]] = stri
switch_UL = "False"
switch = "True"
switch_size = "True"
# filechannel = upper_sideline   testing if this thing breaks anything later

'''
Initalizing the Main Window Application
'''
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
app = QtGui.QApplication(['Graphing Running']) 
sa = pg.QtGui.QScrollArea() #Makes it possible to scroll in window
view = pg.GraphicsLayoutWidget() #View is used to display multiple plots
w = pg.LayoutWidget() #The form application for zooming option
w2 = pg.LayoutWidget() #The form application for toggling options
view.setFixedHeight(4000) 
view.setFixedWidth(1285)
view.resize = (1000, 1000)
sa.setWidget(view)
pg.setConfigOptions(antialias=True) #Makes the window response faster
sa.show()
wlist = []
lsb = []
usb = []

blist = [lsb, usb]
'''
Initalizing the widgets buttons and text area
'''
btn = QtGui.QPushButton('Submit')
btn2 = QtGui.QPushButton('Toggle Amp/Ph')
btn4 = QtGui.QPushButton('Toggle Fit/Stretch')
text = QtGui.QLineEdit('Baseline from 0 to 6')
text2 = QtGui.QLineEdit('Start Time')
text3 = QtGui.QLineEdit('End Time')
 
w.addWidget(text)
w.nextCol()
w.nextRow()
w.addWidget(text2)
w.nextRow()
w.addWidget(text3)
w.nextRow()
w.addWidget(btn)
w2.addWidget(btn2)
w2.nextRow()
w2.addWidget(btn4) 

'''
Generating the 21 plots and associating a ScatterPlotItem with each plot
Note that lower files are default starting data generator 

Jason Note - You are making a new scatterplot item type per plot then later on you are .addPoints(x,y) to that scatterplot item

lsb and usb are arrays of scatterplotitem types
'''


for plotNum in range(amount): 
    labelStyle = {'color':'#000000', 'font-size':'10pt'}
    w1 = view.addPlot()
    wlist.append(w1)
    wlist[plotNum].getAxis('left').setLabel(namelist[plotNum], **labelStyle)
    sc1 = pg.ScatterPlotItem(name=lis[plotNum], size=5 , pen=pg.mkPen(None), brush=pg.mkBrush(0, 0, 0, 255))
    sc2 = pg.ScatterPlotItem(name=lis[plotNum], size=5, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 0, 255))
    wlist[plotNum].addItem(sc1)
    wlist[plotNum].addItem(sc2)

    lsb.append(sc1)
    usb.append(sc2)
    view.nextRow()

'''
In case that it crashed, go through the 21 files and grab the last 15 points through load function

Note- if the program starts late with the data, it'll write out the most recent 15 points
'''
for i, key in enumerate(lis):
    load(adict_lower[key], adict_upper[key], i)

wlist[0].setLabels(title='Amplitude vs. Time' ) #Set the title of the first graph
'''
Connect the button with their respective functions 
Ex:
Clicking the 'submit' button will invoke the function submit()
'''
btn.clicked.connect(submit)
btn2.clicked.connect(toggle_Amp_Ph)
btn4.clicked.connect(toggle_Fit_Stretch)
w2.show()
w.show()

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
