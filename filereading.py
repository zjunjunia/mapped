# -*- coding: utf-8 -*-
"""
filereading: running optimisiation alogorithm with MaPPeD-1.3 models on experimental data a

Started on 4th of February 2020

@author: Zubair Junjunia
"""

#Importing libraries
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.style as style
import scipy.optimize as opt
import seaborn as sns


#Customising plot style
style.use('seaborn-poster')
sns.set_context('poster', font_scale=1.5)
sns.set_palette('Set2')
sns.set_style('white',{'axes.grid': True,'axes.edgecolor': '.80','grid.color': '.85'}) 

#Setting LaTeX font in plots
rc('font', **{'family': 'serif', 'serif': ['cm'], 'size'   : 42})
rc('text', usetex=True)

#Simplest Model
def func(x, N, p):
    press =[]    
    for i in prints:
        if i==0:
            press.append(N*np.exp(p*i))
        if i!=0:                
            press.append(N*np.exp(p*(i-1))-N*np.exp(p*(i)))
    return press


#Particle Sizes
def multi(x, N1, p1, N2, p2):
    press =[]    
    for i in prints:
        press.append(
                (2*N1*np.exp(p1*(i-1)) + N2*np.exp(p2*(i-1)))
                -(N1*np.exp(p1*i) + N2*np.exp(p2*i)))
    return press

#Fragmentation: p1 is large, p2 is small and N large
def frag(x, N2, p2, N1, p1, f):
    anly_exp=[]
    anly_exp_split = []
    press =[]
    j = 0
    while j<=(1):
        size=[N1,N2]
        dummyexp = []
        for i in range(max(prints)+1):
            if i==0:
                dummyexp.append(size[j])            
            if i!=0 and j==0:
                dummyexp.append(dummyexp[i-1]*(1-p1)*(1-f))
            if i!=0 and j==1:
                dummyexp.append((dummyexp[i-1]*(1-p2)) + (2*anly_exp_split[0][i-1]*f*(1-p2)))
        anly_exp_split.append(dummyexp)
        j=j+1    
    for i in range(max(prints)+1):
        dummy1 = 0
        for j in range(len(anly_exp_split)):
            dummy1+=anly_exp_split[j][i]
        anly_exp.append(dummy1)
    for i in prints:
        press.append(anly_exp[i-1]-anly_exp[i])        
    return press


#Reading data file and processing into DataFrame
data = pd.read_csv("datasets/exp3.csv") 
rawdata = pd.DataFrame(data, columns= ['Print','ABS','Glass','Aluminium'])
df=rawdata.dropna()

#Creating lists from data
prints = df['Print'].to_list()
ABS = df['ABS'].to_list()
glass = df['Glass'].to_list()
aluminium = df['Aluminium'].to_list()

#Linear interpolation of data to provide sensible limits for parameters
df_interp=rawdata.interpolate(method='linear', axis=0)
totals = [df_interp['ABS'].sum(),df_interp['Glass'].sum(),df_interp['Aluminium'].sum()]   

#Optimising with Simplest Model
abs_opti, _ = opt.curve_fit(func, prints, ABS, bounds=([0,-1],[totals[0],0]))   
gl_opti, _ = opt.curve_fit(func, prints, glass, bounds=([0,-1],[totals[1],0]))   
al_opti, _ = opt.curve_fit(func, prints, aluminium, bounds=([0,-1],[totals[2],0]))    
print("Probability for one size particle", abs_opti, gl_opti, al_opti)  

#Optimising with Particle Sizes
abs_opti2, _ = opt.curve_fit(multi, prints, ABS, bounds=([[0,-1,0,-1],[totals[0],0,totals[0]*0.5,0]]))     
gl_opti2, _ = opt.curve_fit(multi, prints, glass, bounds=([[0,-1,0,-1],[totals[1],0,totals[1]*0.5,0]]))     
al_opti2, _ = opt.curve_fit(multi, prints, aluminium, bounds=([[0,-1,0,-1],[totals[1],0,totals[2]*0.5,0]]))     
print("Probability for two particle sizes", abs_opti2, gl_opti2, al_opti2)  

#Optimising with Fragmentation
abs_opti3, _ = opt.curve_fit(frag, prints, ABS, bounds=([[0,0,0,0,0],[totals[0],1,totals[0]*0.5,1,1]]))     
gl_opti3, _ = opt.curve_fit(frag, prints, glass, bounds=([[0,0,0,0,0],[totals[1],1,totals[1]*0.5,1,1]]))     
al_opti3, _ = opt.curve_fit(frag, prints, aluminium, bounds=([[0,0,0,0,0],[totals[2],1,totals[2]*0.5,1,1]]),maxfev=5000)     
print("Probability for frag", abs_opti3, gl_opti3, al_opti3)  

#Saving parameters as a csv
#ABS
raw_param_abs = {'Model':['Simplest Model','Particle Sizes','Fragmentation'],
             '\# of Small Particles, $N_{X}^{0}$':[abs_opti[0],abs_opti2[0],abs_opti3[0]],
             'Prob. of Small Particles Transfer, $p_{x}$':[abs_opti[1]*-1,abs_opti2[1]*-1,abs_opti3[1]],
             '\# of Large Particles, $N_{Y}^{0}$':[0,abs_opti2[2],abs_opti3[2]],
             'Prob. of Large Particles Transfer, $p_{y}$':[0,abs_opti2[3]*-1,abs_opti3[3]],
             'Prob. of Fragmentation, $f$':[0,0,abs_opti3[4]]}

opti_param_abs = pd.DataFrame(raw_param_abs, columns= ['Model', '\# of Small Particles, $N_{X}^{0}$', 'Prob. of Small Particles Transfer, $p_{x}$','\# of Large Particles, $N_{Y}^{0}$','Prob. of Large Particles Transfer, $p_{y}$','Prob. of Fragmentation, $f$'])
opti_param_abs = opti_param_abs.round(3)
opti_param_abs.to_csv(r'figures\opti-exp3-abs.csv', index = False)

#Glass
raw_param_gl = {'Model':['Simplest Model','Particle Sizes','Fragmentation'],
             '\# of Small Particles, $N_{X}^{0}$':[gl_opti[0],gl_opti2[0],gl_opti3[0]],
             'Prob. of Small Particles Transfer, $p_{x}$':[gl_opti[1]*-1,gl_opti2[1]*-1,gl_opti3[1]],
             '\# of Large Particles, $N_{Y}^{0}$':[0,gl_opti2[2],gl_opti3[2]],
             'Prob. of Large Particles Transfer, $p_{y}$':[0,gl_opti2[3]*-1,gl_opti3[3]],
             'Prob. of Fragmentation, $f$':[0,0,gl_opti3[4]]}

opti_param_gl = pd.DataFrame(raw_param_gl, columns= ['Model', '\# of Small Particles, $N_{X}^{0}$', 'Prob. of Small Particles Transfer, $p_{x}$','\# of Large Particles, $N_{Y}^{0}$','Prob. of Large Particles Transfer, $p_{y}$','Prob. of Fragmentation, $f$'])
opti_param_gl = opti_param_gl.round(3)
opti_param_gl.to_csv(r'figures\opti-exp3-glass.csv', index = False)

#Aluminium
raw_param_al = {'Model':['Simplest Model','Particle Sizes','Fragmentation'],
             '\# of Small Particles, $N_{X}^{0}$':[al_opti[0],al_opti2[0],al_opti3[0]],
             'Prob. of Small Particles Transfer, $p_{x}$':[al_opti[1]*-1,al_opti2[1]*-1,al_opti3[1]],
             '\# of Large Particles, $N_{Y}^{0}$':[0,al_opti2[2],al_opti3[2]],
             'Prob. of Large Particles Transfer, $p_{y}$':[0,al_opti2[3]*-1,al_opti3[3]],
             'Prob. of Fragmentation, $f$':[0,0,al_opti3[4]]}

opti_param_al = pd.DataFrame(raw_param_al, columns= ['Model', '\# of Small Particles, $N_{X}^{0}$', 'Prob. of Small Particles Transfer, $p_{x}$','\# of Large Particles, $N_{Y}^{0}$','Prob. of Large Particles Transfer, $p_{y}$','Prob. of Fragmentation, $f$'])
opti_param_al = opti_param_al.round(3)
opti_param_al.to_csv(r'figures\opti-exp3-aluminium.csv', index = False)

#Plotting graphs

plt.figure(1)
plt.plot(prints, func(prints, *abs_opti), label="Simplest Model")
plt.plot(prints, multi(prints, *abs_opti2), label="Particle Sizes")
plt.plot(prints, frag(prints, *abs_opti3), label="Fragmentation")
plt.scatter(df['Print'], df['ABS'], s=150, marker='o',c='darkred', label="Experimental Data")
plt.xlabel('Print Number',labelpad=15)
plt.ylabel('Mass Deposited on Surface, $\mu$g',labelpad=15)
plt.title(r'\textbf{Explosive 3 Residue on ABS}', fontsize=32, pad=30)
plt.legend(frameon='True')
plt.savefig('figures/opti-exp3-abs-sub.png',transparent=True,dpi=300,bbox_inches='tight')
plt.savefig('figures/opti-exp3-abs-sub.pdf',bbox_inches='tight')

plt.figure(2)
plt.scatter(df['Print'], df['Glass'], s=150, marker='o',c='darkred', label="Experimental Data")
plt.plot(prints, func(prints, *gl_opti),  label="Simplest Model")
plt.plot(prints, multi(prints, *gl_opti2), label="Particle Sizes")
plt.plot(prints, frag(prints, *gl_opti3), label="Fragmentation")
plt.xlabel('Print Number', labelpad=15)
plt.ylabel('Mass Deposited on Surface, $\mu$g', labelpad=15)
plt.title(r'\textbf{Explosive 3 Residue on Glass}',fontsize = 32, pad=20)
plt.legend(frameon='True')
plt.savefig('figures/opti-exp3-glass-sub.png',transparent=True,dpi=300,bbox_inches='tight')
plt.savefig('figures/opti-exp3-glass-sub.pdf',bbox_inches='tight')

plt.figure(3)
plt.scatter(df['Print'], df['Aluminium'], s=150, marker='o',c='darkred', label="Experimental Data")
plt.plot(prints, func(prints, *al_opti), label="Simplest Model")
plt.plot(prints, multi(prints, *al_opti2), label="Particle Sizes")
plt.plot(prints, frag(prints, *al_opti3), label="Fragmentation")
plt.xlabel('Print Number', labelpad=15)
plt.ylabel('Mass Deposited on Surface, $\mu$g', labelpad=15)
plt.title(r'\textbf{Explosive 3 Residue on Aluminium}',fontsize = 32, pad=20)
plt.legend(frameon='True')
plt.savefig('figures/opti-exp3-aluminium-sub.png',transparent=True,dpi=300,bbox_inches='tight')
plt.savefig('figures/opti-exp3-aluminium-sub.pdf',bbox_inches='tight')

plt.show()