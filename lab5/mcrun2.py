#!/usr/bin/python3

#import handy python modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import time
from matplotlib.ticker import MaxNLocator
import argparse



############ CMD PARSE ############

parser = argparse.ArgumentParser(description='Simulate a chain of beads.')

parser.add_argument('chain',
                     type=str, metavar='CHAIN_FILE', default='chain.dat',
                     help='file with chain definition')

parser.add_argument(	'-s', dest='steps',
			type=int, default=5000,
			help='number of steps (default 5000)')

parser.add_argument(	'-n', dest='perts',
			type=int, default=10,
			help='number of perturbations per steps (default 10)')

parser.add_argument(	'-e', dest='enefile',
			type=str, default=None,
			help='energy output file')

parser.add_argument(	'-p', dest='splot',
			type=float, default=1,
			help='skip plotting this many steps')

parser.add_argument(	'--score', dest='score',
			type=float, default=2,
			help='interaction score (default 2)')

parser.add_argument('--noMetropolis', dest='noMetropolis',help='use the Metropolis criterion' , action='store_false')

args = parser.parse_args()

############ READ CHAIN ############

print("Reading chain file: " + args.chain)

chain_file = open(args.chain, "r")
lines = chain_file.readlines()
cline = lines[0].strip()
chain_file.close()

NrResidues = len(cline)
NrSteps = args.steps

indexHPL = []
indexHPH = []

for i in range(NrResidues):
     b = cline[i]
     if len(b) == 0: continue
     if b == "W":
          indexHPL.append(i)
     elif b == "H":
          indexHPH.append(i)
     else:
          print("ERROR: invalid bead type '" + b + "' found in chain file")
          exit(-1)

############ SIMULATION ############

if args.enefile != None:
    eneFile = open(args.enefile,"w")

# This is a function which takes a number of random steps in 1 dimension
def randomWalkN(dimension, residues):

    # Make an array to fill with 2D-positions
    base = np.zeros(dimension)
    positions = np.tile(base,(residues,1))
    k=0
    lim=100
    # Make as many steps as required
    while(len(set(map(tuple,positions)))<residues and k<lim): #keep making new ones until a non-self-interecting one is produced, or a hundred tries has been made
        for i in np.arange(residues-1):
            # Make a random new position 1 step away
            change = np.random.rand(dimension)-0.5
            change = np.sign(change)*(np.abs(change)==np.max(np.abs(change)))
            positions[i+1] = positions[i] + change
        k+=1
    if k==lim:
        dualbase=[[0.,1.],[1.,0.]]
        dualbase=np.tile(dualbase,(NrResidues,1))
        positions=np.cumsum(dualbase,axis=0)[:NrResidues]
    #print(positions)
    return positions

def perturbChain(chain,pos):
    newchain = np.array(np.copy(chain))
    #print(newchain)
    #print(pos)
    #print(len(chain)-1)
    if(pos==0 or pos==(len(chain)-1)):
        if(pos==0):
            suggests=np.tile(newchain[pos+1],(4,1))
        else:
            suggests=np.tile(newchain[pos-1],(4,1))
        suggests+=[[0,1],[0,-1],[1,0],[-1,0]]
        choice=np.random.randint(4)
        newchain[pos] = suggests[choice] # choose something and modify new chain
    else:
        df = newchain[pos+1]-newchain[pos]
        ds = newchain[pos-1]-newchain[pos]
        dBis = df+ds
        #dBis = np.gradient(np.gradient(newchain[pos-1:pos+2])[0])[0][1]
        if(np.abs(dBis[0])==0): # straight segment. cannot change
            return chain
        else:
            newchain[pos] += np.sign(dBis)   # corner can only change in one way
            # print('success')
            # print(np.sign(dBis))
            # print(len(set(map(tuple,newchain))))
            # print(len(newchain))
    if(len(set(map(tuple,newchain)))<len(newchain)): # if clashing
        return chain
    else:
        return newchain # good move

def MHdistance(P1,P2):
    return(np.sum(np.abs(P2-P1)))

def scoreChain(chain):
    global indexHPL
    global indexHPH
    Tscore=0
    #print('HPL')
    #print(len(indexHPL)-1)
    #print('HPH')
    #print(len(indexHPH)-1)
    #for i in np.arange(len(indexHPL)-1):
    #    j=i
    #    while j<len(indexHPL):
    #        if(MHdistance(chain[indexHPL[i]],chain[indexHPL[j]])==1):
    #            Tscore+=1
    #        j+=1
    for i in np.arange(len(indexHPH)-1):
        j=i
        while j<len(indexHPH):
            if(MHdistance(chain[indexHPH[i]],chain[indexHPH[j]])==1):
                if(np.abs(indexHPH[j]-indexHPH[i])>1):
                    Tscore+=args.score
            j+=1
    return Tscore

def center(chain, position):
    newchain = np.copy(chain)
    newchain[:,0] = chain[:,0] - chain[int(position),0]
    newchain[:,1] = chain[:,1] - chain[int(position),1]
    return newchain

realStepCount = 0

def updateNewChain(i):
    #Nchain = randomWalkN(2,NrResidues)
    global chain
    global score
    global bestChain
    global bestScore
    global realStepCount

    best = False
    while not best:
        if realStepCount >= NrSteps:
            break
        
        Tchain = np.copy(chain)
        for i in np.arange(args.perts):
            res = np.random.randint(NrResidues)
            Tchain = perturbChain(Tchain,res)
        Tscore = scoreChain(Tchain)

        if args.noMetropolis:
            if(Tscore>score):
                chain = Tchain
                score = Tscore
            elif(np.random.rand()<np.exp(-np.abs(Tscore-score))):
                chain = Tchain
                score = Tscore
        else:
            chain = Tchain
            score = Tscore

        if args.enefile != None:
            eneFile.write(str(Tscore) + "\n")

        best = Tscore>bestScore

        if best:
            bestScore = Tscore
            bestChain = Tchain
        
        realStepCount += 1
        
        if realStepCount % args.splot == 0:
            break

    if True:
        ax1.cla()
        ax1.plot(chain[:,0],chain[:,1],lw=1, alpha=0.5,color='gray')
        ax1.scatter(chain[:,0],chain[:,1],s=350,c=HPL,cmap=plt.cm.YlGnBu,lw=2,edgecolors='black',vmin=-0.5,vmax=1.5)
        ax1.plot(bestChain[:,0],bestChain[:,1]-15,lw=1, alpha=0.5,color='gray')
        ax1.scatter(bestChain[:,0],bestChain[:,1]-15,s=350,c=HPL,cmap=plt.cm.YlGnBu,lw=2,edgecolors='black',vmin=-0.5,vmax=1.5)
        ax1.set_xlim([-20,20])
        ax1.set_ylim([-30,15])
        textstr = 'The best score is %.2f'%(bestScore)
        ax1.text(np.min(bestChain[:,0])-5,np.max(bestChain[:,1])-20,textstr)
        textstr = 'Step %d'%(realStepCount)
        ax1.text(np.min(bestChain[:,0])-5,np.max(bestChain[:,1])-21,textstr)
        
    if args.enefile != None:
        eneFile.flush()
#  --------------- THE PROGAM STARTS HERE, AND USES THE ABOVE FUNCTION -----------------

HPL = np.zeros(NrResidues)
for i in indexHPL:
    if(i<NrResidues):
        HPL[i]=1
HPH = 1-HPL

chain = center(randomWalkN(2,NrResidues),np.floor(NrResidues/2))
score = scoreChain(chain)

bestChain = np.copy(chain)
bestScore = np.copy(score)
f1 = plt.figure(figsize=(15,15))
plt.cla()

ax1 = f1.add_subplot(111)
#ax1.plot(chain[:,0],chain[:,1],c='black')
#ax1.scatter(chain[:,0],chain[:,1],c='black')

print("Starting simulation")

animator = anim.FuncAnimation(f1, updateNewChain, frames=NrSteps, repeat=False)

plt.show()
if args.enefile != None:
    eneFile.close()
