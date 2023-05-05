# EEG_schizophrenia
This repo conotains scripts to analyze raw eeg files (.bdf) and output epochs, evoked objects, and group grand averages. 


eeg_preprocessing_v4 loads raw files and filters (bandpass, notch) and removes EOG blink artifacts via regression

nds_pipeline_test is an alternate preprocessing pipeline which has the same filters but removes artifacts vie independent component analysis

nds_evoked creates evoked files and can produce plots of evoked data by condition or epoch

group_avg takes evoked data and grand averages by condition (standard and deviant tones) to produce a group average psd plot

grp_A folders contain a subset of the data this repo was created to analyze
