#!/usr/bin/python2.7

############ IMPORTS ############

import numpy as np
import argparse
import matplotlib.pyplot as plt


############ CALCS ############

traj = np.loadtxt("traj.dat", dtype=int)
mstates = np.loadtxt("enth.dat")
T = 300

#Count microstate occupation
bins = np.bincount(traj)

#Convert int values to floats and put into a numpy array
simulation_dist = np.array([float(i) for i in bins])

#Predict population Suggestion: use enthalpy values in mstates
#prediction_dist = ???

#Group states into macrostates
simulation_dist = np.array([sum(simulation_dist[0:3]),simulation_dist[3]])
prediction_dist = np.array([np.exp(-(mstates[0] - T * np.log(3))/T), np.exp(-mstates[3]/T)])

#Normalize the distributions
simulation_dist = simulation_dist / sum(simulation_dist)
prediction_dist = prediction_dist / sum(prediction_dist)


############ PLOT ############

ind = np.arange(len(simulation_dist)) # the x locations for the groups
width = 0.35 # the width of the bars

plt.bar(ind, prediction_dist, width, color='b',alpha=0.5, label='Predicted')
plt.bar(ind+width, simulation_dist, width, color='g',alpha=0.5, label='Simulation')
plt.legend(loc=4)
plt.show()
