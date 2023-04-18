import mne
import pickle
import numpy as np
import netpyne
from lfpykit.eegmegcalc import NYHeadModel
import matplotlib
import hnn_core


nyhead = NYHeadModel('/Users/scottmcelroy/smm_code/A1_scz/sa_nyhead.mat')

file = open('/Users/scottmcelroy/smm_code/A1_scz/v34_batch_eeg_plot_0_0_data.pkl', 'rb')
data = pickle.load(file)


nyhead.set_dipole_pos('parietal_lobe')
M = nyhead.get_transformation_matrix()
timeRange = [0, 5000]
timeSteps = [int(timeRange[0] / 0.05), int(timeRange[1] / 0.05)]

sfreq = 2500
times = np.arange(0, 5000, 0.05)
ch_types = ['eeg']*231
ch_names = []
p = data['simData']['dipoleSum']
p = np.array(p).T
p = p[:, timeSteps[0] : timeSteps[1]]
t = np.arange(timeRange[0], timeRange[1], 0.05)

p = nyhead.rotate_dipole_to_surface_normal(p)
eeg = M @ p * 1e6  # [mV] -> [uV] unit conversion

for x in range(0, 231):
    ch_names = ch_names + [str(x)]
# for n in dipoles:
#    ch_names = np.append(ch_names, str(n))

info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)


raw = mne.io.RawArray(eeg, info)
raw.load_data()
fig = raw.plot()
fig = raw.plot_psd(fmax = 90)

fig.canvas.manager.full_screen_toggle()
fig.savefig('test_fig.png', bbox_inches='tight')
# fig.grab().save('screenshot_full.png')
print("saved")