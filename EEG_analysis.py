import EEG_tools as et
import mne
# Load files from EEGlab analysis
# epochs = et.load_file.eLab_epochs(path='/Users/scottmcelroy/A1_scz/A1_exp_data/organized_data/cond_D/TI008D440A.set')

# Rename epochs
# epochs.event_id['Deviant'] = epochs.event_id['200/condition 8']
# del epochs.event_id['200/condition 8']
# epochs.event_id['Standard'] = epochs.event_id['condition 4']
# del epochs.event_id['condition 4']

# Make evoked object for MNE
# evokeds = et.evoked.make_evoked(epochs)

# Plot ERP wave form for MMN
# et.evoked.plot_erp(evokeds=evokeds, picks=['Cz'])

# Plot MMN subtracted waveform

# et.evoked.plot_difference(evokeds)

ave_std, ave_dev = et.group_analysis.MMN_epochs('/Users/scottmcelroy/A1_scz/A1_exp_data/organized_data/cond_D/')
evokeds_diff = mne.combine_evoked([ave_dev, ave_std],
                                   weights=[1, -1])

mne.viz.plot_compare_evokeds({'Mismatch-Match': evokeds_diff},
                              show_sensors='upper right',
                             combine='mean',
                             title='Difference Wave',
                             );

# evokeds = et.group_analysis.MMN_epochs('/Users/scottmcelroy/A1_scz/A1_exp_data/organized_data/cond_D/')