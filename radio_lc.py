#!/usr/bin/env python3

# change the name of this to your light curve filename roots
filename = "lc"

# change the name of this variable to your figure file name
figname = "Arp299B-AT1-radio_lc.png"

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
legfontP.set_size(20)

# load simulation light curve
sim166_thick = pd.read_table(filename+"-thick-1.66d9.dat", header=None, sep="\s+", names = ['time', 'lum'])
sim499_thick = pd.read_table(filename+"-thick-4.99d9.dat", header=None, sep="\s+", names = ['time', 'lum'])
sim842_thick = pd.read_table(filename+"-thick-8.42d9.dat", header=None, sep="\s+", names = ['time', 'lum'])


# load data
raw_data = pd.read_excel("AT1_data.xlsx");

# Explosion time
expl_times = raw_data['time'] - raw_data['t_exp']
expl_time = np.unique(expl_times)[0]

# clean the latest data
Mpc = 1e6 * 3.0857e18 # megaparsec
muJy = 1e-6 * 1e-23 # micro-Jansky
dist = 44.8e0 * Mpc # distance to the source


# fix the frequencies
raw_data['freq'] = raw_data['freq'].replace(8.44,8.42)
raw_data['freq'] = raw_data['freq'].replace(1.54,1.66)

# convert fluxes to luminosities
raw_data['lum'] = raw_data['tflux'].astype(float) * muJy * 4e0 * np.pi * dist**2 * raw_data['freq'] * 1e9
raw_data['lum_err'] = raw_data['err_tflux'].astype(float) * muJy * 4e0 * np.pi * dist**2 * raw_data['freq'] * 1e9
raw_data['time'] = raw_data['time'] - expl_time

# keep only needed data
full_data = raw_data

# separate the data by freqency
obs166 = full_data.loc[full_data['freq'] == 1.66]
obs499 = full_data.loc[full_data['freq'] == 4.99]
obs842 = full_data.loc[full_data['freq'] == 8.42]

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



## plot radio lcs
_, p = plt.subplots(1, 1, sharex=True)
plt.rcParams['figure.figsize'] = (14, 6)
lw = 4
ms = 14
p.plot(sim842_thick['time'], sim842_thick['lum'] / 8.4e9,'r--', linewidth=lw, label='8.4 GHz')
p.plot(sim499_thick['time'], sim499_thick['lum'] /4.99e9,'b-.', linewidth=lw, label='5 GHz')
p.plot(sim166_thick['time'], sim166_thick['lum'] / 1.66e9,'g-', linewidth=lw, label='1.7 GHz')
p.errorbar(obs842['time'], obs842['lum'] / 8.42e9, 3*obs842['lum_err'] / 8.42e9, None, 'rs', label='',markersize=ms)
p.errorbar(obs499['time'], obs499['lum'] / 4.99e9, 3*obs499['lum_err'] / 4.99e9, None, 'bp', label='',markersize=ms+4)
p.errorbar(obs166['time'], obs166['lum'] / 1.66e9, 3*obs166['lum_err'] / 1.66e9, None, 'go', label='',markersize=ms+2)
sns.set_style('whitegrid')

plt.rc('text', usetex=True)
p.set_xscale('linear')
p.set_yscale('log')
p.set_xlabel(r'${\rm Epoch\, (days)}$', fontsize=32, fontweight='bold')
p.set_ylabel(r'$L_\nu\ \left({\rm erg\ s}^{-1} {\rm Hz}^{-1}\right)$', fontsize=32, fontweight='bold')

plt.rc('text', usetex=False)
p.tick_params(labelsize=24)

plt.axis([2e1, 5e3, 5e24, 1e30])
p.xaxis.set_ticks(generate_lin_ticks(1000, 5000, 5))
p.xaxis.set_ticks(generate_lin_ticks(100, 5000, 50), minor=True) 
p.set_ylim(1e26, 3e29)
p.set_yscale('log')
p.grid(False)
p.tick_params(which='major', length=14, width=2)
p.tick_params(which='minor', length=9, width=1)
p.tick_params(which='both', direction="in")

handles, labels = p.get_legend_handles_labels()
legend = p.legend(handles, labels, ncol=1, prop=legfontP, loc='upper right')

for axis in ['top','bottom','left','right']:
    p.spines[axis].set_linewidth(2.5)
    p.spines[axis].set_color('k')

plt.text(200, 1e29, 'A', fontsize=35, color='k')
plt.tight_layout()

## plot radio lcs
_, p = plt.subplots(1, 1, sharex=True)
plt.rcParams['figure.figsize'] = (14, 6)
lw = 4
ms = 14
p.plot(sim842_thick['time'], sim842_thick['lum'] / 8.4e9,'r--', linewidth=lw, label='8.4 GHz')
p.plot(sim499_thick['time'], sim499_thick['lum'] /4.99e9,'b-.', linewidth=lw, label='5 GHz')
p.plot(sim166_thick['time'], sim166_thick['lum'] / 1.66e9,'g-', linewidth=lw, label='1.7 GHz')
p.errorbar(obs842['time'], obs842['lum'] / 8.42e9, 3*obs842['lum_err'] / 8.42e9, None, 'rs', label='',markersize=ms)
p.errorbar(obs499['time'], obs499['lum'] / 4.99e9, 3*obs499['lum_err'] / 4.99e9, None, 'bp', label='',markersize=ms+4)
p.errorbar(obs166['time'], obs166['lum'] / 1.66e9, 3*obs166['lum_err'] / 1.66e9, None, 'go', label='',markersize=ms+2)
sns.set_style('whitegrid')

plt.rc('text', usetex=True)
p.set_xscale('linear')
p.set_yscale('log')
p.set_xlabel(r'${\rm Epoch\, (days)}$', fontsize=32, fontweight='bold')
p.set_ylabel(r'$L_\nu\ \left({\rm erg\ s}^{-1} {\rm Hz}^{-1}\right)$', fontsize=32, fontweight='bold')

plt.rc('text', usetex=False)
p.tick_params(labelsize=24)

plt.axis([2e1, 5e3, 5e24, 1e30])
p.xaxis.set_ticks(generate_lin_ticks(1000, 5000, 5))
p.xaxis.set_ticks(generate_lin_ticks(100, 5000, 50), minor=True) 
p.set_ylim(1e26, 3e29)
p.set_yscale('log')
p.grid(False)
p.tick_params(which='major', length=14, width=2)
p.tick_params(which='minor', length=9, width=1)
p.tick_params(which='both', direction="in")

handles, labels = p.get_legend_handles_labels()
legend = p.legend(handles, labels, ncol=1, prop=legfontP, loc='upper right')

for axis in ['top','bottom','left','right']:
    p.spines[axis].set_linewidth(2.5)
    p.spines[axis].set_color('k')

plt.text(200, 1e29, 'A', fontsize=35, color='k')
plt.tight_layout()

plt.savefig(figname)
