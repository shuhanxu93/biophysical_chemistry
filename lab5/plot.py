#!/usr/bin/python2.7

############ IMPORTS ############

import numpy as np
import matplotlib.pyplot as plt
import argparse
parser = argparse.ArgumentParser(description='Plot a simulation of a chain of beads.')

parser.add_argument(	'-f', dest='file',
			type=str, default='ene.dat',
			help='input file name')

parser.add_argument(	'-N', dest='Navg',
			type=int, default=10,
			help='number of states to calculate running mean for')

args = parser.parse_args()

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / N

############ CALCS ############

ene = np.loadtxt(args.file, dtype=float)

############ PLOT ############

plt.plot(ene, '.g',lw=0.1,label='momentary score')
textstr = 'running_mean over %.2i states'%(args.Navg)
plt.plot(running_mean(ene,args.Navg), 'r',lw=1,label=textstr)

plt.legend()
plt.show()
