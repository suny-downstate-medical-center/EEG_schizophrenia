import numpy as np
import mne
from mne.preprocessing import EOGRegression
import os

base_dir = '/Users/scottmcelroy/Desktop/cond_D/'
for file in os.listdir(base_dir):
    if file.endswith('.bdf'):
        raw = mne.io.read_raw_bdf(os.path.join(base_dir, file))
        fname = file[0:5]
        raw.load_data()
        raw.set_channel_types({'HEO1': 'eog', 'HEO2': 'eog', 'VEO1': 'eog', 'VEO2': 'eog', 'NOSE': 'misc', 'M1': 'misc',
                               'M2': 'misc', 'EXG8': 'misc'})
        std_montage = mne.channels.make_standard_montage('biosemi64')
        raw = raw.set_montage(std_montage, on_missing='warn')

        n_time_samps = raw.n_times
        time_secs = raw.times
        ch_names = raw.ch_names
        n_chan = len(ch_names)

        # Bandpass and notch filtering data
        filt = raw.copy().filter(0.1, 100)
        filtered = filt.notch_filter(60)
        tstep = 1.0
        events_ica = mne.make_fixed_length_events(filtered, duration=tstep)
        epochs_ica = mne.Epochs(filtered, events_ica,
                                tmin=0.0, tmax=tstep,
                                baseline=None,
                                preload=True)
        from autoreject import get_rejection_threshold

        reject = get_rejection_threshold(epochs_ica);
        reject
        random_state = 42  # ensures ICA is reproducable each time it's run
        ica_n_components = .99  # Specify n_components as a decimal to set % explained variance

        # Fit ICA
        ica = mne.preprocessing.ICA(n_components=ica_n_components,
                                    random_state=random_state,
                                    )
        ica.fit(epochs_ica,
                reject=reject,
                tstep=tstep)
        ica_z_thresh = 1.96
        eog_indices, eog_scores = ica.find_bads_eog(filtered,
                                                    threshold=ica_z_thresh)
        ica.exclude = eog_indices

        ica.plot_scores(eog_scores);
        events = mne.find_events(raw)
        event_ids = {'Background': 4, 'Target': 200}
        epochs = mne.Epochs(filtered, events, event_id=event_ids, tmin=-0.1, tmax=1.0, preload=True,
                            )
        epochs.average().plot(spatial_colors=True);
        epochs_postica = ica.apply(epochs.copy())
        epochs_postica.average().plot(spatial_colors=True);
        epochs_postica.save(base_dir + 'filtered/' + fname + 'cond_D-epo.fif', overwrite=True)