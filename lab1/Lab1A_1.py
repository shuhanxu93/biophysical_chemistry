#!/usr/bin/python

#import handy python modules
import numpy as np
import pylab as plt



#  ---------------       SECTION I      ---------------
#  --------------- CONVERSION FUNCTIONS ---------------

# These are a few differnt conversion formulas, which
#
#   --  converts the energy of a state to a number --
#   --   describing the popoulation of that state  --
#
# try them out by changing which one is called on line 141
#
# also try changing the temperature setting on line 115
# and the energies of the states on line 122


def convertEnthalpyToDistribution_1(E,k,T):
        return((k*T)/E)

def convertEnthalpyToDistribution_2(E,k,T):
        return(np.exp(-E/(k*T)))

def convertEnthalpyToDistribution_3(E,k,T):
	return(np.exp(-(k*T)/E))

def convertEnthalpyToDistribution_4(E,k,T):
	return(np.exp(-(E+10)/(k*T)))

def convertEnthalpyToDistribution_5(E,k,T):
	return( np.exp(-E/(k*(T-10))))



#  ---------------                     SECTION II                    ---------------
#  --------------- A RANDOM SAMPLER (TO BE USED LATER IN THE SCRIPT) ---------------

# This is a function which takes a list of energies, one for each state
# in a system, and samples it for the required number of observations.
def sampleStates(stateEnergies, numberOfObservations, k, T):
    # Count how many state-energies were provided, that is how many states to use
    Nstates = len(stateEnergies)

    # Create an array to hold the probability interval (ceiling) for each state
    Probs = np.zeros(Nstates)

    # Begin by setting the Partition Function to zero.
    PartitionFunction = 0.0

    # Go through all state energies in the input
    for i in np.arange(Nstates):
        # calculate the boltzmann factor
        Probs[i]            =  convertEnthalpyToDistribution_2(energies[i],k,T)
        # And keep adding all boltzmann factors to the Partion Function
        PartitionFunction   = PartitionFunction + Probs[i]

    # When all Boltzmann factors have been calulated and the Partition Function is
    # complete, we finish the probabilities by dividing by the Partition Function,
    # as Boltzmann statistics instructs us to ("Z" in Eq. 1 in the lab instruction)
    Probs = Probs /  PartitionFunction

    # Now we see each probability as a part of the line between 0 and 1. If the
    # probability of the first state "A" is e.g. 0.23, then all numbers between
    # 0.00 and 0.23 belong to state A. If the next state "B" has probability 0.31,
    # then all numbers between 0.23 and 0.54 (0.23+0.31) belong to state B, and
    # so on. An easy way to find these thresholds is to use a cumulative sum, where
    # each element in the array is the sum of all previous elements.
    ProbThresholds=np.cumsum(Probs)
    # If you would like to see how this works out, try printing them out by
    # un-commenting the lines below:

    print("The probabilites of the states are")
    print(Probs)
    # print("And the thresholds of the states we will use are")
    # print(ProbThresholds)

    # Now we will make lots of random numbers and assign each to a state. Hopefully,
    # the probabilites we made will guide this assignement to look like we expect
    # Boltzmann statistics to look.

    # Make an array to fill with state assignments
    states = np.zeros(numberOfObservations,dtype=int)

    # Make as many observations as required
    for i in np.arange(numberOfObservations):
        # Make a random number this observation
        current = np.random.rand()

        # Test if the current number is above the threshold for a state.
        # as long as it IS, keep testing the next state.
        while current>ProbThresholds[states[i]]:
                states[i]+=1

    # We now have a number of state assignments, as many as required. Let's create a plot
    # of them in histogram, so that the first state is "1", then "2", and so on.
    bins=np.arange(Nstates+1)+0.5
    y,dummy = plt.histogram(states+1, bins=bins, normed=True)

    plt.bar(np.arange(len(energies))+0.9, y, width=0.4, fc='blue',alpha=0.5, label='sampled states')



#  ---------------                    SECTION III                        ---------------
#  --------------- THE PROGAM STARTS HERE, AND USES THE ABOVE FUNCTION -----------------



# Set the temperature and boltzmann constant in [eV/K] & [K]
k = 8.6e-5
T = 10000

# Create a number of states by defining the energy of each state, in
# this case three states (& their state-energies).
#
# NOTE: We never actually say explicitly that there are 3 states, but
# rather we just create a set where each entry is one possible state.
energies=[-0.30, -0.35, -0.25]
# Set the number of observations of the "system", i.e. how many times
# we check which of the above state the system is in.
steps = 500




# ----- FIRST, LET'S PLOT THE PREDICTED BOLTZMANN DISTRIBUTION -----
# Create an array to hold the probabilites that is
# the same size (length=len) as the array with state-energies
predictedDistribution = np.zeros(len(energies))
# The partition function will be the sum of all, so lets have it set to zero at the beginning
PartitionFunction = 0.0
# Now loop over all the energies, i=0,1,2....N, where N=len(energies)
N=len(energies)
for i in np.arange(N):
    # given the energy of state "i", what is the population of "i"? Below, use one of the functions
    # energyToDistributionConversion_X() we defined above.
    predictedDistribution[i]  =  convertEnthalpyToDistribution_2(energies[i],k,T)
    # And keep adding all pupoulations to the Partion Function, so that we can normalize it later
    PartitionFunction = PartitionFunction + predictedDistribution[i]
# Normalize by PartitionFunction ("Z" in Boltzmann statistics)
predictedDistribution = predictedDistribution / PartitionFunction




# Prepare figure
f = plt.figure(figsize=(20,10))
fs = f.add_subplot(111)
fs.set_ylim([0,1.1])
fs.set_xlabel('State')
fs.set_ylabel('Population/Distribution')

# Make a bar-plot of prediction, in red
fs.bar(np.arange(len(energies))+0.5, predictedDistribution, width=0.4, fc='red',alpha=0.5, label='predicted Distribution from chosen conversion formula')


# Now, randomize numbers to see if it matches the predicted distribution.
# This uses the function "sampleStates" defined in the begining of the files,

sampleStates(energies,steps,k,T)

fs.legend(loc='upper center')
plt.show()
