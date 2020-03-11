# -*- coding: utf-8 -*-
"""
MaPPeD-1.3: with multiple particle sizes and possibility of large particles
fragmenting to smaller ones 

Started on 2nd of Jan 2020

@author: Zubair Junjunia
"""

#Importing libraries
import numpy as np
import matplotlib.pyplot as plt
import random as random
from matplotlib import rc
import matplotlib.style as style
import seaborn as sns

#Customising plot style
style.use('seaborn-poster')
sns.set_context('poster')
sns.set_palette('Set2')
sns.set_style('white',{'axes.grid': True,'axes.edgecolor': '.80','grid.color': '.85'})

#Setting LaTeX font in plots
rc('font', **{'family': 'serif', 'serif': ['cm']})
rc('text', usetex=True)

#Summing all the elements in an array
def arraysum(array):
    total = 0
    for i in range(len(array)):
        total = total + array[i]
    return total

#Sums all elements in a 2D array returning a single value
def twoarraysum(array):
    total=0
    for i in range(len(array)):
        for j in range(len(array[i])):
            total = total + array[i][j]
    return total    

#Sums each list in a 2D array and returns a list
def twosplitsum(array):
    total=[]
    for i in range(len(array)):
        dummy = 0
        for j in range(len(array[i])):
            dummy += array[i][j]
        total.append(dummy)
    return total
        
#Retuns maximum length of the inner list in a 2D array
def maxarraylen(array):
    maxlen = 0
    for i in range(len(array)):
        if maxlen < len(array[i]):
            maxlen = len(array[i])
    return maxlen

#Fill the inner lists of a 2d array with 0s to maxarraylen so that each inner list is of the same length
def addingzeros(array):
    for i in range(len(array)):
        while len(array[i]) < maxarraylen(array):
            array[i].append(0)

#Mean of each list in a 2D array and returns a list
def arraymean(array):
    mean = []
    addingzeros(array)
    dummysum = 0
    for i in range(maxarraylen(array)):
        for j in range(len(array)):
            dummysum = dummysum + array[j][i]
        mean.append(dummysum/len(array))
        dummysum = 0
    return(mean)

#Population standard deviation of each list in a 2D array and returns a list
def arraystd(array):
    std = []
    addingzeros(array)
    dummyarray = []
    for i in range(maxarraylen(array)):
        for j in range(len(array)):
            dummyarray.append(array[j][i])
        std.append(np.std(dummyarray,ddof=1))
        dummyarray = []
    return(std)

#Initiates a given array and size with 1s in each position
def initiate(array,size):
    subarray=[]
    for i in range(len(size)):
        for j in range(size[i]):
            subarray.append(1)
        array.append(subarray)
        subarray=[]

#Function that mimics a press of finger with particles of different sizes and possibility of fragentation onto a slide
def presswithpsize(array):
    i=0
    while i<=len(array)-1:
        j=0
        while j<=(len(array[i])-1):
            #Random number generated form a uniform distribution, r for transferring and q for fragmenting
            r = random.uniform(0,1)
            q = random.uniform(0,1)
            if i==len(array)-1:
                if transferprobarray[i] >= r:
                    if array[i][j] == 1:
                        array[i][j] = 0
                        j=j+1
                else:
                    j=j+1
            else:
                if fragprob >= q:
                    if array[i][j] == 1:
                        del array[i][j]
                        array[i+1].append(1)
                        array[i+1].append(1)
                        j=j+1
                elif transferprobarray[i] >= r:
                    if array[i][j] == 1:
                        array[i][j] = 0
                        j=j+1
                    else:
                        j=j+1
                else:
                    j=j+1
        i=i+1
    return(array)

# Fixing variables
# Particles of different size classes are in different lists, descending order

# Probability of a particle to transfer to the slide, ordered from Largest -> Smallest
transferprobarray = [0.3,0.6]

# Probability of a particle in a larger class size fragmenting into two particles of the next smaller class 
fragprob = 0.1

#Number of particles in each size class, ordered from Largest -> Smallest
size = [50,50]

#Number of times the experiment will be run from start until all particles have transferred
experiments = 1000

totalexp = []
totalexpsmall = []
totalexplarge = []
anly_exp_split = []
anly_expsqrd_split = []
anly_var_split = []
anly_exp = []    
anly_stddev = []

#Running simulation
for i in range(experiments):
    finger = []
    smallfinger=[]
    largefinger=[]
    totalfinger=[]
    splitparticles = []
    initiate(finger,size)
    while twoarraysum(finger) != 0:
        splitparticles = twosplitsum(presswithpsize(finger))
        totalfinger.append(splitparticles[0]+splitparticles[1])
        smallfinger.append(splitparticles[1])
        largefinger.append(splitparticles[0])
    totalfinger.insert(0,arraysum(size))
    smallfinger.insert(0,size[1])
    largefinger.insert(0,size[0])
    totalexpsmall.append(smallfinger)
    totalexplarge.append(largefinger)    
    totalexp.append(totalfinger)
    i=i+1

#The expectation and variance (only for Large case) calculated analytically by iteration
j = 0
while j<=(len(size)-1):
    dummyexp = []
    dummyvar = []
    for i in range(maxarraylen(totalexp)):
        if i==0:
            dummyexp.append(size[j])            
            dummyvar.append(0)
        if i!=0 and j==0:
            dummyexp.append(dummyexp[i-1]*(1-transferprobarray[j])*(1-fragprob))
            dummyvar.append((dummyexp[i-1]*(1-transferprobarray[j])*(1-fragprob))*(transferprobarray[j]+fragprob-(transferprobarray[j]*fragprob)))
        if i!=0 and j==1:
            dummyexp.append((dummyexp[i-1]*(1-transferprobarray[j])) + (2*anly_exp_split[0][i-1]*fragprob*(1-transferprobarray[j])))
    anly_exp_split.append(dummyexp)
    anly_var_split.append(dummyvar)
    j=j+1

#Combining analytic mean calculated for the large and small cases seperately 
for i in range(maxarraylen(totalexp)):
    dummy1 = 0
    dummy2 = 0
    for j in range(len(anly_exp_split)):
        dummy1+=anly_exp_split[j][i]
    anly_exp.append(dummy1)

#Calculating standard deviation for the large case with fragmentation  
anly_stddev_split = anly_var_split    
for i in range(maxarraylen(totalexp)):
    for j in range(len(anly_var_split)-1):
        anly_stddev_split[j][i] = (anly_var_split[j][i]**0.5)       

#Calculating standard deviation in non-fragmenting cases
for i in range(maxarraylen(totalexp)):
    dummyvar = 0
    for j in range(len(size)):        
        dummyvar += (size[j]*((1-transferprobarray[j])**i-(1-transferprobarray[j])**(2*i)))
    anly_stddev.append(dummyvar**0.5)

#Plotting graphs
plt.figure(1)
plt.semilogy(arraymean(totalexp),label='Simulation Mean')
plt.semilogy(anly_exp,label='Analytic Mean')
plt.legend(loc='upper right', frameon='True')
plt.xlabel('Print Number',labelpad=15)
plt.ylabel('Particles Remaining on Finger (Log Scale)',labelpad=15)
plt.title(r'\textbf{Expected Remaining Particles on Finger}', fontsize=32, pad=30)
plt.savefig('figures/sm-mean-longer.png',transparent=True,dpi=300,bbox_inches='tight')
plt.savefig('figures/sm-mean-longer.pdf',bbox_inches='tight')

plt.figure(2)
plt.semilogy(arraymean(totalexpsmall),label='Simulation Mean of Small')
plt.semilogy(anly_exp_split[1],label='Analytic Mean of Small')
plt.legend(loc='upper right', frameon='True')
plt.xlabel('Print Number',labelpad=15)
plt.ylabel('Particles Remaining on Finger (Log Scale)',labelpad=15)
plt.title(r'\textbf{Expected Remaining Small Particles on Finger}', fontsize=32, pad=30)
plt.savefig('figures/frag-small-mean.png',transparent=True,dpi=300,bbox_inches='tight')
plt.savefig('figures/frag-small-mean.pdf',bbox_inches='tight')

plt.figure(3)
plt.semilogy(arraymean(totalexplarge),label='Simulation Mean of Large')
plt.semilogy(anly_exp_split[0],label='Analytic Mean of Large')
plt.legend(loc='upper right', frameon='True')
plt.xlabel('Print Number',labelpad=15)
plt.ylabel('Particles Remaining on Finger (Log Scale)',labelpad=15)
plt.title(r'\textbf{Expected Remaining Large Particles on Finger}', fontsize=32, pad=30)
plt.savefig('figures/frag-large-mean.png',transparent=True,dpi=300,bbox_inches='tight')
plt.savefig('figures/frag-large-mean.pdf',bbox_inches='tight')

plt.figure(4)
plt.semilogy(arraystd(totalexp),label='Simulation Standard Deviation')
plt.semilogy(anly_stddev,label='Analytic Standard Deviation')
plt.legend(loc='upper right', frameon='True')
plt.xlabel('Print Number',labelpad=15)
plt.ylabel('Standard Deviation (Log Scale)',labelpad=15)
plt.title(r'\textbf{Standard Deviation of Particles on Finger}', fontsize=32, pad=30)
plt.savefig('figures/sm-sd.png',transparent=True,dpi=300,bbox_inches='tight')
plt.savefig('figures/sm-sd.pdf',bbox_inches='tight')

plt.figure(5)
plt.plot(arraystd(totalexpsmall),label='Simulation Small Standard Deviation')
plt.plot(anly_stddev_split[1],label='Analytic Small Standard Deviation')
plt.legend(loc='upper right')
plt.xlabel('press')
plt.savefig('sd_small_frag.png',dpi=300)

plt.figure(6)
plt.semilogy(arraystd(totalexplarge),label='Simulation Standard Deviation of Large')
plt.semilogy(anly_stddev_split[0],label='Analytic Standard Deviation of Large')
plt.legend(loc='upper right', frameon='True')
plt.xlabel('Print Number',labelpad=15)
plt.ylabel('Particles Remaining on Finger (Log Scale)',labelpad=15)
plt.title(r'\textbf{Standard Deviation of Remaining Large Particles on Finger}', fontsize=32, pad=30)
plt.savefig('figures/frag-large-sd.png',transparent=True,dpi=300,bbox_inches='tight')
plt.savefig('figures/frag-large-sd.pdf',bbox_inches='tight')

plt.show()
