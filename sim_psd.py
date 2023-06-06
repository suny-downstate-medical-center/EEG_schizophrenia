"""
Load .pkl files of NetPyNE and saves a PSD plot
TODO fix hardcoded path, pick better dipole location than parietal, trim down number of EEG leads
"""
import mne
import pickle
import numpy as np
import netpyne
import lfpykit
from lfpykit.eegmegcalc import NYHeadModel
import os

# Import head model for EEG lead locations

nyhead = NYHeadModel(nyhead_file=os.getenv('NP_LFPYKIT_HEAD_FILE', None))

# Load pkl file

file = open('/Users/scottmcelroy/smm_code/A1_sim_data/v34_batch53_0_0_data.pkl', 'rb')
data = pickle.load(file)

# Set dipole location

nyhead.set_dipole_pos('parietal_lobe')
nyhead.find_closest_electrode()

# Convert sim data to be in EEG format

M = nyhead.get_transformation_matrix()
timeRange = [0, 5000]
timeSteps = [int(timeRange[0] / 0.05), int(timeRange[1] / 0.05)]

# Set params to be readable by MNE

sfreq = 2500
times = np.arange(0, 5000, 0.05)
ch_types = ['eeg']*231
ch_names = []
p = data['simData']['dipoleSum']
p = np.array(p).T
p = p[:, timeSteps[0]:timeSteps[1]]
t = np.arange(timeRange[0], timeRange[1], 0.05)

# Rotate dipole to head surface and convert to appropriate units

p = nyhead.rotate_dipole_to_surface_normal(p)
eeg = M @ p * 1e3  # [mV] -> [uV] unit conversion

# Set channel names

for x in range(0, 231):
    ch_names = ch_names + [str(x)]
# for n in dipoles:
#    ch_names = np.append(ch_names, str(n))

# Create raw.info for MNE

info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)

# Create MNE Raw Array

raw = mne.io.RawArray(eeg, info)
raw.load_data()

# Generate and save PSD

fig = raw.plot_psd(picks = ['38'], fmax=90)
#fig.canvas.manager.full_screen_toggle()
fig.savefig('sim_psd.png', bbox_inches='tight')
print("saved")
