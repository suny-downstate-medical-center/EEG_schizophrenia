'''
Attempting to address the issue by concatenating all raw files from each group
Will then process data as before
'''

import numpy as np
import mne
import glob
import os
conditions = ['Background', 'Target']

base_dir = '/Users/scottmcelroy/smm_code/A1_scz/A1_raw_data/cond_D/'
for file in os.listdir(base_dir):
    if file.endswith('.bdf'):
        raw = mne.io.read_raw_bdf(os.path.join(base_dir, file))
        fname = file[0:5]
        raw.load_data()
