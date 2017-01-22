import time
import re
import os
import glob
import sys

os.chdir('inputfiles')
#inside inputfiles directory
f1 = open('data.corr1k.01.cross', 'r')
f2 = open('data.corr1k.02.cross', 'r')
f3 = open('data.corr1k.03.cross', 'r')
f4 = open('data.corr1k.12.cross', 'r')
f5 = open('data.corr1k.13.cross', 'r')
f6 = open('data.corr1k.23.cross', 'r')

filechannel = [f1, f2, f3, f4, f5, f6]
os.chdir('/home/corr/Desktop/jmarr/version2Working')
g1 = open('read6baselines/usb-01.dat', 'w')
g2 = open('read6baselines/usb-02.dat', 'w')
g3 = open('read6baselines/usb-03.dat', 'w')
g4 = open('read6baselines/lsb-01.dat', 'w')
g5 = open('read6baselines/lsb-02.dat', 'w')
g6 = open('read6baselines/lsb-03.dat', 'w')
filechannel2 = [g1, g2, g3, g4, g5, g6]

h1 = open('read6baselines/usb-12.dat', 'w')
h2 = open('read6baselines/usb-13.dat', 'w')
h3 = open('read6baselines/usb-23.dat', 'w')
h4 = open('read6baselines/lsb-12.dat', 'w')
h5 = open('read6baselines/lsb-13.dat', 'w')
h6 = open('read6baselines/lsb-23.dat', 'w')
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


