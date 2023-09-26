'''
Loads EEG epoch data, and breaks down into evoked object (background and target tones)
Plots average Target and Background evoked for each file and the difference waveform
Saves evoked data

# TODO nds_evoked.py creates .fif files with different sizes which breaks group_avg.py
'''

import numpy as np
import mne
import os
mne.set_log_level('error')

base_dir = base_dir = '/Users/scottmcelroy/A1_scz/A1_exp_data/organized_data/40Hz/cond_A/'
data = 'processed/'
data_dir = base_dir + data
evokeds = {}
for file in os.listdir(data_dir):
    if file.endswith('.fif'):
        epochs = mne.read_epochs(os.path.join(data_dir, file))
        epochs = epochs.filter(1, 12)
        fname = file[0:5]
        conditions = ['Background', 'Target']

        evokeds = {c: epochs[c].average() for c in conditions}



        # for c in evokeds.keys():
        #     evokeds[c].plot_joint();

        mne.viz.plot_compare_evokeds(evokeds, picks="Cz", combine='mean');
        
    
        roi = ['Pz', 'P5', 'P6', 'Cz', 'C4', 'C3']
        
        color_dict = {'Background': 'blue', 'Target': 'red'}
        linestyle_dict = {'Standard': '-', 'Deviant': '--'}

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


        mne.write_evokeds('/Users/scottmcelroy/A1_scz/A1_exp_data/organized_data/mne_evoked/cond_A/' + fname + 'cond_A-ave.fif',
                           list(evokeds.values()))
