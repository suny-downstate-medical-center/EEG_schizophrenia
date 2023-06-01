import mne
from mne.preprocessing import EOGRegression

base_dir = '/Users/scottmcelroy/smm_code/A1_scz/A1_raw_data/organized_data/cond_D/TI001C40.bdf'

raw = mne.io.read_raw_bdf(base_dir)

raw.load_data()
# maybe use
raw.set_channel_types({'HEO1': 'eog', 'HEO2': 'eog', 'VEO1': 'eog', 'VEO2': 'eog',
                       'NOSE': 'misc', 'M1': 'misc', 'M2': 'misc', 'EXG8': 'misc'})
raw.set_eeg_reference(['NOSE'])
std_montage = mne.channels.make_standard_montage('biosemi64')
raw = raw.set_montage(std_montage, on_missing='warn')

n_time_samps = raw.n_times
time_secs = raw.times
ch_names = raw.ch_names
n_chan = len(ch_names)

raw.resample(1000)


# Bandpass and notch filtering data
filt = raw.copy().filter(1, 100)
filtered = filt.notch_filter(60)
filtered.plot_psd(fmax=100)
eog_evoked = mne.preprocessing.create_eog_epochs(raw).average(picks='all')
eog_evoked.apply_baseline((None, None))
eog_evoked.plot_joint()
projs, events = mne.preprocessing.compute_proj_eog(raw, average=True)
print(projs)