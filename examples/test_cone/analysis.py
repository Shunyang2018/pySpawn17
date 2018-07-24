# this analysis script processes the sim.hdf5 file into various human-readable 
# formats.  This script can be run while the simulation is in progress.
import pyspawn
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


# open sim.hdf5 for processing
an = pyspawn.fafile("sim.hdf5")
work = pyspawn.fafile("working.hdf5")
# create N.dat and store the data in times and N
an.fill_electronic_state_populations(column_filename = "N.dat")
an.fill_trajectory_populations(column_file_prefix = "Pop")
times = an.datasets["00_time"]
# N = an.datasets["electronic_state_populations"]
# make population (N.dat) plot in png format
# plt.plot(times,N[:,0],"ro",times,N[:,1],"bs",markeredgewidth=0.0)
# plt.xlabel('Time')
# plt.ylabel('Population')
# plt.savefig('N.png')
# uncomment to show the plot in a window
# plt.show()

# write files with energy data for each trajectory
an.fill_trajectory_energies(column_file_prefix="E")

# list all datasets
an.list_datasets()
e1 = an.datasets["00_poten"]
ke1 = an.datasets["00_kinen"]
tot1 = an.datasets["00_toten"]
aven1 = an.datasets["00_aven"]
pop = an.datasets["00_pop"]
# plt.plot(times, ke1, "bs", markeredgewidth=0.0)
# plt.plot(times, aven1, "rs", markeredgewidth=0.0)
# plt.plot(times, tot1, "go")
plt.plot(times, pop[:, 0], "ro")
plt.plot(times, pop[:, 1], "bo")
plt.xlabel('Time')
plt.ylabel('Population')
plt.show()
