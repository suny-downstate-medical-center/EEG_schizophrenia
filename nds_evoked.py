import numpy as np
import mne
import os

base_dir = '/Users/scottmcelroy/smm_code/A1_scz/A1_raw_data/cond_A/'
data = 'processed'
data_dir = base_dir + data
for file in os.listdir(data_dir):
    if file.endswith('.fif'):
        epochs = mne.read_epochs(os.path.join(data_dir, file))
        fname = file[0:5]

        conditions = ['Background', 'Target']

        evokeds = {c: epochs[c].average() for c in conditions}

        times = [.150, .250, .400, .600, .800]
        #for c in evokeds.keys():
        #    evokeds[c].plot_joint(times=times, title=c);
        mne.viz.plot_compare_evokeds(evokeds, picks="Fz", combine='mean');

        roi = ['Pz', 'P5', 'P6', 'Cz', 'C4', 'C3']

        color_dict = {'Background': 'blue', 'Target': 'red'}
        linestyle_dict = {'Background': '-', 'Target': '--'}

        # epochs['Target'].plot_image(picks=roi, combine='mean', evoked=True)
    #    epochs.average('eeg').plot(picks=roi)
    #    epochs['Background'].plot_psd(picks=roi, fmax=60, fmin=35)
    #    fig = evokeds.plot_psd(fmax=100)
    #    fig.savefig(base_dir + 'psd_figs_ica/' + fname + 'psd')

    #    mne.viz.plot_compare_evokeds(evokeds, combine='mean',
    #                                legend='lower right',
    #                                picks=roi, show_sensors='upper right',
    #                                colors=color_dict,
    #                                linestyles=linestyle_dict);
        #mne.viz.plot_dipole_amplitudes(epochs)
#        epochs.pick_types(eeg=True, eog=False)
#        epochs_full = epochs.copy()
#        epochs.crop(0.07, 0.08)
#        dip = mne.fit_dipole(epochs)[0]
        evokeds_diff = mne.combine_evoked([evokeds['Target'], evokeds['Background']],
                                          weights=[1, -1])

        evokeds_diff
        mne.viz.plot_compare_evokeds({'Mismatch-Match': evokeds_diff},
                                     picks=['Cz'], show_sensors='upper right',
                                     combine='mean',
                                     title='Difference Wave');
        evokeds['Background'].comment
        evokeds['Target'].comment
        for condition in evokeds.keys():
            evokeds[condition].comment = condition

        evokeds
        mne.write_evokeds('/Users/scottmcelroy/smm_code/A1_scz/A1_raw_data/grp_A/' + fname + 'cond_D-ave.fif',
                          list(evokeds.values()))