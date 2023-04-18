import mne


# Establish plot standards
plot_kwargs = dict(picks='all', ylim=dict(eeg=(-5, 10), eog=(-20, 50)))

# Load EEG data and define non-standard channels (set up iterative loop once mne figured out)
raw = mne.io.read_raw_bdf(
    "/Users/scottmcelroy/smm_code/sdlab_data/THC-IOM_for_Salva/TI001-SA244/Day 4/postTI001D30.bdf")
raw.load_data()
raw.set_channel_types({'HEO1': 'eog'})
raw.set_channel_types({'HEO2': 'eog'})
raw.set_channel_types({'VEO1': 'eog'})
raw.set_channel_types({'VEO2': 'eog'})
raw.set_eeg_reference('average')
raw.drop_channels(['M1', 'M2', 'NOSE', 'EXG8'])

# Set EEG Montage for Electrode Locations
std_montage = mne.channels.make_standard_montage('biosemi64')
raw.set_montage(std_montage, on_missing='warn')

#events, new_triggers = mne.events_from_annotations(raw)

n_time_samps = raw.n_times
time_secs = raw.times
ch_names = raw.ch_names
n_chan = len(ch_names)

# Measure of signal's power content versus frequency. A PSD is typically used to characterize broadband random signals
'''raw.plot_psd(fmax=210)
raw_plot = raw.plot(duration=5, n_channels=72)
spectrum = raw.compute_psd()
spectrum.plot(average=True)'''

# Bandpass and notch filtering data
bandpass = raw.filter(0.1, 100)
notch = bandpass.notch_filter(60)
# notch.plot_psd(fmax=100)


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

tones = mne.find_events(raw)
event_dict = {'A': 2, 'B': 8, 'C': 100, 'Target': 200, 'D': 65663}
fig = mne.viz.plot_events(tones, event_id=event_dict, sfreq=raw.info['sfreq'])

reject_criteria = dict(eeg=150e-6,eog=250e-6)
epochs = mne.Epochs(raw, tones, event_id=event_dict, tmin=-0.05, tmax=0.15, preload=True)

oddball = epochs['Target']
oddball.plot_image(picks = ['Pz'])

#oddball.plot_image(picks = ['TP8', 'TP7', 'P7', 'P8', 'O1', 'O2', 'Pz', 'POz', 'PO4', 'PO8', 'P10', 'P6', 'P4',
                            #'CP6', 'CP5', 'P9', 'P5', 'P3', 'PO7', 'PO3'])
