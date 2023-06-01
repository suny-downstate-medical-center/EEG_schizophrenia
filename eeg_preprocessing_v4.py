"""
Load raw EEG files, filters, EOG regression and epoching - bad epochs are rejected
Output is filtered and regressed EEG epochs
"""

import mne
from mne.preprocessing import EOGRegression
import os

plot_kwargs = dict(picks='all', ylim=dict(eeg=(-10, 10), eog=(-5, 15)))

base_dir = '/Users/scottmcelroy/smm_code/A1_scz/A1_exp_data/organized_data/cond_D/'
for file in os.listdir(base_dir):
    if file.endswith('.bdf'):
        raw = mne.io.read_raw_bdf(os.path.join(base_dir, file))
        fname = file[0:5]
        raw.load_data()

# Define misc channels not in montage
        raw.set_channel_types({'HEO1': 'eog', 'HEO2': 'eog', 'VEO1': 'eog', 'VEO2': 'eog',
                               'NOSE': 'misc', 'M1': 'misc', 'M2': 'misc', 'EXG8': 'misc'})
        raw.set_eeg_reference(['NOSE'])
# Set EEG Montage for Electrode Locations

        std_montage = mne.channels.make_standard_montage('biosemi64')
        raw = raw.set_montage(std_montage, on_missing='warn')

        n_time_samps = raw.n_times
        time_secs = raw.times
        ch_names = raw.ch_names
        n_chan = len(ch_names)
# Bandpass and notch filtering data

        filt = raw.copy().filter(0.1, 100)
        filtered = filt.notch_filter(60)
        # raw.resample(1230)

# establish flat and reject criteria for bad channels
        reject_criteria = dict(eeg=100e-6, eog=200e-6)
        flat_criteria = dict(eeg=1e-6)

# Find events and epoch data using rejection criteria
        events = mne.find_events(filtered)
        event_id = {'Background': 4, 'Target': 200}
        epochs = mne.Epochs(filtered, events, event_id=event_id, preload=True,
                            reject=reject_criteria, flat=flat_criteria)
        epochs['Background'].plot_psd(method='auto', fmax=100)
        epochs['Background'].average().plot_psd(method='auto', fmax=100)
        #epochs.average().plot_psd(method='auto',xscale='log', fmax=100)

        # epochs['Background'].plot_psd(fmax=100)

# plot the evoked for the EEG and the EOG sensors
        # fig = epochs.average('all').plot(**plot_kwargs)
        # fig.set_size_inches(6, 6)
        model_plain = EOGRegression(picks='eeg', picks_artifact='eog').fit(epochs)
        epochs_clean_plain = model_plain.apply(epochs)
        # After regression, we should redo the baseline correction
        epochs_clean_plain.apply_baseline()

# Show the evoked potential computed on the corrected data
        # fig = epochs_clean_plain.average('all').plot(**plot_kwargs)
        # fig.set_size_inches(6, 6)

# create epochs with the evoked subtracted out
        epochs_sub = epochs.copy().subtract_evoked()

        # perform regression
        model_sub = EOGRegression(picks='eeg', picks_artifact='eog').fit(epochs_sub)
        # fig = model_sub.plot(vlim=(None, 0.4))
        # fig.set_size_inches(3, 2)

        # apply the regression coefficients to the original epochs
        epochs_clean_sub = model_plain.apply(epochs).apply_baseline()
        eog_epochs = mne.preprocessing.create_eog_epochs(raw)
        # specify that we want to average the EOG channel too
        eog_evoked = eog_epochs.average('all')
        # eog_evoked.plot('all')
        # fig.set_size_inches(6, 6)

        # perform regression on the evoked blink response
        model_evoked = EOGRegression(picks='eeg', picks_artifact='eog').fit(eog_evoked)

        # apply the regression coefficients to the original epochs
        epochs_clean_evoked = model_evoked.apply(epochs).apply_baseline()
        # fig = epochs_clean_evoked.average('all').plot(**plot_kwargs)
        # fig.set_size_inches(6, 6)

# show the effect on the blink evoked
        eog_evoked_clean = model_evoked.apply(eog_evoked)
        eog_evoked_clean.apply_baseline()
        # eog_evoked_clean.plot('all')
        # epochs_clean_evoked.plot_psd(picks='eeg', fmax=90)
        # epochs.save(base_dir + 'processed/' + fname + 'cond_D-epo.fif', overwrite=True)

'''
V2: Change from Original is that I will be using Gratton's method from the paper for 
blink artifactsthis method also calls for epoching data before removing artifacts
V3: Exporting preprocessed data to begin further analysis, 
eliminated lines that aren't currently being used, if needed check V2
V4: New EOG regression, still follows Gratton et al, but looks cleaner.
Added a flats rejection to remove dead channels in epochs
'''