from scipy.signal import butter, filtfilt
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import neo
import mne
from mne import io, read_proj, read_selection
from mne.datasets import sample
from mne.time_frequency import psd_multitaper
import mne

print(__doc__)



sfreq = 250
tsample = 1 / sfreq
f_low = 50
f_high = 1
order = 2
channel_vector = [1,2, 3, 4, 5]
data = []
ch_types = []
ch_names = []
n_ch = len(channel_vector)

df = pd.read_csv("/home/runge/openbci/application.linux64/application.linux64/OpenBCI-RAW-right_strait_up_new.txt")
df = df[channel_vector].dropna(axis=0)

# Set parameters
data_path = sample.data_path()
raw_fname = data_path + '/MEG/sample/sample_audvis_raw.fif'
proj_fname = data_path + '/MEG/sample/sample_audvis_eog-proj.fif'


for i in range(0,n_ch):
    data.append(df.ix[:,i])
    ch_types.append('mag')
    ch_names.append(df.ix[:,i].name)

info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
raw = mne.io.RawArray(data, info)
scalings = 'auto'

# Add SSP projection vectors to reduce EOG and ECG artifacts
# projs = read_proj(proj_fname)
# raw.add_proj(projs, remove_existing=True)

# raw.plot(n_channels=n_ch, scalings=scalings, title='MEG data visualization over time', show=True, block=True)

fmin, fmax = 2, 300
tmin, tmax = 0, 130
n_fft = 64

# Let's first check out all channel types
# raw.plot_psd(area_mode='range', tmax=10.0, show=False)

picks = mne.pick_types(raw.info, meg='mag', eeg=False, eog=False,
                       stim=False)
picks = picks[:1]


f, ax = plt.subplots()
psds, freqs = psd_multitaper(raw, low_bias=True, tmin=tmin, tmax=tmax,
                             fmin=fmin, fmax=fmax, proj=True, picks=picks,
                             n_jobs=1)
psds = 10 * np.log10(psds)
psds_mean = psds.mean(0)
psds_std = psds.std(0)

ax.plot(freqs, psds_mean, color='k')
ax.fill_between(freqs, psds_mean - psds_std, psds_mean + psds_std,
                color='k', alpha=.5)
ax.set(title='Multitaper PSD', xlabel='Frequency',
       ylabel='Power Spectral Density (dB)')
plt.show()

# EpochsArray
# event_id = 1
# events = np.array([[200, 0, event_id],
#                    [1200, 0, event_id],
#                    [2000, 0, event_id]])
# epochs_data = np.array([[data[0][:700], data[1][:700]],
#                         [data[0][1000:1700], data[1][1000:1700]],
#                         [data[0][1800:2500], data[1][1800:2500]]])
#
# epochs = mne.EpochsArray(epochs_data, info=info, events=events,
#                          event_id={'arbitrary': 1})
# picks = mne.pick_types(info, meg=True, eeg=False, misc=False)
# epochs.plot(picks=picks, scalings='auto', show=True, block=True)

# ###############################################################################
# # EvokedArray
#
# nave = len(epochs_data)  # Number of averaged epochs
# evoked_data = np.mean(epochs_data, axis=0)
#
# evokeds = mne.EvokedArray(evoked_data, info=info, tmin=-0.2,
#                           comment='Arbitrary', nave=nave)
# evokeds.plot(picks=picks, show=True, units={'mag': '-'},
#              titles={'mag': 'sin and cos averaged'})
#
# ###############################################################################
# # Create epochs by windowing the raw data.
#
# # The events are spaced evenly every 1 second.
# duration = 1.
#
# # create a fixed size events array
# # start=0 and stop=None by default
# events = mne.make_fixed_length_events(raw, event_id, duration=duration)
# print(events)
#
# # for fixed size events no start time before and after event
# tmin = 0.
# tmax = 0.99  # inclusive tmax, 1 second epochs
#
# # create :class:`Epochs <mne.Epochs>` object
# epochs = mne.Epochs(raw, events=events, event_id=event_id, tmin=tmin,
#                     tmax=tmax, baseline=None, verbose=True)
# epochs.plot(scalings='auto', block=True)
#
# ###############################################################################
# # Create overlapping epochs using :func:`mne.make_fixed_length_events` (50 %
# # overlap). This also roughly doubles the amount of events compared to the
# # previous event list.
#
# duration = 0.5
# events = mne.make_fixed_length_events(raw, event_id, duration=duration)
# print(events)
# epochs = mne.Epochs(raw, events=events, tmin=tmin, tmax=tmax, baseline=None,
#                     verbose=True)
# epochs.plot(scalings='auto', block=True)
#
# ###############################################################################
# # Extracting data from NEO file
#
# # The example here uses the ExampleIO object for creating fake data.
# # For actual data and different file formats, consult the NEO documentation.
# reader = neo.io.ExampleIO('fakedata.nof')
# bl = reader.read(cascade=True, lazy=False)[0]
#
# # Get data from first (and only) segment
# seg = bl.segments[0]
# title = seg.file_origin
#
# ch_names = list()
# data = list()
# for asig in seg.analogsignals:
#     # Since the data does not contain channel names, channel indices are used.
#     ch_names.append(str(asig.channel_index))
#     asig = asig.rescale('V').magnitude
#     data.append(asig)
#
# sfreq = int(seg.analogsignals[0].sampling_rate.magnitude)
#
# # By default, the channel types are assumed to be 'misc'.
# info = mne.create_info(ch_names=ch_names, sfreq=sfreq)
#
# raw = mne.io.RawArray(data, info)
# raw.plot(n_channels=4, scalings={'misc': 1}, title='Data from NEO',
#          show=True, block=True, clipping='clamp')
