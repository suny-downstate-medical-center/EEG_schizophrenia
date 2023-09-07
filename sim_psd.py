"""
Load .pkl files of NetPyNE and saves a PSD plot
TODO fix hardcoded path, pick better dipole location than parietal, trim down number of EEG leads
"""
import mne
import pickle
import numpy as np
from lfpykit.eegmegcalc import NYHeadModel
import os
import matplotlib.pyplot as plt

# Import head model for EEG lead locations

nyhead = NYHeadModel(nyhead_file=os.getenv('NP_LFPYKIT_HEAD_FILE', None))

# Load pkl file

file = open('/Users/scottmcelroy/A1_scz/A1_sim_data/Control_40Hz_10seeds/Control_40Hz_9_data.pkl', 'rb')
data = pickle.load(file)
# Set dipole location

nyhead.set_dipole_pos('parietal_lobe')
nyhead.find_closest_electrode()

# Convert sim data to be in EEG format

M = nyhead.get_transformation_matrix()
timeRange = [0, data['simConfig']['duration']]
timeSteps = [int(timeRange[0] / 0.05), int(timeRange[1] / data['simConfig']['recordStep'])]

# Set params to be readable by MNE

sfreq = 20000
times = np.arange(0, 260000, 0.05)
ch_types = ['eeg']*231 + ['stim']
ch_names = []
p = data['simData']['dipoleSum']
p = np.array(p).T
p = p[:, timeSteps[0]:timeSteps[1]]
t = np.arange(timeRange[0], timeRange[1], data['simConfig']['recordStep'])

# Rotate dipole to head surface and convert to appropriate units

p = nyhead.rotate_dipole_to_surface_normal(p)
eeg = M @ p * 1e6   # [mV] -> [uV] unit conversion

# Set channel names

for x in range(0, 231):
    ch_names = ch_names + [str(x)]

ch_names = ch_names + ['STIM']

# Create raw.info for MNE



# insert stim channel to create epoch

stim = np.zeros(shape=(1, 129999))
stim = np.insert(stim, 30000, 1)
eeg = np.append(eeg, stim.reshape(1, 130000), axis=0)

info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
raw = mne.io.RawArray(eeg, info)

raw = raw.filter(0.1, 100)

info['description'] = 'sim_data_test'
events = mne.find_events(raw)
event_id = {'stim' : 1}

epochs = mne.Epochs(raw, events, event_id=event_id, preload=True, tmin=-0.5, tmax=1)

evoked = epochs['stim'].average()

# Generate and save PSD

# fig = epochs.plot_psd(picks = ['38'], fmax=90)
# fig = epochs["stim"].plot()
fig = evoked.plot(picks=[38])
fig.canvas.manager.full_screen_toggle()
fig.savefig('sim_epoch_10e6.png', bbox_inches='tight')
print("saved")

