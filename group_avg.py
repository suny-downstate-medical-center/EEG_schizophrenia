# TODO - Evaluate value error


import numpy as np
import mne
import glob
import os
conditions = ['Background', 'Target']

base_dir = '/Users/scottmcelroy/smm_code/A1_scz/A1_raw_data/grp_D/'
data_files = glob.glob(base_dir + '*.fif')

evokeds = {}

for idx, c in enumerate(conditions):
    evokeds[c] = [mne.read_evokeds(d)[idx] for d in data_files]

evokeds
ave = mne.grand_average(evokeds['Background'], ['Target'])
evokeds_diff = mne.combine_evoked([evokeds['Target'], evokeds['Background']],
                                          weights=[1, -1])
# thc_epochs = {}
# Define plot parameters
roi = ['Cz']

color_dict = {'Control':'blue', 'Violation':'red'}
linestyle_dict = {'Control':'-', 'Violation':'--'}


mne.viz.plot_compare_evokeds(ave,
                             combine='mean',
                             legend='lower right',
                             picks=roi, show_sensors='upper right',
                             colors=color_dict,
                             linestyles=linestyle_dict,
                             title='Violation vs. Control Waveforms'
                            )



#for idx, c in enumerate(conditions):
#  thc_epochs[c] = [mne.read_epochs(d) for d in data_files]
#thc_bkgd = []

# Avg PSDs
#for i in thc_epochs:
#    for x in i.events:
#        thc_bkgd = np.append(thc_bkgd, x)










'''
epochs = mne.read_epochs('/Users/scottmcelroy/Desktop/thc_iom/processed/TI008thc_iom-epo.fif')
epoch_cov = mne.compute_covariance(epochs)
mne.bem.make_bem_model(subject='TI008')
mne.fit_dipole(epochs, epoch_cov)
'''