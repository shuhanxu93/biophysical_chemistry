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
			
parser.add_argument(	'-n', dest='steps',
			type=int, default=1000,
			help='number of steps (default 1000)')
			
parser.add_argument(	'-o', dest='traj',
			type=str, default='traj.dat',
			help='output trajectory file')
			
parser.add_argument(	'-t', dest='temp',
			type=float, default=300.0,
			help='simulation tempetature in kelvin (default 300 K)')
			
parser.add_argument(	'-i', dest='init',
			type=int, default=0,
			help='initial state (default 0)')
			
parser.add_argument(	'-net', dest='net',
			type=str, default=None,
			help='network file of transition booleans')
			
parser.add_argument('--append', dest='append',help='appends to the traj-file, instead of overwriting' , action='store_true')
			
parser.add_argument(	'--skip-steps', dest='skip',
			type=int, default=1,
			help='strides of steps to skip in output (default 1)')
			
args = parser.parse_args()



############ READ ENERGIES ############

print("Reading enthalpy file:", args.ene)
e =  np.loadtxt(args.ene)
nstates = len(e)
beta = 1/args.temp

############ TRANSITION MATRIX ############

#Create forbidden tansition matrix of ones (no forbidden transitions)
net = np.ones((nstates,nstates))

#Check the ftrans file
if (args.net != None):
	if os.path.isfile(args.net):
		print ("Reading in network file:", args.net)
		net =  np.loadtxt(args.net)
	else:
		print ("Writing out default network file:", args.net)
		np.savetxt(args.net, net, delimiter="	", fmt="%d")

if len(net) != nstates or len(net[0]) != nstates:
	print("ERROR: forbidden transition file size missmatch")
	exit(-1)

#Create actual transition matrix using boltzmann factors, filtered by barriers
trans = np.ones((nstates,nstates))

for i in range(nstates):
	for j in range(nstates):
		trans[i,j] = min(1, np.exp(-beta * (e[j] - e[i])) ) * net[i,j]

############ MC ############

print ("Preforming simulation")

if args.append:
	trajFile = open(args.traj,"a")
else:
	trajFile = open(args.traj,"w")

if args.init >= nstates:
	print("ERROR: initial state not found")
	exit(-1)
	
current_state = args.init

for i in range(args.steps):
	
	#output progress to prompt
	if i % int(float(args.steps)/4.) == 0:
		print (str(int(round(float(i)/float(args.steps)*100)))+"% done")
	
	#output current state to file
	if i % args.skip == 0:
		trajFile.write(str(current_state) + "\n")
	
	#pick a random state
	next_state = random.sample(range(nstates), 1)[0]
	
	if (trans[current_state,next_state] == 0):
		continue
	
	#take next step
	if trans[current_state, next_state] > random.random():
		current_state = next_state

trajFile.close()

print ("100% done")




















