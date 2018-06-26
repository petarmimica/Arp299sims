#!/usr/bin/env python3

# change the name of this to your mass and energy file
mefile = "massen.dat"

# change the name of this file to your shock position file
spfile = "fsp-pos.dat"

# change the name of this variable to your beta figure file name
bfigname = "Arp299B-AT1-beta.png"

# change the name of this variable to your E_K figure file name
efigname = "Arp299B-AT1-E_K.png"

# preamble
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)
legfontP = FontProperties()

# generate ticks routine
def generate_log_ticks(min_pow10, max_pow10, min_i, max_i):
    ticks = []
    for k in range(min_pow10,max_pow10+1):
        for i in range(min_i,max_i+1):
            ticks.append(i*10**k)
    return ticks;
def generate_lin_ticks(min_val, max_val, nticks):
    ticks = []
    for k in range(0, nticks):
        ticks.append(min_val + (max_val - min_val) * k / (nticks - 1))
    return ticks;

# energy figure
# load the shock position data
# t: time in 1E16 cm / c
# r: position in 1E16 cm
# gsh: Lorentz factor of the shock front (estimated by SPEV)
raw_data = pd.read_table(spfile, header=None, sep="\s+", names = ['t', 'r', 'gsh'])
raw_data.drop(raw_data.index[0:1], inplace=True)
# critical radii
r_Sedov = 15.08 # Sedov radius (inside the torus)
r_f = 67.5 # torus size

# Compute the observer time (in days) corresponding to t and r
raw_data['Tobs'] = (raw_data['t'] - raw_data['r']) * 1E16 / 2.99792458E10 / 86400e0

# load the energy data
# t: time in 1E16 cm / c
# M: mass in code units
# Ek: energy in code units
raw_energy = pd.read_table(mefile, header=None, sep="\s+", names = ['t', 'M', 'Ek'])
#raw_energy = raw_energy1.iloc[1:]
# Convert to physical units
raw_energy['t'] = raw_energy['t'] + 1.00503781526E0
raw_energy['Ek'] = raw_energy['Ek'] * 2e0 * np.pi * (1e0 - np.cos(0.1e0)) * 1.67262158e-24 * 1e48 * (2.99792458e10)**2

# Save times as rounded integers (for merging purposes)
raw_data['tkey'] = (raw_data['t'] * 10000).round(1)
raw_data.tkey = raw_data.tkey.astype(int)
raw_energy['tkey'] = (raw_energy['t'] * 10000).round(1)
raw_energy.tkey = raw_energy.tkey.astype(int)

# Merge datasets
data = pd.merge(raw_data, raw_energy, on='tkey')

# Drop unnecessary variables
data = data.drop(['t_y','M','tkey'],axis=1)

# Compute the jet velocity
data['bsh'] = np.sqrt(1e0 - 1e0 / data['gsh']**2)
data['gammabeta'] = data['bsh'] * data['gsh']

# Find the rows corresponding to the Sedov radius and the torus edge
pos_r_Sedov=data.r[(data['r'] - r_Sedov).abs().argsort()[:1]].index.tolist()[0]
pos_r_f = data.r[(data['r'] - r_f).abs().argsort()[:1]].index.tolist()[0]

# Find the row corresponding to 1 day
pos_t_1 = data.r[(data['Tobs'] - 1e0).abs().argsort()[:1]].index.tolist()[0]

# show table rows corresponding to Sedov, pre- and post-jet breakout
print(pd.concat([data[pos_t_1:pos_t_1+1], data[pos_r_Sedov:pos_r_Sedov+1], data[pos_r_f:pos_r_f+1], 
           data[pos_r_f+5:pos_r_f+6]]))

print("t_x is the simulation time in units of 1E16 cm / c")
print("r is the simulation jet position in units of 1E16 cm /c")
print("Tobs = t_x - r, which is then converted to days")

# plot beta versus Tobs


# prepare the plot
sns.set_style('whitegrid')

_, p = plt.subplots(1, 1, sharex=True)
plt.rcParams['figure.figsize'] = (14, 6)

lw = 4
ms = 14

# Main plot
p.plot(data['Tobs'], data['bsh'],'k-', linewidth=4, label=r'$\beta_{\rm jet}$')
#p.plot([data.Tobs[pos_t_1], data.Tobs[pos_t_1]], [0.07, 1], 'r--', linewidth=3, label='early')
#p.plot([data.Tobs[pos_r_Sedov], data.Tobs[pos_r_Sedov]], [0.07, 1], 'b--', linewidth=3, label=r'$r_{\rm Sedov}$')
#p.plot([data.Tobs[pos_r_f], data.Tobs[pos_r_f]], [0.07, 1], 'g--', linewidth=3, label=r'$r_f$')
#p.plot([data.Tobs[pos_r_f + 5], data.Tobs[pos_r_f + 5]], [0.07, 1], 'm--', linewidth=3, label=r'$r_f + \Delta r_{acc}$')
p.plot([data.Tobs[pos_t_1], data.Tobs[pos_t_1]], [0.07, 1], 'r:', linewidth=3, label='early')
p.plot([data.Tobs[pos_r_Sedov], data.Tobs[pos_r_Sedov]], [0.07, 1], 'b-.', linewidth=3, label=r'$r_{\rm Sedov}$')
p.plot([data.Tobs[pos_r_f], data.Tobs[pos_r_f]], [0.07, 1], 'g--', linewidth=3, label=r'$r_f$')
p.plot([data.Tobs[pos_r_f + 5], data.Tobs[pos_r_f + 5]], [0.07, 1], 'm--', linewidth=3, label=r'$r_f + \Delta r_{acc}$')


# set logarithmic axes
p.set_xscale('log')
p.set_yscale('log')

# set labels
plt.rc('text', usetex=True)
p.set_xlabel(r'${\rm Epoch [days]}$', fontsize=32, fontweight = 'bold')
p.set_ylabel(r'$\beta_{\rm jet}$', fontsize=32, fontweight='bold')
#p.set_title("TDE jet velocity", fontsize=36)
p.tick_params(labelsize=24)

# plot range
plt.axis([0.1, 5000, 0.07, 1])

# x axis ticks
p.xaxis.set_ticks(generate_log_ticks(-1, 3, 1, 1))
p.xaxis.set_ticks(np.concatenate((generate_log_ticks(-1, 2, 2, 9), generate_log_ticks(3, 3, 2, 5))), minor=True) 

# y axis ticks
p.yaxis.set_ticks(generate_log_ticks(-1, 0, 1, 1))
p.yaxis.set_ticks(np.concatenate((generate_log_ticks(-1, -1, 2, 9), generate_log_ticks(-2, -2, 7, 9))), minor=True)

p.grid(False)

# set styles
p.tick_params(which='major', length=14, width=2)
p.tick_params(which='minor', length=9, width=1)
p.tick_params(which='both', direction="in")
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

handles, labels = p.get_legend_handles_labels()
legend = p.legend(handles, labels, ncol=1, prop=legfontP, loc='upper right')

# inset
a = plt.axes([0.65, 0.75, .15, .18]) #, facecolor='w')
#a.plot(data['Tobs'], data['bsh'],'k-', linewidth=4, label=r'$\beta_{\rm jet}$')
#a.plot([data.Tobs[pos_r_f], data.Tobs[pos_r_f]], [0.05, 1], 'g--', linewidth=3, label=r'$r_f$')
#a.plot([data.Tobs[pos_r_f + 5], data.Tobs[pos_r_f + 5]], [0.05, 1], 'm--', linewidth=3, label=r'$r_f + \Delta r_{acc}$')
a.plot(data['Tobs'], data['bsh'],'k-', linewidth=4, label=r'$\beta_{\rm jet}$')
a.plot([data.Tobs[pos_r_f], data.Tobs[pos_r_f]], [0.05, 1], 'g--', linewidth=2, label=r'$r_f$')
a.plot([data.Tobs[pos_r_f + 5], data.Tobs[pos_r_f + 5]], [0.05, 1], 'm--', linewidth=4, label=r'$r_f + \Delta r_{acc}$')
a.axis([770, 820, 0.05, 0.25])
a.grid(False)
a.set_xlabel(r'${\rm Time [days]}$', fontsize=22, fontweight = 'bold')
a.set_ylabel(r'$\beta_{\rm jet}$', fontsize=22, fontweight='bold')

for axis in ['top','bottom','left','right']:
    p.spines[axis].set_linewidth(2.5)
    p.spines[axis].set_color('k')

p.tick_params(axis='both', pad=10)
p.set_ylim((0.07, 1.1))
    
for axis in ['top','bottom','left','right']:
    a.spines[axis].set_linewidth(2.0)
    a.spines[axis].set_color('k')

plt.tight_layout()
#plt.show()

_, p = plt.subplots(1, 1, sharex=True)
plt.rcParams['figure.figsize'] = (14, 6)

lw = 4
ms = 14

# Main plot
p.plot(data['Tobs'], data['bsh'],'k-', linewidth=4, label=r'$\beta_{\rm jet}$')
#p.plot([data.Tobs[pos_t_1], data.Tobs[pos_t_1]], [0.07, 1], 'r--', linewidth=3, label='early')
#p.plot([data.Tobs[pos_r_Sedov], data.Tobs[pos_r_Sedov]], [0.07, 1], 'b--', linewidth=3, label=r'$r_{\rm Sedov}$')
#p.plot([data.Tobs[pos_r_f], data.Tobs[pos_r_f]], [0.07, 1], 'g--', linewidth=3, label=r'$r_f$')
#p.plot([data.Tobs[pos_r_f + 5], data.Tobs[pos_r_f + 5]], [0.07, 1], 'm--', linewidth=3, label=r'$r_f + \Delta r_{acc}$')
p.plot([data.Tobs[pos_t_1], data.Tobs[pos_t_1]], [0.07, 1], 'r:', linewidth=3, label='early')
p.plot([data.Tobs[pos_r_Sedov], data.Tobs[pos_r_Sedov]], [0.07, 1], 'b-.', linewidth=3, label=r'$r_{\rm Sedov}$')
p.plot([data.Tobs[pos_r_f], data.Tobs[pos_r_f]], [0.07, 1], 'g--', linewidth=3, label=r'$r_f$')
p.plot([data.Tobs[pos_r_f + 5], data.Tobs[pos_r_f + 5]], [0.07, 1], 'm--', linewidth=3, label=r'$r_f + \Delta r_{acc}$')


# set logarithmic axes
p.set_xscale('log')
p.set_yscale('log')

# set labels
plt.rc('text', usetex=True)
p.set_xlabel(r'${\rm Epoch [days]}$', fontsize=32, fontweight = 'bold')
p.set_ylabel(r'$\beta_{\rm jet}$', fontsize=32, fontweight='bold')
#p.set_title("TDE jet velocity", fontsize=36)
p.tick_params(labelsize=24)

# plot range
plt.axis([0.1, 5000, 0.07, 1])

# x axis ticks
p.xaxis.set_ticks(generate_log_ticks(-1, 3, 1, 1))
p.xaxis.set_ticks(np.concatenate((generate_log_ticks(-1, 2, 2, 9), generate_log_ticks(3, 3, 2, 5))), minor=True) 

# y axis ticks
p.yaxis.set_ticks(generate_log_ticks(-1, 0, 1, 1))
p.yaxis.set_ticks(np.concatenate((generate_log_ticks(-1, -1, 2, 9), generate_log_ticks(-2, -2, 7, 9))), minor=True)

p.grid(False)

# set styles
p.tick_params(which='major', length=14, width=2)
p.tick_params(which='minor', length=9, width=1)
p.tick_params(which='both', direction="in")
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

handles, labels = p.get_legend_handles_labels()
legend = p.legend(handles, labels, ncol=1, prop=legfontP, loc='upper right')

# inset
a = plt.axes([0.65, 0.75, .15, .18]) #, facecolor='w')
#a.plot(data['Tobs'], data['bsh'],'k-', linewidth=4, label=r'$\beta_{\rm jet}$')
#a.plot([data.Tobs[pos_r_f], data.Tobs[pos_r_f]], [0.05, 1], 'g--', linewidth=3, label=r'$r_f$')
#a.plot([data.Tobs[pos_r_f + 5], data.Tobs[pos_r_f + 5]], [0.05, 1], 'm--', linewidth=3, label=r'$r_f + \Delta r_{acc}$')
a.plot(data['Tobs'], data['bsh'],'k-', linewidth=4, label=r'$\beta_{\rm jet}$')
a.plot([data.Tobs[pos_r_f], data.Tobs[pos_r_f]], [0.05, 1], 'g--', linewidth=2, label=r'$r_f$')
a.plot([data.Tobs[pos_r_f + 5], data.Tobs[pos_r_f + 5]], [0.05, 1], 'm--', linewidth=4, label=r'$r_f + \Delta r_{acc}$')
a.axis([770, 820, 0.05, 0.25])
a.grid(False)
a.set_xlabel(r'${\rm Time [days]}$', fontsize=22, fontweight = 'bold')
a.set_ylabel(r'$\beta_{\rm jet}$', fontsize=22, fontweight='bold')

for axis in ['top','bottom','left','right']:
    p.spines[axis].set_linewidth(2.5)
    p.spines[axis].set_color('k')

p.tick_params(axis='both', pad=10)
p.set_ylim((0.07, 1.1))
    
for axis in ['top','bottom','left','right']:
    a.spines[axis].set_linewidth(2.0)
    a.spines[axis].set_color('k')

plt.tight_layout()
#plt.show()


# save to file
plt.savefig(bfigname)

# Generate the kinetic energy - gammabeta figure

# prepare plot
sns.set_style('whitegrid')
_, p2 = plt.subplots(1, 1, sharex=True)
plt.rcParams['figure.figsize'] = (14, 6)

# plot
ms = 20
p2.plot(data['gammabeta'], data['Ek'] / 1e51,'k-', linewidth=4, label='jet')
#p2.plot(data.gammabeta[pos_t_1], data.Ek[pos_t_1]/1e51, 'ro', ms=ms,label='early')
#p2.plot(data.gammabeta[pos_r_Sedov], data.Ek[pos_r_Sedov]/1e51, 'bo', ms=ms,label=r'$r_{\rm Sedov}$')
#p2.plot(data.gammabeta[pos_r_f], data.Ek[pos_r_f]/1e51, 'go', ms=ms,label=r'$r_f$')
#p2.plot(data.gammabeta[pos_r_f + 5], data.Ek[pos_r_f + 5]/1e51, 'mo', ms=ms,label=r'$r_f + \Delta r_{acc}$')
p2.plot(data.gammabeta[pos_t_1], data.Ek[pos_t_1]/1e51, 'ro', ms=ms,label='early')
p2.plot(data.gammabeta[pos_r_Sedov], data.Ek[pos_r_Sedov]/1e51, 'b^', ms=ms,label=r'$r_{\rm Sedov}$')
p2.plot(data.gammabeta[pos_r_f], data.Ek[pos_r_f]/1e51, 'gs', ms=ms,label=r'$r_f$')
p2.plot(data.gammabeta[pos_r_f + 5], data.Ek[pos_r_f + 5]/1e51, 'mp', ms=ms+3,label=r'$r_f + \Delta r_{acc}$')

lw = 4
ms = 14

plt.rc('text', usetex=True)

# set logarithmic axes
p2.set_xscale('log')
p2.set_yscale('log')

# set labels
p2.set_xlabel(r'$\Gamma \beta$', fontsize=32, fontweight='bold')
p2.set_ylabel(r'$E_K / 10^{51}$ erg', fontsize=32, fontweight = 'bold')
#p2.set_title("TDE jet energy and four-velocity", fontsize=36)
p2.tick_params(labelsize=24)

# plot range
plt.axis([0.05, 10, 0.1, 2.5])

# x axis ticks
p2.xaxis.set_ticks(generate_log_ticks(-1, 1, 1, 1))
p2.xaxis.set_ticks(np.concatenate((generate_log_ticks(-2, -2, 5, 9), generate_log_ticks(-1, 0, 2, 9))), minor=True) 

# y axis ticks
p2.yaxis.set_ticks(generate_log_ticks(0, 0, 1, 1))
p2.yaxis.set_ticks(np.concatenate((generate_log_ticks(-1, -1, 2, 9), generate_log_ticks(0, 0, 2, 2))), minor=True)

p2.grid(False)

# set styles
p2.tick_params(which='major', length=14, width=2)
p2.tick_params(which='minor', length=9, width=1)
p2.tick_params(which='both', direction="in")
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

handles2, labels2 = p2.get_legend_handles_labels()
legend = p2.legend(handles2, labels2, ncol=1, prop=legfontP, loc='upper right')

for axis in ['top','bottom','left','right']:
    p2.spines[axis].set_linewidth(2.5)
    p2.spines[axis].set_color('k')

p2.tick_params(axis='x', pad=10)
p2.set_xlim((0.05,12.))
plt.tight_layout()

# save to file
plt.savefig(efigname)
