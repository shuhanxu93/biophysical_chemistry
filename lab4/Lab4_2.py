#!/usr/bin/python
import matplotlib
matplotlib.use("Qt4Agg")

#import handy python modules
import numpy as np
import pylab as plt
from matplotlib.ticker import MaxNLocator


# This is a function which takes a number of random steps in 1 dimension
def randomWalk(stepLength, steps):

    # Make an array to fill with positions
    positions = np.zeros(steps)

    # Make as many steps as required
    for i in np.arange(steps-1):
        # Make a random number this observation
        change = stepLength * np.sign(np.random.rand()-0.5)

        if positions[i] + change > 10:
            positions[i+1] = 20 - (positions[i] + change)
        elif positions[i] + change < -10:
            positions[i+1] = -20 - (positions[i] + change)
        else:
            positions[i+1] = positions[i] + change

    return positions


#  --------------- THE PROGAM STARTS HERE, AND USES THE ABOVE FUNCTION -----------------

# Set the number of steps to walk
steps = 100

# How many walks?
numberOfWalks = 10000

# Set the length of each step
stepLength = 1

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
minStep = 10 # minimum number of steps
maxStep = 100 # maximum number of steps


f1 = plt.figure(figsize=(15,15))

ax1 = f1.add_subplot(221, title='Plot of walks (maximum 300 walks)')
for i in np.arange(numberOfWalks):
    stepsThisWalk = np.random.randint(minStep,maxStep+1)
    positions = randomWalk(stepLength,stepsThisWalk)
    if(i<300):
        ax1.plot(positions)
    lengthOfWalks[i] = stepsThisWalk
    endPositons[i] = positions[-1]

#plt.plot(np.arange(stepsThisWalk),positions, 'k', alpha = 0.3)
ax1.ticklabel_format(useOffset=False)
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

savg = np.zeros(maxStep-minStep)
uavg = np.zeros(maxStep-minStep)
uavg2 = np.zeros(maxStep-minStep)

for i in np.arange(maxStep-minStep):
    thisBool = lengthOfWalks==i+minStep
    thisMany  = np.sum(thisBool)
    thisSumS   = np.sum(np.multiply(thisBool,endPositons))
    thisSumU   = np.sum(np.multiply(thisBool,abs(endPositons)))
    thisSumU2  = np.sum(np.multiply(thisBool,endPositons**2))
    if(thisMany != 0):
         savg[i] =  thisSumS / thisMany
         uavg[i] =  thisSumU / thisMany
         uavg2[i] =  thisSumU2 / thisMany
    else:
         savg[i] =   np.nan
         uavg[i] =   np.nan
         uavg2[i] =  np.nan


ax2 = f1.add_subplot(222, title='Positions at end of walk')
ax2.scatter(lengthOfWalks, endPositons,s=10, c='green', alpha=0.5, label='walks')
ax2.scatter(np.arange(maxStep-minStep)+minStep,savg, marker='+', c='red', s=100, lw=2, label='average for walks of length x')
ax2.set_xlabel('steps taken for walk')
ax2.set_ylabel('y-position at end of walk')
ax2.ticklabel_format(useOffset=False)
ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
ax2.legend()

ax3 = f1.add_subplot(223, title='Distance from origin at end of walk')
ax3.scatter(lengthOfWalks, abs(endPositons),s=10, c='green', alpha=0.5, label='walks')
ax3.scatter(np.arange(maxStep-minStep)+minStep,uavg, marker='+', c='red', s=100, lw=2, label='average for walks of length x')
ax3.set_xlabel('steps taken for walk')
ax3.set_ylabel('abs(y-position) at end of walk')
ax3.ticklabel_format(useOffset=False)
ax3.xaxis.set_major_locator(MaxNLocator(integer=True))
ax3.yaxis.set_major_locator(MaxNLocator(integer=True))
ax3.legend()

ax4 = f1.add_subplot(224, title='Squared distance from origin at end of walk')
ax4.scatter(lengthOfWalks, endPositons**2, s=10, c='green', alpha=0.5, label='walks')
ax4.scatter(np.arange(maxStep-minStep)+minStep,uavg2, marker='+', c='red', s=100, lw=2, label='average for walks of length x')
ax4.set_xlabel('steps taken for walk')
ax4.set_ylabel('(y-position)^2 at end of walk')
ax4.ticklabel_format(useOffset=False)
ax4.xaxis.set_major_locator(MaxNLocator(integer=True))
ax4.yaxis.set_major_locator(MaxNLocator(integer=True))
ax4.legend()

switch = True
if(switch):
    meanWalk_S = np.zeros(steps)
    meanWalk_U = np.zeros(steps)
    meanWalk_U2 = np.zeros(steps)
    f2 = plt.figure()
    for i in np.arange(numberOfWalks):
        positions = randomWalk(stepLength,steps)
        meanWalk_S  += positions
        meanWalk_U  += abs(positions)
        meanWalk_U2 += positions**2

    meanWalk_S /= numberOfWalks
    meanWalk_U /= numberOfWalks
    meanWalk_U2 /= numberOfWalks
    ax = f2.add_subplot(111)
    ax.plot(meanWalk_S, label='mean of positions P(t)',lw=2.5)
    ax.plot(meanWalk_U, label='mean of distance d(t)',lw=2.5)
    ax.plot(meanWalk_U2, label='mean of distance squared d^2(t)',lw=2.5)

    prep = np.polyfit(np.arange(steps),meanWalk_U2,1)
    p = np.poly1d(prep)

    textstr = 'the slope of the line is %.2f'%(prep[0])
    ax.text(0.1*steps, 0.7*steps,textstr)

    ax.plot(p(np.arange(steps)),'k--', label='Line-fit')
    ax.legend(loc=2)

plt.show()
