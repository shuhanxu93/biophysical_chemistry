#!/usr/bin/python

#import handy python modules
import numpy as np
import pylab as plt

# This is a function which takes a number of random steps in 1 dimension
def randomWalk(stepLength, steps):

    # Make an array to fill with positions
    positions = np.zeros(steps)

    # Make as many steps as required
    for i in np.arange(steps-1):

        # Make a new suggested step, +/- steplength
        change = np.sign(np.random.rand() - 0.5) * stepLength

        # and add that change to the last position
        positions[i+1] = positions[i] + change

    return positions


#  --------------- THE PROGAM STARTS HERE, AND USES THE ABOVE FUNCTION -----------------

# Set the number of steps to take each random walk
steps = 50

# Set the length of each step
stepLength = 1.0

# How many walks?
numberOfWalks = 5

# Arrays to hold partial output
lengthOfWalks = np.zeros(numberOfWalks)
endPositons   = np.zeros(numberOfWalks)

# Make each random walk take a random number of steps
# Is they are set to the same value, that number of steps will be taken
# by all random walks. 
# If yu want to see walks in the range between 50 and a 100, set  
#
# minStep = 50 
# maxStep = 100 
#
# NOTE: if you use a large range here, then you will need MANY more walks (line 30)
# A recommendation is [2,15] 
minStep = steps
maxStep = steps


# Make the required number of walks
for i in np.arange(numberOfWalks):
    stepsThisWalk = np.random.randint(minStep,maxStep+1)
    positions = randomWalk(stepLength,stepsThisWalk)
    plt.plot(positions)
    lengthOfWalks[i] = stepsThisWalk
    endPositons[i] = positions[-1]


plt.xlabel('step')
plt.ylabel('y-position ')
plt.ticklabel_format(useOffset=False)
plt.show()
