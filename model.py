import wave
import contextlib
import numpy as np
from tkinter import filedialog as fd
from matplotlib.figure import Figure
from os import path
from pydub import AudioSegment
from scipy.io import wavfile
from scipy.signal import welch

#Model class to handle all calculations
class Model:
    def __init__(self):
        self.gfile = ' '
        self.filename=' '
        self.dura = ' '
        self.power=[]
        self.duration = 0
        self.fig = 0
        self.low_indices =0
        self.frequencies= []

    #function to convert a audio file to a single channel
    def to_single_channel(self):
        raw_audio = AudioSegment.from_file(self.gfile, format="wav")
        channel_count = raw_audio.channels
        mono_wav = raw_audio.set_channels(1)
        mono_wav.export(self.gfile, format="wav")

    #function to convert audio files to .wav
    def convert_to_wav(self, filename):
        main, extension = path.splitext(filename)
        if extension != ".wav":
            extension = ".wav"
            sound = AudioSegment.from_file(filename)
            sound.export(main + extension, format="wav")
            self.gfile = main + extension
        else:
            self.gfile = filename
        print(self.gfile)
        self.to_single_channel()

    #function to select a file
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

    #function to calculate the length of the audio file
    def show_time(self):
        #finds and prints time of sound
        with contextlib.closing(wave.open(self.gfile, 'r')) as f:
            numch = f.getnchannels()
            frames = f.getnframes()
            rate = f.getframerate()
            self.duration = frames / float(rate)
            self.dura = str(self.duration)

    #function to calculate the rt60 of varying frequency bands
    def compute_rt60(self, frequencies, power, band):
        if band == 'low':
            freq_band = (20, 200)
        elif band == 'mid':
            freq_band = (200, 2000)
        elif band == 'high':
            freq_band = (2000, 20000)
        elif band == 'all':
            freq_band = (20, 20000)

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

    #function to calculate the dominant frequency and the power of the different frequency bands
    def freq_calc(self):
        # finds frequencies
        sample_rate, data = wavfile.read(self.gfile)
        frequencies, power = welch(data, sample_rate, nperseg=4096)
        self.dominant_frequency = frequencies[np.argmax(power)]
        print(f'Dominant frequency is {round(self.dominant_frequency)}Hz')

        # Compute frequency bands
        low_freq_band = (20, 200)
        mid_freq_band = (200, 2000)
        high_freq_band = (2000, 20000)

        low_indices = np.where((frequencies >= 20) & (frequencies <= 200))
        mid_indices = np.where((frequencies >= 200) & (frequencies <= 2000))
        high_indices = np.where((frequencies >= 2000) & (frequencies <= 20000))
        all_indices = np.where((frequencies >=20) & (frequencies <= 20000))

        self.low_power = np.sum(power[low_indices])
        self.mid_power = np.sum(power[mid_indices])
        self.high_power = np.sum(power[high_indices])
        self.all_power = np.sum(power[all_indices])

        # Plot the waveform
        self.fig_waveform = Figure(figsize=(7, 4), dpi=100)
        plt_waveform = self.fig_waveform.add_subplot(111)
        time_waveform = np.linspace(0., self.duration, data.shape[0])
        plt_waveform.plot(time_waveform, data[:], label="Left channel")
        plt_waveform.legend()
        plt_waveform.set_xlabel('Time (s)')
        plt_waveform.set_ylabel('Amplitude')
        plt_waveform.margins(0.1, 0.1)  # Add padding

        # Plot the RT60 for low frequency
        rt60_low = self.compute_rt60(frequencies[low_indices], power[low_indices], 'low')
        self.fig_low = Figure(figsize=(5, 4), dpi=100)
        plt_low = self.fig_low.add_subplot(111)
        plt_low.axvline(x=rt60_low, color='red', linestyle='--', label='RT60')
        plt_low.plot(frequencies[low_indices], power[low_indices])
        plt_low.set_title('Low Frequency Band')
        plt_low.set_xlabel('Frequency (Hz)')
        plt_low.set_ylabel('Power Spectral Density')
        plt_low.margins(0.1, 0.1)  # Add padding

        # Plot the RT60 for mid frequency
        rt60_mid = self.compute_rt60(frequencies[mid_indices], power[mid_indices], 'mid')
        self.fig_mid = Figure(figsize=(7, 4), dpi=100)
        plt_mid = self.fig_mid.add_subplot(111)
        plt_mid.axvline(x=rt60_mid, color='red', linestyle='--', label='RT60')
        plt_mid.plot(frequencies[mid_indices], power[mid_indices])
        plt_mid.set_title('Mid Frequency Band')
        plt_mid.set_xlabel('Frequency (Hz)')
        plt_mid.set_ylabel('Power Spectral Density')
        plt_mid.margins(0.1, 0.1)  # Add padding

        # Plot the RT60 for high frequency
        rt60_high = self.compute_rt60(frequencies[high_indices], power[high_indices], 'high')
        self.fig_high = Figure(figsize=(6, 4), dpi=100)
        plt_high = self.fig_high.add_subplot(111)
        plt_high.axvline(x=rt60_high, color='red', linestyle='--', label='RT60')
        plt_high.plot(frequencies[high_indices], power[high_indices])
        plt_high.set_title('High Frequency Band')
        plt_high.set_xlabel('Frequency (Hz)')
        plt_high.set_ylabel('Power Spectral Density')
        plt_high.margins(0.1, 0.1)  # Add padding

        # Plot the RT60 for high frequency
        rt60_all = self.compute_rt60(frequencies[all_indices], power[all_indices], 'all')
        self.fig_all = Figure(figsize=(7, 4), dpi=100)
        plt_all = self.fig_all.add_subplot(111)
        plt_all.axvline(x=rt60_all, color='red', linestyle='--', label='RT60')
        plt_all.plot(frequencies[all_indices], power[all_indices])
        plt_all.set_title('All Frequency Bands')
        plt_all.set_xlabel('Frequency (Hz)')
        plt_all.set_ylabel('Power Spectral Density')
        plt_all.margins(0.1, 0.1)  # Add padding