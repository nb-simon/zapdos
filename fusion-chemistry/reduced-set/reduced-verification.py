#script for analyzing the behavior of the reduced reaction network
#based on CRANE's "Two-Reaction Argon Plasma" tutorial

##import
#import numpy for reading .txt file
import numpy as np

#import matplotlib for visualization
import matplotlib.pyplot as plt
import matplotlib.patches as patches
plt.rcParams.update({'font.size': 12})

###dynamic case
##load data
#read and store tabulated data using genfromtxt, ignoring first line with strings
data = np.genfromtxt("I14-N22-dynamic.csv",skip_header=1,delimiter=',')

#select time column
time = data[1:,0] # s

#select electron density column
n_e = data[1:,3] # m^-3
n_e_dynamic = n_e[-1]

#select ion density column
n_i = data[1:,1] # m^-3

#select neutral density column
n_D = data[1:,2] # m^-3
n_D_dynamic = n_D[-1]

#select ionization rate coefficient
k_ion = data[1:,4] # m^3 s^-1

#select recombination rate coefficient
k_rec = data[1:,5] # m^3 s^-1

##initial calculations
#calculate predicted steady state plasma density
ss_n = (k_ion[-1]/k_rec[-1])*n_D[-1]
pred_dynamic = ss_n

##plotting
#rectangle
rect_x = time[-1] + 1
rect_y = 0
rect_width = 100
rect_height = 1e25

#species densities
fig, ax = plt.subplots()
plt.title('Functional Rate Case')
plt.axhline(y=ss_n, xmin=0, xmax=time[-1], color='black',linestyle='--',label='Steady-State Plasma Density Prediction')
plt.plot(time, n_e, color='red', label='Plasma Density')
plt.plot(time, n_D, color='blue', label='Neutral Density')
rect = patches.Rectangle((rect_x, rect_y), rect_width, rect_height, linewidth=1, edgecolor='gray', facecolor='gray')
ax.add_patch(rect)
plt.axvline(x = time[-1] + 1, color='gray', label='Steady State Reached')
plt.yscale("log")
plt.xscale("linear")
plt.xlim(0, 425)
plt.ylim(1e13, 1e23)
plt.xlabel("Time (s)")
plt.ylabel("Species Density (m${}^{-3}$)")
plt.text(125, 3e21, r'value: $(k_{ion}/k_{rec})n_{D}$', fontsize=12)
plt.legend(bbox_to_anchor=(0.5, -0.125), loc='upper center')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("dynamic_verification.png",dpi=600,bbox_inches='tight')

#reaction rates
fig, ax = plt.subplots()
plt.title('Normalized Functional Rate Coefficients')
plt.plot(time, k_ion/k_ion[0], color='red', label='Ionization Rate')
plt.plot(time, k_rec/k_rec[0], color='blue', label='Recombination Rate')
rect = patches.Rectangle((rect_x, rect_y), rect_width, rect_height, linewidth=1, edgecolor='gray', facecolor='gray')
ax.add_patch(rect)
plt.axvline(x = time[-1] + 1, color='gray', label='Steady State Reached')
plt.yscale('linear')
plt.xscale("linear")
plt.xlim(0, 425)
plt.ylim(0.7, 2.4)
plt.xlabel("Time (s)")
plt.ylabel("Normalized Reaction Rate Coefficient $(k/k_{0})$")
plt.legend(bbox_to_anchor=(0.5, -0.125), loc='upper center')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("reaction_rates.png",dpi=600,bbox_inches='tight')

###constant case
##load data
#read and store tabulated data using genfromtxt, ignoring first line with strings
data = np.genfromtxt("I14-N22-const.csv",skip_header=1,delimiter=',')

#select time column
time = data[1:,0] # s

#select electron density column
n_e = data[1:,3] # m^-3
n_e_const = n_e[-1]

#select ion density column
n_i = data[1:,1] # m^-3

#select neutral density column
n_D = data[1:,2] # m^-3
n_D_const = n_D[-1]

#select ionization rate coefficient
k_ion = 1.7628661330328915e10/6.022e23 # m^3 s^-1

#select recombination rate coefficient
k_rec = 5.754799703061313e2/6.022e23 # m^3 s^-1

##initial calculations
#calculate predicted steady state plasma density
ss_n = (k_ion/k_rec)*n_D[-1]
pred_const = ss_n

##plotting
#species densities
fig = plt.figure()
plt.title('Constant Rate Case')
plt.axhline(y=ss_n,color='black',linestyle='--',label='Steady-State Plasma Density Prediction', xmin=0, xmax=time[-1])
plt.plot(time, n_e, color='red', label='Plasma Density')
plt.plot(time, n_D, color='blue', label='Neutral Density')
plt.yscale("log")
plt.xscale("linear")
plt.xlim(0, 425)
plt.ylim(1e13, 1e23)
plt.xlabel("Time (s)")
plt.xticks([0, 50, 100, 150, 200, 250, 300, 350, 400])
plt.ylabel("Species Density (m${}^{-3}$)")
plt.text(125, 2e21, r'value: $(k_{ion}/k_{rec})n_{D}$', fontsize=12)
plt.legend(bbox_to_anchor=(0.5, -0.125), loc='upper center')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("const_verification.png",dpi=600,bbox_inches='tight')


'''

###table results
#steady state plasma densities
print('Constant Case Steady State Plasma Density: ' + str(n_e_const))
print('Functional Case Steady State Plasma Density: ' + str(n_e_dynamic))
print('Steady State Plasma Density % Difference: ' + str(100*(n_e_dynamic - n_e_const)/((n_e_dynamic + n_e_const)/2)) + '\n')

#steady state neutral densities
print('Constant Case Steady State Neutral Density: ' + str(n_D_const))
print('Functional Case Steady State Neutral Density: ' + str(n_D_dynamic))
print('Steady State Neutral Density % Difference: ' + str(100*(n_D_dynamic - n_D_const)/((n_D_dynamic + n_D_const)/2)) + '\n')

#steady state plasma prediction
print('Constant Case Steady State Neutral Density: ' + str(pred_const))
print('Functional Case Steady State Neutral Density: ' + str(pred_dynamic))
print('Steady State Neutral Density % Difference: ' + str(100*(pred_dynamic - pred_const)/((pred_dynamic + pred_const)/2)) + '\n')

#prediction inaccuracy
inacc_const = 100*(pred_const - n_e_const)/((pred_const + n_e_const)/2)
print('Constant Case Prediction Inaccuracy: ' + str(inacc_const))
inacc_dynamic = 100*(pred_dynamic - n_e_dynamic)/((pred_dynamic + n_e_dynamic)/2)
print('Functional Case Prediction Inaccuracy: ' + str(inacc_dynamic))
print('Prediction Inaccuracy % Difference: ' + str(100*(pred_dynamic - pred_const)/((pred_dynamic + pred_const)/2)) + '\n')



'''
