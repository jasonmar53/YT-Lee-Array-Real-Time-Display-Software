import time

f1 = open('inputfiles21/data.usb.corr1k.01.cross', 'r')
f2 = open('inputfiles21/data.usb.corr1k.02.cross', 'r')
f3 = open('inputfiles21/data.usb.corr1k.03.cross', 'r')
f4 = open('inputfiles21/data.lsb.corr1k.01.cross', 'r')
f5 = open('inputfiles21/data.lsb.corr1k.02.cross', 'r')
f6 = open('inputfiles21/data.lsb.corr1k.03.cross', 'r')

filechannel = [f1, f2, f3, f4, f5, f6]

g1 = open('read21baselines/usb-01.dat', 'w')
g2 = open('read21baselines/usb-02.dat', 'w')
g3 = open('read21baselines/usb-03.dat', 'w')
g4 = open('read21baselines/lsb-01.dat', 'w')
g5 = open('read21baselines/lsb-02.dat', 'w')
g6 = open('read21baselines/lsb-03.dat', 'w')
filechannel2 = [g1, g2, g3, g4, g5, g6]

h1 = open('read21baselines/usb-04.dat', 'w')
h2 = open('read21baselines/usb-05.dat', 'w')
h3 = open('read21baselines/usb-06.dat', 'w')
h4 = open('read21baselines/lsb-04.dat', 'w')
h5 = open('read21baselines/lsb-05.dat', 'w')
h6 = open('read21baselines/lsb-06.dat', 'w')
filechannel3 = [h1, h2, h3, h4, h5, h6]


a1 = open('read21baselines/usb-12.dat', 'w')
a2 = open('read21baselines/usb-13.dat', 'w')
a3 = open('read21baselines/usb-14.dat', 'w')
a4 = open('read21baselines/lsb-12.dat', 'w')
a5 = open('read21baselines/lsb-13.dat', 'w')
a6 = open('read21baselines/lsb-14.dat', 'w')
filechannel4 = [a1, a2, a3, a4, a5, a6]

b1 = open('read21baselines/usb-15.dat', 'w')
b2 = open('read21baselines/usb-16.dat', 'w')
b3 = open('read21baselines/usb-23.dat', 'w')
b4 = open('read21baselines/lsb-15.dat', 'w')
b5 = open('read21baselines/lsb-16.dat', 'w')
b6 = open('read21baselines/lsb-23.dat', 'w')
filechannel5 = [b1, b2, b3, b4, b5, b6]

c1 = open('read21baselines/usb-24.dat', 'w')
c2 = open('read21baselines/usb-25.dat', 'w')
c3 = open('read21baselines/usb-26.dat', 'w')
c4 = open('read21baselines/lsb-24.dat', 'w')
c5 = open('read21baselines/lsb-25.dat', 'w')
c6 = open('read21baselines/lsb-26.dat', 'w')
filechannel6 = [c1, c2, c3, c4, c5, c6]

d1 = open('read21baselines/usb-34.dat', 'w')
d2 = open('read21baselines/usb-35.dat', 'w')
d3 = open('read21baselines/usb-36.dat', 'w')
d4 = open('read21baselines/lsb-34.dat', 'w')
d5 = open('read21baselines/lsb-35.dat', 'w')
d6 = open('read21baselines/lsb-36.dat', 'w')
filechannel7 = [d1, d2, d3, d4, d5, d6]

e1 = open('read21baselines/usb-45.dat', 'w')
e2 = open('read21baselines/usb-46.dat', 'w')
e3 = open('read21baselines/usb-56.dat', 'w')
e4 = open('read21baselines/lsb-45.dat', 'w')
e5 = open('read21baselines/lsb-46.dat', 'w')
e6 = open('read21baselines/lsb-56.dat', 'w')
filechannel8 = [e1, e2, e3, e4, e5, e6]

quit = "False"
while True:
  for i in range(6):
    l = filechannel[i].readline()
    if l:
#      print("Writing")
      filechannel2[i].write(l)
      filechannel3[i].write(l)
      filechannel4[i].write(l)
      filechannel5[i].write(l)
      filechannel6[i].write(l)
      filechannel7[i].write(l)
      filechannel8[i].write(l)
    else:
      pass
#      print("EOF reached")
#      inputfiles21("Press Enter to Quit")
#      quit = "True"
#      break
  time.sleep(1)


