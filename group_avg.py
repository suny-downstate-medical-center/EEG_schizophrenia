# TODO - Evaluate value error


import mne
import glob

conditions = ['Background', 'Target']

base_dir = '/Users/scottmcelroy/A1_scz/A1_exp_data/organized_data/mne_evoked/cond_D/'
data_files = glob.glob(base_dir + '*ave.fif')

evokeds = {}

for idx, c in enumerate(conditions):
    evokeds[c] = [mne.read_evokeds(d)[idx] for d in data_files]

std = evokeds['Background']
dev = evokeds['Target']

ave_std = mne.grand_average(std)
ave_dev = mne.grand_average(dev)
ave_std.plot_psd(fmax=100)

kwargs = dict(fmin=2, fmax=40, n_jobs=None)
# freqs = np.logspace(*np.log10([6, 35]), num=8)
# n_cycles = freqs / 2.  # different number of cycle per frequency
# power_std, itc = tfr_morlet(ave_std, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                       # return_itc=False, decim=3, n_jobs=None)

# power_dev, itc = tfr_morlet(epochs, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                       # return_itc=False, decim=3, n_jobs=None)
evokeds_diff = mne.combine_evoked([ave_dev, ave_std],
                                   weights=[1, -1])

mne.viz.plot_compare_evokeds({'Mismatch-Match': evokeds_diff},
                              show_sensors='upper right',
                             combine='mean',
                             title='Difference Wave',
                             );
