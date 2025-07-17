#script for analyzing the behavior of the full reaction network
#based on CRANE's "Two-Reaction Argon Plasma" tutorial

##import
#import numpy for reading .txt file
import numpy as np

#import matplotlib for visualization
import matplotlib.pyplot as plt

import math

##electron temperature
T_e = 500

##verification data
#atomic ratio fit
a_ratio = [
  [-3.885296435411E+00, -5.697204983970E-02, 7.332383617797E-02, -3.505183129037E-02, 8.175768579910E-03, -1.025860190568E-03, 7.041006112962E-05, -2.467291455100E-06, 3.436102553376E-08],
  [1.505487187018E+01, 4.633572829771E-04, -1.702732444633E-03, 1.882868187070E-03, -6.728098565933E-04, 1.133241004935E-04, -9.735191629933E-06, 4.053170686858E-07, -6.463282471161E-09],
  [-6.749191912028E+00, 1.050145613783E-03, -3.148776304951E-03, 1.594704172137E-03, -3.246647453262E-04, 3.184754694533E-05, -1.387656614654E-06, 1.600623293301E-08, 2.722493472041E-10],
  [2.212221660002E+00, 4.854461323593E-03, -2.452783916892E-03, 4.064257852894E-04, -2.059459670150E-05, -2.358171220598E-06, 3.488698891258E-07, -1.422059161908E-08, 1.698254518458E-10],
  [-5.257981277508E-01, -3.179654723425E-03, 1.767567981601E-03, -3.839001285389E-04, 4.783673711689E-05, -3.378269018931E-06, 9.511636577030E-08, 6.913540712148E-10, -5.483090178167E-11],
  [8.824411449640E-02, 9.193475524397E-04, -4.299802583958E-04, 6.248027250326E-05, -4.077787495573E-06, 1.124935475483E-07, 1.140116701448E-08, -1.211498169926E-09, 3.020216342872E-11],
  [-9.799369577387E-03, -1.679454700153E-04, 7.381643118061E-05, -7.865967145477E-06, -4.674862715791E-08, 4.744742742259E-08, -4.127705769609E-09, 2.185243304602E-10, -4.848384547542E-12],
  [6.413937652029E-04, 1.902440743752E-05, -9.875692439849E-06, 1.734207080274E-06, -1.760833256154E-07, 1.551629723045E-08, -9.432683181108E-10, 2.682232500047E-11, -2.216051536502E-13],
  [-1.861114574375E-05, -9.394367819466E-07, 5.893327001637E-07, -1.457328885095E-07, 2.193301182972E-08, -2.248254389232E-09, 1.398963108397E-10, -4.493865381320E-12, 5.590467018306E-14],
]

#molecular ratio fit
m_ratio = [
  [-1.929803964240E+01, 2.097006502950E-01, -1.100904809661E-01, 4.477781641551E-02, -9.060826089295E-03, 1.170547725039E-03, -8.893455666588E-05, 3.479454987799E-06, -5.361512296401E-08],
  [1.727612905933E+01, -4.662670859833E-01, 8.567341672326E-02, -6.827368520293E-03, -3.618060467670E-03, 6.852659500488E-04, -4.473404420068E-05, 1.209602016239E-06, -1.069974187479E-08],
  [-8.438025952533E+00, 6.115179297110E-01, -1.153478632323E-01, 1.993457166448E-02, 1.643837202714E-04, -3.516424328964E-04, 3.207886028645E-05, -1.101305933603E-06, 1.299192188737E-08],
  [2.883389908864E+00, -4.286361930144E-01, 6.596018559458E-02, -1.341784022457E-02, 1.582201264314E-03, -7.056994955968E-05, 4.431489645883E-07, 2.326874797653E-08, 1.068518137706E-10],
  [-7.403401021470E-01, 1.809442086665E-01, -1.864042138902E-02, 1.875666968084E-03, -2.978688155916E-04, 2.721069163086E-05, -1.428413713222E-06, 4.845148645034E-08, -8.048035605554E-10],
  [1.387371448471E-01, -4.879175895909E-02, 4.430141421894E-03, 1.476743155802E-04, -3.955049388000E-05, 2.382368688632E-06, -5.790867265229E-08, -6.986008432331E-10, 4.535659079263E-11],
  [-1.746217632264E-02, 8.151856339270E-03, -1.015594807894E-03, 6.205132641268E-06, 7.210178682186E-06, -6.812476857444E-07, 3.277446170025E-08, -8.583517963518E-10, 9.700723935742E-12],
  [1.287561948974E-03, -7.544209459715E-04, 1.374937928555E-04, -1.222677896703E-05, 8.247029259344E-07, -5.043186962921E-08, 2.025920058300E-09, -3.655728430701E-11, 8.337869178540E-14],
  [-4.136061327089E-05, 2.914443517923E-05, -7.106408217685E-06, 1.041267499432E-06, -1.158374992604E-07, 9.052478729563E-09, -4.280094258996E-10, 1.063115935764E-11, -1.030790224273E-13],
]

###low molecular ion density case
##load data
#read and store tabulated data using genfromtxt, ignoring first line with strings
data = np.genfromtxt("I120-I29-N116-N28.csv",skip_header=1,delimiter=',')

#select time column
time = data[1:,0] # s

#select D2 density column
n_D2 = data[1:,1] # m^-3

#select D2+ density column
n_D2p = data[1:,2] # m^-3

#select D density column
n_D = data[1:,3] # m^-3

#select D+ density column
n_Dp = data[1:,4] # m^-3

#select electron density column
n_e = data[1:,20] # m^-3

#select dissociation rate 1 column
RDS1 = data[1:,5] # m^-3 s^-1

#select dissociation rate 2 column
RDS2 = data[1:,6] # m^-3 s^-1

#select dissociation rate 3 column
RDS3 = data[1:,7] # m^-3 s^-1

#select dissociation rate 4 column
RDS4 = data[1:,8] # m^-3 s^-1

#select ionization rate 1 column
REI1 = data[1:,9] # m^-3 s^-1

#select ionization rate 2 column
REI2 = data[1:,10] # m^-3 s^-1

#select ionization rate 3 column
REI3 = data[1:,11] # m^-3 s^-1

#select fusion rate 1 column
RFS1 = data[1:,12] # m^-3 s^-1

#select recombination rate column
RRC = data[1:,13] # m^-3 s^-1

#select D source column
SD = data[1:,14] # m^-3 s^-1

#select D2 source column
SD2 = data[1:,15] # m^-3 s^-1

#select D2+ source column
SD2p = data[1:,16] # m^-3 s^-1

#select D+ source column
SDp = data[1:,17] # m^-3 s^-1

#select electron source column
Sem = data[1:,18] # m^-3 s^-1

#select T+ density column
n_Tp = data[1:,19] #m^-3 s^-1

#select dissociation rate coefficient 1 column
kDS1 = data[1:,21] # m^3 s^-1

#select dissociation rate coefficient 2 column
kDS2 = data[1:,22] # m^3 s^-1

#select dissociation rate coefficient 3 column
kDS3 = data[1:,23] # m^3 s^-1

#select dissociation rate coefficient 4 column
kDS4 = data[1:,24] # m^3 s^-1

#select ionization rate coefficient 1 column
kEI1 = data[1:,25] # m^3 s^-1

#select ionization rate coefficient 2 column
kEI2 = data[1:,26] # m^3 s^-1

#select ionization rate coefficient 3 column
kEI3 = data[1:,27] # m^3 s^-1

#select fusion rate coefficient 1 column
kFS1 = data[1:,28] # m^3 s^-1

#select recombination rate coefficient column
kRC = data[1:,29] # m^3 s^-1

##initial calculations
#steady state atomic ratio
R_a = 0
#temperature index
for n in range(0, 9):
  #density index
  for m in range(0, 9):
    R_a += a_ratio[n][m] * (math.log(n_e[-1]/1e14))**m * (math.log(T_e))**n

#steady state molecular ratio
R_m = 0
#temperature index
for n in range(0, 9):
  #density index
  for m in range(0, 9):
    R_m += m_ratio[n][m] * (math.log(n_e[-1]))**m * (math.log(T_e))**n

##plotting
#species densities
fig = plt.figure()
plt.title('Low Molecular IC Densities')
plt.axhline(y=(math.exp(R_a))*n_D[-1],color='black',linestyle='--',label='Predicted n${}_{D^+}$')
plt.plot(time, n_D, color='green', label='n${}_D$')
plt.plot(time, n_Dp, color='red', label='n${}_{D^+}$')
plt.plot(time, n_e, color='purple',linestyle='--', label='n${}_e$')
plt.plot(time, n_D2, color='blue', label='n${}_{D_2}$')
plt.plot(time, n_D2p, color='orange', label='n${}_{D_2^+}$')
plt.yscale("log")
plt.ylim(1e7, 1e26)
plt.xscale("linear")
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Species Density (m${}^{-3}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("low_ion_verification.png",dpi=600,bbox_inches='tight')

#reaction rates
fig = plt.figure()
plt.title('Low Molecular IC Reaction Rates')
plt.plot(time, RDS1, label='RDS1')
plt.plot(time, RDS2, label='RDS2')
plt.plot(time, RDS3, label='RDS3')
plt.plot(time, RDS4, label='RDS4')
plt.plot(time, REI1, label='REI1')
plt.plot(time, REI2, label='REI2')
plt.plot(time, REI3, label='REI3')
plt.plot(time, RRC, label='RRC')
plt.plot(time, RFS1, label='RFS1')
plt.yscale("log")
plt.ylim(1e10, 1e27)
plt.xscale("linear")
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Reaction Rate (m${}^{-3}$ s${}^{-1}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("low_ion_rates.png",dpi=600,bbox_inches='tight')

#reaction rate coefficients
fig = plt.figure()
plt.title('Low Molecular IC Reaction Rate Coefficients')
plt.plot(time, kDS1, label='kDS1')
plt.plot(time, kDS2, label='kDS2')
plt.plot(time, kDS3, label='kDS3')
plt.plot(time, kDS4, label='kDS4')
plt.plot(time, kEI1, label='kEI1')
plt.plot(time, kEI2, label='kEI2')
plt.plot(time, kEI3, label='kEI3')
plt.plot(time, kRC, label='kRC')
plt.plot(time, kFS1, label='kFS1')
plt.yscale("log")
#plt.ylim(1e10, 1e27)
plt.xscale("linear")
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Reaction Rate Coefficient (m${}^{3}$ s${}^{-1}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("low_ion_coefficients.png",dpi=600,bbox_inches='tight')

#source terms
fig = plt.figure()
plt.title('Low Molecular IC Source Terms')
plt.plot(time, SD, color='green', label='S${}_D$')
plt.plot(time, SDp, color='red', label='S${}_{D^+}$')
plt.plot(time, Sem, color='purple',linestyle='--', label='S${}_e$')
plt.plot(time, SD2, color='blue', label='S${}_{D_2}$')
plt.plot(time, SD2p, color='orange', label='S${}_{D_2^+}$')
plt.yscale("symlog")
plt.yticks([-1e24, -1e21, -1e18, -1e15, -1e12, -1e9, -1e6, -1e3, 0, 1e3, 1e6, 1e9, 1e12, 1e15, 1e18, 1e21, 1e24])
plt.ylim(-1e25, 1e25)
plt.xscale("linear")
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Production Rate (m${}^{-3}$ s${}^{-1}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("low_ion_sources.png",dpi=600,bbox_inches='tight')

###medium molecular ion density case
##load data
#read and store tabulated data using genfromtxt, ignoring first line with strings
data = np.genfromtxt("I120-I213-N116-N28.csv",skip_header=1,delimiter=',')

#select time column
time = data[1:,0] # s

#select D2 density column
n_D2 = data[1:,1] # m^-3

#select D2+ density column
n_D2p = data[1:,2] # m^-3

#select D density column
n_D = data[1:,3] # m^-3

#select D+ density column
n_Dp = data[1:,4] # m^-3

#select electron density column
n_e = data[1:,20] # m^-3

#select dissociation rate 1 column
RDS1 = data[1:,5] # m^-3 s^-1

#select dissociation rate 2 column
RDS2 = data[1:,6] # m^-3 s^-1

#select dissociation rate 3 column
RDS3 = data[1:,7] # m^-3 s^-1

#select dissociation rate 4 column
RDS4 = data[1:,8] # m^-3 s^-1

#select ionization rate 1 column
REI1 = data[1:,9] # m^-3 s^-1

#select ionization rate 2 column
REI2 = data[1:,10] # m^-3 s^-1

#select ionization rate 3 column
REI3 = data[1:,11] # m^-3 s^-1

#select fusion rate 1 column
RFS1 = data[1:,12] # m^-3 s^-1

#select recombination rate column
RRC = data[1:,13] # m^-3 s^-1

#select D source column
SD = data[1:,14] # m^-3 s^-1

#select D2 source column
SD2 = data[1:,15] # m^-3 s^-1

#select D2+ source column
SD2p = data[1:,16] # m^-3 s^-1

#select D+ source column
SDp = data[1:,17] # m^-3 s^-1

#select electron source column
Sem = data[1:,18] # m^-3 s^-1

#select T+ density column
n_Tp = data[1:,19] #m^-3 s^-1

#select dissociation rate coefficient 1 column
kDS1 = data[1:,21] # m^3 s^-1

#select dissociation rate coefficient 2 column
kDS2 = data[1:,22] # m^3 s^-1

#select dissociation rate coefficient 3 column
kDS3 = data[1:,23] # m^3 s^-1

#select dissociation rate coefficient 4 column
kDS4 = data[1:,24] # m^3 s^-1

#select ionization rate coefficient 1 column
kEI1 = data[1:,25] # m^3 s^-1

#select ionization rate coefficient 2 column
kEI2 = data[1:,26] # m^3 s^-1

#select ionization rate coefficient 3 column
kEI3 = data[1:,27] # m^3 s^-1

#select fusion rate coefficient 1 column
kFS1 = data[1:,28] # m^3 s^-1

#select recombination rate coefficient column
kRC = data[1:,29] # m^3 s^-1

##initial calculations
#steady state atomic ratio
R_a = 0
#temperature index
for n in range(0, 9):
  #density index
  for m in range(0, 9):
    R_a += a_ratio[n][m] * (math.log(n_e[-1]/1e14))**m * (math.log(T_e))**n

#steady state molecular ratio
R_m = 0
#temperature index
for n in range(0, 9):
  #density index
  for m in range(0, 9):
    R_m += m_ratio[n][m] * (math.log(n_e[-1]))**m * (math.log(T_e))**n

##plotting
#species densities
fig = plt.figure()
plt.title('Medium Molecular IC Densities')
plt.axhline(y=(math.exp(R_a))*n_D[-1],color='black',linestyle='--',label='Predicted n${}_{D^+}$')
plt.plot(time, n_D, color='green', label='n${}_D$')
plt.plot(time, n_Dp, color='red', label='n${}_{D^+}$')
plt.plot(time, n_e, color='purple',linestyle='--', label='n${}_e$')
plt.plot(time, n_D2, color='blue', label='n${}_{D_2}$')
plt.plot(time, n_D2p, color='orange', label='n${}_{D_2^+}$')
plt.yscale("log")
plt.ylim(1e7, 1e26)
plt.xscale("linear")
plt.xticks(range(0, 220, 20))
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Species Density (m${}^{-3}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("medium_ion_verification.png",dpi=600,bbox_inches='tight')

#reaction rates
fig = plt.figure()
plt.title('Medium Molecular IC Reaction Rates')
plt.plot(time, RDS1, label='RDS1')
plt.plot(time, RDS2, label='RDS2')
plt.plot(time, RDS3, label='RDS3')
plt.plot(time, RDS4, label='RDS4')
plt.plot(time, REI1, label='REI1')
plt.plot(time, REI2, label='REI2')
plt.plot(time, REI3, label='REI3')
plt.plot(time, RRC, label='RRC')
plt.plot(time, RFS1, label='RFS1')
plt.yscale("log")
plt.ylim(1e10, 1e27)
plt.xscale("linear")
plt.xticks(range(0, 220, 20))
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Reaction Rate (m${}^{-3}$ s${}^{-1}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("medium_ion_rates.png",dpi=600,bbox_inches='tight')

#reaction rate coefficients
fig = plt.figure()
plt.title('Medium Molecular IC Reaction Rate Coefficients')
plt.plot(time, kDS1, label='kDS1')
plt.plot(time, kDS2, label='kDS2')
plt.plot(time, kDS3, label='kDS3')
plt.plot(time, kDS4, label='kDS4')
plt.plot(time, kEI1, label='kEI1')
plt.plot(time, kEI2, label='kEI2')
plt.plot(time, kEI3, label='kEI3')
plt.plot(time, kRC, label='kRC')
plt.plot(time, kFS1, label='kFS1')
plt.yscale("log")
#plt.ylim(1e10, 1e27)
plt.xscale("linear")
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Reaction Rate Coefficient (m${}^{3}$ s${}^{-1}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("medium_ion_coefficients.png",dpi=600,bbox_inches='tight')


#source terms
fig = plt.figure()
plt.title('Medium Molecular IC Source Terms')
plt.plot(time, SD, color='green', label='S${}_D$')
plt.plot(time, SDp, color='red', label='S${}_{D^+}$')
plt.plot(time, Sem, color='purple',linestyle='--', label='S${}_e$')
plt.plot(time, SD2, color='blue', label='S${}_{D_2}$')
plt.plot(time, SD2p, color='orange', label='S${}_{D_2^+}$')
plt.yscale("symlog")
plt.yticks([-1e24, -1e21, -1e18, -1e15, -1e12, -1e9, -1e6, -1e3, 0, 1e3, 1e6, 1e9, 1e12, 1e15, 1e18, 1e21, 1e24])
plt.ylim(-1e25, 1e25)
plt.xscale("linear")
plt.xticks(range(0, 220, 20))
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Production Rate (m${}^{-3}$ s${}^{-1}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("medium_ion_sources.png",dpi=600,bbox_inches='tight')

###high molecular ion density case
##load data
#read and store tabulated data using genfromtxt, ignoring first line with strings
data = np.genfromtxt("I120-I216-N116-N28.csv",skip_header=1,delimiter=',')

#select time column
time = data[1:,0] # s

#select D2 density column
n_D2 = data[1:,1] # m^-3

#select D2+ density column
n_D2p = data[1:,2] # m^-3

#select D density column
n_D = data[1:,3] # m^-3

#select D+ density column
n_Dp = data[1:,4] # m^-3

#select electron density column
n_e = data[1:,20] # m^-3

#select dissociation rate 1 column
RDS1 = data[1:,5] # m^-3 s^-1

#select dissociation rate 2 column
RDS2 = data[1:,6] # m^-3 s^-1

#select dissociation rate 3 column
RDS3 = data[1:,7] # m^-3 s^-1

#select dissociation rate 4 column
RDS4 = data[1:,8] # m^-3 s^-1

#select ionization rate 1 column
REI1 = data[1:,9] # m^-3 s^-1

#select ionization rate 2 column
REI2 = data[1:,10] # m^-3 s^-1

#select ionization rate 3 column
REI3 = data[1:,11] # m^-3 s^-1

#select fusion rate 1 column
RFS1 = data[1:,12] # m^-3 s^-1

#select recombination rate column
RRC = data[1:,13] # m^-3 s^-1

#select D source column
SD = data[1:,14] # m^-3 s^-1

#select D2 source column
SD2 = data[1:,15] # m^-3 s^-1

#select D2+ source column
SD2p = data[1:,16] # m^-3 s^-1

#select D+ source column
SDp = data[1:,17] # m^-3 s^-1

#select electron source column
Sem = data[1:,18] # m^-3 s^-1

#select T+ density column
n_Tp = data[1:,19] #m^-3 s^-1

#select dissociation rate coefficient 1 column
kDS1 = data[1:,21] # m^3 s^-1

#select dissociation rate coefficient 2 column
kDS2 = data[1:,22] # m^3 s^-1

#select dissociation rate coefficient 3 column
kDS3 = data[1:,23] # m^3 s^-1

#select dissociation rate coefficient 4 column
kDS4 = data[1:,24] # m^3 s^-1

#select ionization rate coefficient 1 column
kEI1 = data[1:,25] # m^3 s^-1

#select ionization rate coefficient 2 column
kEI2 = data[1:,26] # m^3 s^-1

#select ionization rate coefficient 3 column
kEI3 = data[1:,27] # m^3 s^-1

#select fusion rate coefficient 1 column
kFS1 = data[1:,28] # m^3 s^-1

#select recombination rate coefficient column
kRC = data[1:,29] # m^3 s^-1

##initial calculations
#steady state atomic ratio
R_a = 0
#temperature index
for n in range(0, 9):
  #density index
  for m in range(0, 9):
    R_a += a_ratio[n][m] * (math.log(n_e[-1]/1e14))**m * (math.log(T_e))**n

#steady state molecular ratio
R_m = 0
#temperature index
for n in range(0, 9):
  #density index
  for m in range(0, 9):
    R_m += m_ratio[n][m] * (math.log(n_e[-1]))**m * (math.log(T_e))**n

##plotting
#species densities
fig = plt.figure()
plt.title('High Molecular IC Densities')
plt.axhline(y=(math.exp(R_a))*n_D[-1],color='black',linestyle='--',label='Predicted n${}_{D^+}$')
plt.plot(time, n_D, color='green', label='n${}_D$')
plt.plot(time, n_Dp, color='red', label='n${}_{D^+}$')
plt.plot(time, n_e, color='purple',linestyle='--', label='n${}_e$')
plt.plot(time, n_D2, color='blue', label='n${}_{D_2}$')
plt.plot(time, n_D2p, color='orange', label='n${}_{D_2^+}$')
plt.yscale("log")
plt.ylim(1e7, 1e26)
plt.xscale("linear")
plt.xticks(range(0, 220, 20))
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Species Density (m${}^{-3}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("high_ion_verification.png",dpi=600,bbox_inches='tight')

#reaction rates
fig = plt.figure()
plt.title('High Molecular IC Reaction Rates')
plt.plot(time, RDS1, label='RDS1')
plt.plot(time, RDS2, label='RDS2')
plt.plot(time, RDS3, label='RDS3')
plt.plot(time, RDS4, label='RDS4')
plt.plot(time, REI1, label='REI1')
plt.plot(time, REI2, label='REI2')
plt.plot(time, REI3, label='REI3')
plt.plot(time, RRC, label='RRC')
plt.plot(time, RFS1, label='RFS1')
plt.yscale("log")
plt.ylim(1e10, 1e27)
plt.xscale("linear")
plt.xticks(range(0, 220, 20))
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Reaction Rate (m${}^{-3}$ s${}^{-1}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("high_ion_rates.png",dpi=600,bbox_inches='tight')

#source terms
fig = plt.figure()
plt.title('High Molecular IC Source Terms')
plt.plot(time, SD, color='green', label='S${}_D$')
plt.plot(time, SDp, color='red', label='S${}_{D^+}$')
plt.plot(time, Sem, color='purple',linestyle='--', label='S${}_e$')
plt.plot(time, SD2, color='blue', label='S${}_{D_2}$')
plt.plot(time, SD2p, color='orange', label='S${}_{D_2^+}$')
plt.yscale("symlog")
plt.yticks([-1e24, -1e21, -1e18, -1e15, -1e12, -1e9, -1e6, -1e3, 0, 1e3, 1e6, 1e9, 1e12, 1e15, 1e18, 1e21, 1e24])
plt.ylim(-1e25, 1e25)
plt.xscale("linear")
plt.xticks(range(0, 220, 20))
plt.xlim(0, time[-1])
plt.xlabel("Time (s)")
plt.ylabel("Production Rate (m${}^{-3}$ s${}^{-1}$)")
plt.legend(bbox_to_anchor=(1.005, 0.5), loc='center left')
plt.grid(linestyle='--',alpha=0.9)
plt.draw()
plt.savefig("high_ion_sources.png",dpi=600,bbox_inches='tight')
