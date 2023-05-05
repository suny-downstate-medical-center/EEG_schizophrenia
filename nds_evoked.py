'''
Loads EEG epoch data, and breaks down into evoked object (background and target tones)
Plots average Target and Background evoked for each file and the difference waveform
Saves evoked data
'''

import numpy as np
import mne
import os

base_dir = base_dir = '/Users/scottmcelroy/smm_code/A1_scz/A1_raw_data/organized_data/cond_D/'
data = 'processed/'
data_dir = base_dir + data
for file in os.listdir(data_dir):
    if file.endswith('.fif'):
        epochs = mne.read_epochs(os.path.join(data_dir, file))
        fname = file[0:5]

        conditions = ['Background', 'Target']

        evokeds = {c: epochs[c].average() for c in conditions}

        times = [.150, .250, .400]
        # for c in evokeds.keys():
        #     evokeds[c].plot_joint();
        mne.viz.plot_compare_evokeds(evokeds, picks="Fz", combine='mean');

        roi = ['Pz', 'P5', 'P6', 'Cz', 'C4', 'C3']

        color_dict = {'Background': 'blue', 'Target': 'red'}
        linestyle_dict = {'Background': '-', 'Target': '--'}

        evokeds_diff = mne.combine_evoked([evokeds['Target'], evokeds['Background']],
                                          weights=[1, -1])

        evokeds_diff
        # mne.viz.plot_compare_evokeds({'Mismatch-Match': evokeds_diff},
        #                              picks=['Cz'], show_sensors='upper right',
        #                             combine='mean',
        #                             title='Difference Wave');
        evokeds['Background'].comment
        evokeds['Target'].comment
        for condition in evokeds.keys():
            evokeds[condition].comment = condition

        mne.write_evokeds('/Users/scottmcelroy/smm_code/A1_scz/A1_raw_data/organized_data/test/' + fname + 'cond_D-ave.fif',
                           list(evokeds.values()))