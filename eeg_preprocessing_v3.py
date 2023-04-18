import numpy as np
import mne
from mne.preprocessing import EOGRegression
import os

base_dir = '/Users/scottmcelroy/smm_code/A1_scz/A1_raw_data/cond_D/'
for file in os.listdir(base_dir):
    if file.endswith('.bdf'):
        raw = mne.io.read_raw_bdf(os.path.join(base_dir, file))
        fname = file[0:5]
        raw.load_data()
# maybe use
        reject_criteria = dict(eeg=100e-6)
        raw.set_channel_types({'HEO1': 'eog', 'HEO2': 'eog', 'VEO1': 'eog', 'VEO2': 'eog', 'NOSE': 'misc', 'M1': 'misc',
                               'M2': 'misc', 'EXG8': 'misc'})
        raw.set_eeg_reference(['NOSE'])
#        raw.info['bads'].append('CP4')
# Set EEG Montage for Electrode Locations

        std_montage = mne.channels.make_standard_montage('biosemi64')
        raw = raw.set_montage(std_montage, on_missing='warn')

        n_time_samps = raw.n_times
        time_secs = raw.times
        ch_names = raw.ch_names
        n_chan = len(ch_names)

# Bandpass and notch filtering data
        filt = raw.copy().filter(1, 100)
        filtered = filt.notch_filter(60)
        # filtered.plot_psd(fmax=100)
        #filtered.plot_psd(fmax=100)

        events = mne.find_events(filtered)
        event_ids = {'Background': 4, 'Target': 200}

        epochs = mne.Epochs(filtered, events, event_id=event_ids, tmin=-0.2, tmax=1.0, preload=True,
                            reject=reject_criteria)

        model_plain = EOGRegression(picks='eeg', picks_artifact='eog').fit(epochs)
# create epochs with the evoked subtracted out
        epochs_sub = epochs.copy().subtract_evoked()

# perform regression
        model_sub = EOGRegression(picks='eeg', picks_artifact='eog').fit(epochs_sub)

# apply the regression coefficients to the original epochs
        epochs_clean_sub = model_plain.apply(epochs).apply_baseline(baseline = (None, 0))
        #epochs_clean_sub.plot(title = str(fname))
        order = np.concatenate([mne.pick_types(raw.info, eog=True), mne.pick_types(raw.info, eeg=True)])

        # epochs_clean_sub = epochs_clean_sub.decimate(60)
# plot original data
        raw_kwargs = dict(events=events, order=order, start=13, duration=3, n_channels=10,
                          scalings=dict(eeg=50e-6, eog=250e-6))
        # raw.plot(**raw_kwargs)
# regress (using coefficients computed previously) and plot
        raw_clean = model_sub.apply(raw)
        # raw_clean.plot(**raw_kwargs)
# raw.plot_psd(picks=['FCz'], fmax=100)
        bkgd_epochs = epochs_clean_sub['Background']
        # bkgd_epochs.plot_psd()
        # bkgd_epochs.plot_image(picks=['Cz', 'C4', 'C3', 'Pz', 'P5', 'P6'])
        #bkgd_epochs.plot_image(picks=['Cz'])
        epochs_clean_sub.save(base_dir + 'processed/' + fname + 'cond_D-epo.fif', overwrite=True)



'''
V2: Change from Original is that I will be using Gratton's method from the paper for 
blink artifactsthis method also calls for epoching data before removing artifacts
V3: Exporting preprocessed data to begin further analysis, 
eliminated lines that aren't currently being used, if needed check V2
'''
