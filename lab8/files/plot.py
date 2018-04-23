#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import argparse

############ INPOT ############

parser = argparse.ArgumentParser(description='Plot a simulation of a chain of beads.')

parser.add_argument(	'file',
			type=str, metavar='file', default='energy.xvg',
			help='file with simulation statistics')
			
parser.add_argument(	'--skiprows', dest='skiprows',
			type=int, default='24',
			help='number of rows to skip at the start of the file')

args = parser.parse_args()

######### READ DATA ##########

ene = np.loadtxt(args.file, skiprows=args.skiprows)
x = ene[:,0]
y = ene[:,1]

############ PLOT ############

plt.plot(x,y)
plt.xlabel("time (ns)")
plt.ylabel("output (a.u.)")
plt.show()
