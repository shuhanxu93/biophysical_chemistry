#!/usr/bin/python

import numpy as np 
import pylab as plt


hists = np.genfromtxt('histo_1.xvg', skip_header=12)
profile = np.genfromtxt('profile_1.xvg', skip_header=12)


N = np.shape(hists)[1] - 1 
x = hists[:,0]

f = plt.figure()

ax1=f.add_subplot(211)
for i in np.arange(N):
	ax1.plot(hists[:,i+1])

ax2=f.add_subplot(212)
ax2.plot(profile[:,0],profile[:,1])
plt.show()
