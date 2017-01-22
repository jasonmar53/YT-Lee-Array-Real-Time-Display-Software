import time
import re
import os
import glob
import sys

os.chdir('h5inputfiles')
#inside inputfiles directory
f1 = open('2016_Jul_01_01_57_48.corr1k.01.cross.h5', 'r')
f2 = open('2016_Jul_01_01_57_48.corr1k.02.cross.h5', 'r')
f3 = open('2016_Jul_01_01_57_48.corr1k.03.cross.h5', 'r')
f4 = open('2016_Jul_01_01_57_48.corr1k.12.cross.h5', 'r')
f5 = open('2016_Jul_01_01_57_48.corr1k.13.cross.h5', 'r')
f6 = open('2016_Jul_01_01_57_48.corr1k.23.cross.h5', 'r')

filechannel = [f1, f2, f3, f4, f5, f6]
os.chdir('/home/corr/Desktop/jmarr/version2Working')
g1 = open('h5read6baselines/usb-01.h5', 'w')
g2 = open('h5read6baselines/usb-02.h5', 'w')
g3 = open('h5read6baselines/usb-03.h5', 'w')
g4 = open('h5read6baselines/lsb-01.h5', 'w')
g5 = open('h5read6baselines/lsb-02.h5', 'w')
g6 = open('h5read6baselines/lsb-03.h5', 'w')
filechannel2 = [g1, g2, g3, g4, g5, g6]

h1 = open('h5read6baselines/usb-12.h5', 'w')
h2 = open('h5read6baselines/usb-13.h5', 'w')
h3 = open('h5read6baselines/usb-23.h5', 'w')
h4 = open('h5read6baselines/lsb-12.h5', 'w')
h5 = open('h5read6baselines/lsb-13.h5', 'w')
h6 = open('h5read6baselines/lsb-23.h5', 'w')
filechannel3 = [h1, h2, h3, h4, h5, h6]

quit = "False"

while True:
   for i in range(6):
      l = filechannel[i].readline()
      if l:
         filechannel2[i].write(l)
         filechannel3[i].write(l)
      else:
         pass
   time.sleep(1)


