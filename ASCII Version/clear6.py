g1 = open('read6baselines/corr.01.cross', 'w')
g2 = open('read6baselines/corr.02.cross', 'w')
g3 = open('read6baselines/corr.03.cross', 'w')
g4 = open('read6baselines/corr.12.cross', 'w')
g5 = open('read6baselines/corr.13.cross', 'w')
g6 = open('read6baselines/corr.23.cross', 'w')
filechannel2 = [g1, g2, g3, g4, g5, g6]

for i in range(6):
  filechannel2[i].truncate()
