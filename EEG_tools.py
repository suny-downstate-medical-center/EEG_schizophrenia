import mne
import pickle

class load_file:

    # simple class using load functions for the three file types I use for analysis
    def raw_bdf(path):
        raw = mne.io.read_raw_bdf(path, preload=True)
        raw.set_channel_types({'HEO1': 'eog', 'HEO2': 'eog', 'VEO1': 'eog', 'VEO2': 'eog',
                               'M1': 'misc', 'M2': 'misc', 'EXG8': 'misc'})
        raw.set_eeg_reference(['NOSE'])

        return raw

    def eLab_epochs(path):
        epochs = mne.read_epochs_eeglab(path)
        epochs.event_id['Deviant'] = epochs.event_id['200/condition 8']
        del epochs.event_id['200/condition 8']
        epochs.event_id['Standard'] = epochs.event_id['condition 4']
        del epochs.event_id['condition 4']

        return epochs

    def sim_pkl(path):
        file = open(path)
        data = pickle.load(file)

        return data
class processing:
    def epoch_bandpass(epochs, min, max):
        filtered = epochs.filter(l_freq = min, h_freq = max)

        return filtered

class evoked:

    def make_evoked(epochs):
        evokeds = {}
        conditions = ['Standard', 'Deviant']
        evokeds = {c: epochs[c].average() for c in conditions}

        return evokeds

    def plot_erp(evokeds, picks = ['Cz']):
        fig = mne.viz.plot_compare_evokeds(evokeds, picks=picks, combine='mean')

        return fig

    def plot_difference(evokeds, picks=['Cz']):
        evokeds_diff = mne.combine_evoked([evokeds['Deviant'], evokeds['Standard']],
                                          weights=[1, -1])

        mne.viz.plot_compare_evokeds({'Mismatch-Match': evokeds_diff},
                                     picks=picks, show_sensors='upper right',
                                     combine='mean',
                                     title='Difference Wave',
                                     );

class group_analysis:


    def MMN_epochs(folder_dir):

        import glob
        conditions = ['Standard', 'Deviant']

        data_files = glob.glob(folder_dir + '*.set')
        print(data_files)

        # empty dict to fill with each subject's evoked
        evoked_dict = {}

        # i is index, d is the file
        for i,d in enumerate(data_files):

            # load each file in data_files
            epochs = load_file.eLab_epochs(d)

            # create dict with index and the evoked file,
            # within evoked is Standard and Deviant
            evoked_dict.update({i: evoked.make_evoked(epochs)})
            print(evoked_dict[i].keys())

        # Create final evoked dicts -
        # first layer is conditions, second layer is subjects
        evokeds = {}
        for idx, c in enumerate(conditions):
            # c is the condition idx is the index of conditions list
            evokeds.update({c: [evoked_dict[i][c] for i in evoked_dict.keys()]})

        print(evokeds['Standard'])

        # ave_std = mne.grand_average(evokeds['condition 4'])
        # ave_dev = mne.grand_average(evokeds['200/condition 8'])


