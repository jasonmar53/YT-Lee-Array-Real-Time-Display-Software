# YT Lee Array Real Time Display Software and Tools

Used to display incoming data real time on the Yuan Tseh Lee Array on Mauna Loa in Hawaii. 

The system was dependent on a seperate MATLAB code that processed the raw data and converted it into ASCII format. The conversion from
binary to ASCII made the processing up to 10x longer. The ASCII version of the software utilized Panda's read_csv to read the processed
data every second. 

To reduce the time and resources the MATLAB code used, I modified the real time display software to read HDF5 files with H5PY's h5_read 
function instead of ASCII allowing the MATLAB code to skip the conversion step.

To optimize the CPU usage and time of the software tools, I implemented multiprocessing to split the tasks among 4 different CPUs and
managed to reduce the computation time of 10 hours (roughly a full observing night of incoming data) data from 20-23 mins to 4 - 8 seconds.

PYQTGraph was used to graph the data points in real time. 
