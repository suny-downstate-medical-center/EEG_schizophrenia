import mne
import pickle

class load_file:

    def raw_bdf(path):
        raw = mne.io.read_raw_bdf(path, preload=True)
        raw.set_channel_types({'HEO1': 'eog', 'HEO2': 'eog', 'VEO1': 'eog', 'VEO2': 'eog',
                               'M1': 'misc', 'M2': 'misc', 'EXG8': 'misc'})
        raw.set_eeg_reference(['NOSE'])
        return raw

    def eLab_epochs(path):
        epochs = mne.read_epochs_eeglab(path)

        return epochs

    def sim_pkl(path):
        file = open(path, 'rb')
        data = pickle.load(file)
        return data

class evoked:

    def make_evoked(epochs):
        evokeds = {}
        conditions = ['standard', 'deviant']
        evokeds = {c: epochs[c].average() for c in conditions}
        return evokeds

    def plot_erp(evokeds):
        mne.viz.plot_compare_evokeds(evokeds, picks="Fz", combine='mean')