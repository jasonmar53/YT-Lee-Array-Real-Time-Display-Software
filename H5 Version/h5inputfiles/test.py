import numpy as np
import h5py
import pandas


fh = h5py.File('test.h5', 'r')
data = fh.get('/fullData/real')

stuff = np.array(data)
stuff=np.transpose(stuff)

print (stuff)
print (len(stuff[1]))
print (len(stuff))
