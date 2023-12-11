
import wave
import contextlib
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from os import path
from pydub import utils, AudioSegment
from pydub.playback import play
from scipy.io import wavfile
from scipy.signal import welch

class Model:
    def __init__(self):
        self.gfile = ' '
        self.filename=' '
        self.dura = ' '
        self.dominant_frequency = 0
        self.frequencies = 0
        self.power=0
        self.low_power = 0
        self.mid_power = 0
        self.high_power = 0
        self.duration = 0
        self.data = 0
        self.fig = 0
        self.low_indices =0
    def to_single_channel(self):
        raw_audio = AudioSegment.from_file(self.gfile, format="wav")
        channel_count = raw_audio.channels
        mono_wav = raw_audio.set_channels(1)
        mono_wav.export(self.gfile, format="wav")
    def convert_to_wav(self, filename):
        main, extension = path.splitext(filename)
        if extension != ".wav":
            extension = ".wav"
            sound = AudioSegment.from_file(filename)
            sound.export(main + extension, format="wav")
            self.gfile = main + extension
        else:
            self.gfile = filename
        self.to_single_channel()
    def select_file(self):
        self.filetypes = (
            ('Audio files', ".wav"),
            ('Audio files' , ".m4a"),
            ('Audio files', ".mp3"),
            ('All files', '*.*')
        )
        self.filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=self.filetypes)
        self.convert_to_wav(self.filename)

    def show_time(self):
        try:
            #finds and prints time of sound
            with contextlib.closing(wave.open(self.gfile, 'r')) as f:
                numch = f.getnchannels()
                frames = f.getnframes()
                rate = f.getframerate()
                self.duration = frames / float(rate)
                self.dura = str(self.duration)
        except:
            showinfo(
                title='Filetype not supported',
                message='Please select a supported audio file type.'
            )


    def dom_freq(self):
        #finds frequencies
        sample_rate, self.data = wavfile.read(self.gfile)
        self.frequencies, self.power = welch(self.data, sample_rate, nperseg=4096)
        self.dominant_frequency = self.frequencies[np.argmax(self.power)]

    def freq_calc(self):
        # Compute frequency bands
        low_freq_band = (20, 200)
        mid_freq_band = (200, 2000)
        high_freq_band = (2000, 20000)

        self.low_power = np.sum(self.power[(self.frequencies >= low_freq_band[0]) & (self.frequencies <= low_freq_band[1])])
        self.mid_power = np.sum(self.power[(self.frequencies >= mid_freq_band[0]) & (self.frequencies <= mid_freq_band[1])])
        self.high_power = np.sum(self.power[(self.frequencies >= high_freq_band[0]) & (self.frequencies <= high_freq_band[1])])

    def compute_rt60(frequencies, power, band):
        if band == 'low':
            freq_band = (20, 200)
        elif band == 'mid':
            freq_band = (200, 2000)
        elif band == 'high':
            freq_band = (2000, 20000)

        indices = np.where((frequencies >= freq_band[0]) & (frequencies <= freq_band[1]))
        band_power = power[indices]
        threshold_power = band_power.max() - 60  # 60 dB below the peak

        # Find the time it takes for the power to decay to the threshold
        decay_indices = np.where(band_power <= threshold_power)[0]
        if len(decay_indices) > 1:
            rt60_index = decay_indices[0]
            return frequencies[rt60_index]
        else:
            return None
    def plot_waveform(self):
        # Plot the waveform
        self.fig = Figure(figsize=(3, 4), dpi=100)
        plt = self.fig.add_subplot(111)
        time = np.linspace(0., self.duration, self.data.shape[0])
        plt.plot(time, self.data[:], label="Left channel")
        plt.legend()
        plt.set_xlabel('Time (s)')
        plt.set_ylabel('Amplitude')
        plt.margins(0.1)  # Add padding
        """rt60_low = self.compute_rt60(self.frequencies[self.low_indices], self.power[self.low_indices], 'low')
        self.fig_low = Figure(figsize=(4, 3), dpi=100)
        plt_low = self.fig_low.add_subplot(111)
        plt_low.axvline(x=rt60_low, color='red', linestyle='--', label='RT60')
        plt_low.plot(self.frequencies[self.low_indices], self.power[self.low_indices])
        plt_low.set_title('Low Frequency Band')
        plt_low.set_xlabel('Frequency (Hz)')
        plt_low.set_ylabel('Power Spectral Density')
        plt_low.margins(0.1, 0.1)  # Add padding"""



