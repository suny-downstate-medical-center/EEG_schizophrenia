# TODO - Evaluate value error


import numpy as np
import mne
from mne.time_frequency import tfr_morlet
import glob
import os
conditions = ['Background', 'Target']

base_dir = '/Users/scottmcelroy/smm_code/A1_scz/A1_raw_data/organized_data/test/'
data_files = glob.glob(base_dir + '*.fif')

evokeds = {}

for idx, c in enumerate(conditions):
    evokeds[c] = [mne.read_evokeds(d)[idx] for d in data_files]

std = evokeds['Background']
dev = evokeds['Target']

ave_std = mne.grand_average(std)
ave_dev = mne.grand_average(dev)
ave_std.plot_psd(fmax=100)
'''
kwargs = dict(fmin=2, fmax=40, n_jobs=None)
# freqs = np.logspace(*np.log10([6, 35]), num=8)
# n_cycles = freqs / 2.  # different number of cycle per frequency
# power_std, itc = tfr_morlet(ave_std, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                       # return_itc=False, decim=3, n_jobs=None)

# power_dev, itc = tfr_morlet(epochs, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                       # return_itc=False, decim=3, n_jobs=None)
ave_std.plot_psd(['Cz'], baseline=(-0.5, 0), mode='logratio', title= 'Standard')
ave_dev.plot_psd(['Cz'], baseline=(-0.5, 0), mode='logratio', title= 'Deviant')
'''