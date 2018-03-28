#!/usr/bin/python

############ IMPORTS ############

import random
import numpy as np
import argparse
import os.path



############ CMD PARSE ############

parser = argparse.ArgumentParser(description='Do a simple MC simulation.')

parser.add_argument(	'ene',
			type=str, metavar='ENE', default='enth.dat',
			help='file with entahlpy of each state')
			
parser.add_argument(	'-o', dest='traj',
			type=str, default='traj.dat',
			help='output trajectory file')
			
parser.add_argument(	'-t', dest='temp',
			type=float, default=300.0,
			help='simulation tempetature in kelvin (default 300 K)')
			
parser.add_argument(	'-n', dest='steps',
			type=int, default=1000,
			help='number of steps (default 1000)')
			
parser.add_argument(	'-i', dest='init',
			type=int, default=0,
			help='initial state (default 0)')
			
parser.add_argument(	'--skip-steps', dest='skip',
			type=int, default=1,
			help='strides of steps to skip in output (default 1)')
			
parser.add_argument(	'--ftrans', dest='ftrans',
			type=str, default=None,
			help='forbidden transition file')
			
args = parser.parse_args()



############ READ ENERGIES ############

print("Reading enthalpy file:", args.ene)
e =  np.loadtxt(args.ene)
nstates = len(e)
beta = 1/args.temp

############ TRANSITION MATRIX ############

#Create forbidden tansition matrix of ones (no forbidden transitions)
ftrans = np.ones((nstates,nstates))

#Check the ftrans file
if (args.ftrans != None):
	if os.path.isfile(args.ftrans):
		print("Reading forbidden trans file:", args.ftrans)
		ftrans =  np.loadtxt(args.ftrans)
	else:
		print("Writing forbidden trans file:", args.ftrans)
		np.savetxt(args.ftrans, ftrans, delimiter="	", fmt="%d")

if len(ftrans) != nstates or len(ftrans[0]) != nstates:
	print("ERROR: forbidden transition file size missmatch")
	exit(-1)

#Create actuall transition matrix using boltzmann factors
trans = np.ones((nstates,nstates))

for i in range(nstates):
	for j in range(nstates):
		trans[i,j] = min(1, np.exp(-beta * (e[j] - e[i])) ) * ftrans[i,j]

############ MC ############

print("Performing simulation")
	
trajFile = open(args.traj,"w")

if args.init >= nstates:
	print("ERROR: initial state not found")
	exit(-1)
	
current_state = args.init

for i in range(args.steps):
		
	#output current state
	if i % args.skip == 0:
		trajFile.write(str(current_state) + "\n")
		
	#list possible next states
	possible_next = []
	for j in range(nstates):
		if j != current_state and trans[current_state,j] != 0.:
			possible_next.append(j)
	
	#pick a random one
	if len(possible_next) > 0:
		next_state = random.sample(possible_next, 1)[0]
	else:
		next_state = current_state
	
	#take next step
	if trans[current_state, next_state] > random.random():
		current_state = next_state

trajFile.close()

print("Done!")




















