#!/usr/bin/python2.7

############ IMPORTS ############

import numpy as np
import argparse
import matplotlib.pyplot as plt
from matplotlib import gridspec

############ CALCS ############

traj = np.loadtxt("traj.dat", dtype=int)
mstates = np.loadtxt("enth.dat")
T = 300
N = len(mstates)

#Count microstate occupation
simulation_dist = np.zeros(N)
for i in np.arange(N):
    simulation_dist[i] = np.sum(traj==i)
prediction_dist = np.exp(-mstates/T)

print (simulation_dist)

#Normalize the distributions
simulation_dist = simulation_dist / float(sum(simulation_dist))
prediction_dist = prediction_dist / float(sum(prediction_dist))

############ PLOT ############


#Append zeros at missing elements
simulation_dist = np.concatenate((simulation_dist,np.zeros(N-len(simulation_dist))))

#Setup plot data
ind = np.arange(N) # the x locations for the groups
width = 0.35 # the width of the bars

plt.rcParams.update({'font.size': 18})
f = plt.figure(figsize=(18,8))
gs = gridspec.GridSpec(1, 2, width_ratios=[2, 4]) 
ax1=f.add_subplot(gs[0])
ax2=f.add_subplot(gs[1])

ax1.bar(ind, prediction_dist, width, color='b',alpha=0.5, label='Predicted')
ax1.bar(ind+width, simulation_dist, width, color='g',alpha=0.5, label='Simulation')

#Add legend
ax1.legend(loc=0)
ax1.set_ylim([0,1])
ax1.set_xlim([-0.5,N*2])

#Remove ticks
ax1.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')
    
ax2.plot(traj[::1],'+')
ax2.set_ylim([-0.5, N+0.5])
ax2.set_ylabel('State')
ax2.set_xlabel('Simulation step')
plt.show()