from __future__ import print_function
import Queue
import json
import socket
import sys
import threading
import tensorflow as tf
import pandas as pd
from scipy.signal import butter, filtfilt

import librosa
import numpy as np

from processor import Clip
from ssa import SingularSpectrumAnalysis


class PreProcessor(threading.Thread):
    def __init__(self, thread_id, input_buffer, output_buffer, config):
        threading.Thread.__init__(self)
        self.isRun = True
        self.config = config
        self.thread_id = thread_id
        self.lock = threading.Lock()
        self.input_buffer = input_buffer
        self.output_buffer = output_buffer
        self.window_size = int(config["window_size"])
        self.sampling_rate = int(config["sampling_rate"])
        self.low_frequency = int(config["low_frequency"])
        self.high_frequency = int(config["high_frequency"])
        self.order = int(config["order"])
        self.train_dir = str(config["train_dir_abs_location"])
        self.number_of_channels = int(config["number_of_channels"])
        self.sampling_time = 1.0 / self.sampling_rate * 1.0

    def run(self):
        self.processor(self.thread_id)

    def nomalize_signal(self, input_signal):
        mean = np.mean(input_signal, axis=0)
        input_signal -= mean
        return input_signal / np.std(input_signal, axis=0)

    def processor(self, thread_id):
        noise_signal = self.input_buffer[thread_id]
        with open(self.train_dir + "/"+str(thread_id)+"noise_signal.csv", 'a') as f:
                np.savetxt(f, noise_signal, delimiter=',', fmt='%.18e')
        noise_reduced_signal = self.apply_noise_reducer_filer(noise_signal)
        noise_reduced_signal = self.nomalize_signal(noise_reduced_signal)
        with open(self.train_dir + "/"+str(thread_id)+"noise_reduced_signal.csv", 'a') as f:
                np.savetxt(f, noise_reduced_signal, delimiter=',', fmt='%.18e')

        reconstructed_signal = SingularSpectrumAnalysis(noise_reduced_signal, int(np.ceil(self.window_size/8))).execute()
        with open(self.train_dir + "/fr"
                                   "" + str(thread_id) + "reconstructed_signal.csv", 'a') as f:
            np.savetxt(f, reconstructed_signal, delimiter=',', fmt='%.18e')
        clip = Clip(self.config, buffer=reconstructed_signal)
        reconstructed_signal = clip.get_feature_vector()
        with open(self.train_dir + "/" + str(thread_id) + "feature_vector.csv", 'a') as f:
            np.savetxt(f, reconstructed_signal, delimiter=',', fmt='%.18e')
        self.lock.acquire()
        self.output_buffer[thread_id] = reconstructed_signal
        self.lock.release()

    def apply_noise_reducer_filer(self, data):

        b, a = butter(self.order, (self.order * self.low_frequency * 1.0)
                      / self.sampling_rate * 1.0, btype='low')
        for i in range(0, self.number_of_channels):
            data = np.transpose(filtfilt(b, a, data))

        b1, a1 = butter(self.order, (self.order * self.high_frequency * 1.0) /
                        self.sampling_rate * 1.0, btype='high')
        for i in range(0, self.number_of_channels):
            data = np.transpose(filtfilt(b1, a1, data))

        Wn = (np.array([58.0, 62.0]) / 500 * self.order).tolist()
        b3, a3 = butter(self.order, Wn, btype='stop')
        for i in range(0, self.number_of_channels):
            data = np.transpose(filtfilt(b3, a3, data))

        return data

# df2 = pd.read_csv("/home/runge/openbci/git/OpenBCI_Python/build/dataset/3noise_reduced_signal.csv")
# df2 = df2.dropna(axis=0)
# noise_reduced_signal = df2.ix[:,0]
# window_size = 128
# number_of_windows = int(np.ceil(len(noise_reduced_signal)/window_size))
# for j in range(0,number_of_windows-1):
#     reconstructed_signal = SingularSpectrumAnalysis(noise_reduced_signal[j*window_size:(j+1)*window_size], int(np.ceil(window_size / 16))).execute(1)
#     with open("/home/runge/openbci/git/OpenBCI_Python/build/dataset/reconstructed_mod.csv", 'a') as f:
#         np.savetxt(f, reconstructed_signal, delimiter=',', fmt='%.18e')


