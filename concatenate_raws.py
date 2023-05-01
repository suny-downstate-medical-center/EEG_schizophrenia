'''
Attempting to address the issue by concatenating all raw files from each group
Will then process data as before
'''

import numpy as np
import mne
import glob
import os
conditions = ['Background', 'Target']

base_dir = '/Users/scottmcelroy/smm_code/A1_scz/A1_raw_data/cond_A/'
data_files = glob.glob(base_dir + '*.bdf')

raws = {}

for idx, c in enumerate(conditions):
    raws[c] = [mne.io.read_raw_bdf(d)[idx] for d in data_files]