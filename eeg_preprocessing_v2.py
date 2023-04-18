import numpy as np
import mne
from mne.preprocessing import EOGRegression

# Establish plot standards
plot_kwargs = dict(picks='all', ylim=dict(eeg=(-5, 10), eog=(-20, 50)))

# Load EEG data and define non-standard channels (set up iterative loop once mne figured out)
raw = mne.io.read_raw_bdf(
    "/Users/scottmcelroy/Desktop/eeg_ctrl/TI009D140A.bdf")
raw.load_data()
raw.set_channel_types({'HEO1': 'eog','HEO2': 'eog','VEO1': 'eog','VEO2': 'eog'})
raw.set_eeg_reference('average')
raw.drop_channels(['M1', 'M2', 'NOSE', 'EXG8'])
# Set EEG Montage for Electrode Locations
std_montage = mne.channels.make_standard_montage('biosemi64')
raw.set_montage(std_montage, on_missing='warn')
# events, new_triggers = mne.events_from_annotations(raw)

n_time_samps = raw.n_times
time_secs = raw.times
ch_names = raw.ch_names
n_chan = len(ch_names)

# Measure of signal's power content versus frequency. A PSD is typically used to characterize broadband random signals
# raw.plot_psd(fmax=210)
# raw_plot = raw.plot(duration=5, n_channels=72)
# spectrum = raw.compute_psd()
# spectrum.plot(average=True)

# Bandpass and notch filtering data
raw = raw.filter(0.1, 100)
raw = raw.notch_filter(60)
# notch.plot_psd(fmax=100)

reject_criteria = dict(eeg=100e-6, eog=250e-6)

events = mne.find_events(raw)
event_ids = {'Background':4, 'Button Press':8, 'Distractor':100, 'B':128, 'Target':200}
fig = mne.viz.plot_events(events, event_id=event_ids, sfreq=raw.info['sfreq'])
epochs = mne.Epochs(raw, events, event_id=event_ids, tmin=-0.1, tmax=1, preload=True)

fig = epochs.average('all').plot(**plot_kwargs)

model_plain = EOGRegression(picks='eeg', picks_artifact='eog').fit(epochs)

# create epochs with the evoked subtracted out
epochs_sub = epochs.copy().subtract_evoked()

# perform regression
model_sub = EOGRegression(picks='eeg', picks_artifact='eog').fit(epochs_sub)

# These two lines plot epochs on head models
# fig = model_sub.plot(vlim=(None, 0.4))
# fig.set_size_inches(3, 2)

# apply the regression coefficients to the original epochs
epochs_clean_sub = model_plain.apply(epochs).apply_baseline()
fig = epochs_clean_sub.average('all').plot(**plot_kwargs)
fig.set_size_inches(6, 6)

order = np.concatenate([mne.pick_types(raw.info, eog=True),
                       mne.pick_types(raw.info, eeg=True)])

raw_kwargs = dict(events=events, order=order, start=13, duration=3, n_channels=10, scalings=dict(eeg=50e-6, eog=250e-6))

# plot original data
raw.plot(**raw_kwargs)

# regress (using coefficients computed previously) and plot
raw_clean = model_sub.apply(raw)
raw_clean.plot(**raw_kwargs)

# raw.plot_psd(picks = ['Fz'], fmax=110)

oddball = epochs['Background']
oddball.plot_image(combine='mean')
# oddball.plot_psd(picks = ['Pz'], fmax = 100)

'''
V2 = Change from Original is that I will be using Gratton's method from the paper for blink artifacts
this method also calls for epoching data before removing artifacts
'''

'''

# Find EOG events for eyeblink artifacts

eog_evoked = mne.preprocessing.create_eog_epochs(notch) #baseline=(-0.5, -0.2)
# eog_evoked.plot_image(combine='mean')
# eog_evoked.average('all').plot(**plot_kwargs)

model_plain = mne.preprocessing.EOGRegression(picks='eeg', picks_artifact='eog').fit(eog_evoked)
#eog_evoked.apply_baseline(baseline=(None, -0.2))
#eog_evoked.plot_joint()
# fig = model_plain.plot(vlim=(None, 0.4))
# fig.set_size_inches(3, 2)

epochs_clean_plain = model_plain.apply(eog_evoked)
# Redo the baseline correction after regression
epochs_clean_plain.apply_baseline()
# Show the evoked potential computed on the corrected data
# fig = epochs_clean_plain.average('all').plot(**plot_kwargs)
# fig.set_size_inches(6, 6)

# epochs_clean_plain.plot()
# raw.plot()
'''