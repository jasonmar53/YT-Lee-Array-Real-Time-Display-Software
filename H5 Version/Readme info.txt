H5 Version of real time display 

File Usages
clear6/21 - clears all the simulated data read so far

phaseClosure_plot/6 - plots all the possible combinations of phase closures with the time span specified by the user

plot_x_baselines - plots the data real time using h5read to parse through ASCII files. Allows the user to alternate between plotting amplitude or phase and provides a GUI for the user to use phaseClosure and singlePlot. 

stim6 - simulates incoming real time data by reading full datasets and writing it out to a new file every second

**NOTES** 
	There is no stim21 because at that point in time we overhauled how we processed data on the MATlab software which processes the raw incoming data and we were using the data straight from there isntead of using completed files.

	MULTI VERSIONS - same functionality, but used multiprocessing to greatly improve performance. 
