import tkinter as tk
import wave
import contextlib
import numpy as np
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.io import wavfile
from scipy.signal import welch

gfile = ''
current_frequency_band = 'low'
fig_low, plt_low, canvas_low = None, None, None
fig_mid, plt_mid, canvas_mid = None, None, None
fig_high, plt_high, canvas_high = None, None, None

# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('1200x600')
frame = tk.Frame(root)

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

def select_file():
    global gfile, fig_low, plt_low, canvas_low, fig_mid, plt_mid, canvas_mid, fig_high, plt_high, canvas_high

    filetypes = (
        ('Audio files', ".wav"),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    gfile = filename

    # tkinter.messagebox — Tkinter message prompts
    showinfo(
        title='Selected File',
        message=filename
    )

    # Finds and prints time of sound
    with contextlib.closing(wave.open(gfile, 'r')) as f:
        numch = f.getnchannels()
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        dura = str(duration)
        seconds = Label(root, text=("Time in seconds: " + dura[:4]))
        seconds.place(x=20, y=20)

        # Finds frequencies
        sample_rate, data = wavfile.read(gfile)
        frequencies, power = welch(data, sample_rate, nperseg=4096)
        dominant_frequency = frequencies[np.argmax(power)]
        print(f'Dominant frequency is {round(dominant_frequency)}Hz')

        # Compute frequency band powers
        low_indices = np.where((frequencies >= 20) & (frequencies <= 200))
        mid_indices = np.where((frequencies >= 200) & (frequencies <= 2000))
        high_indices = np.where((frequencies >= 2000) & (frequencies <= 20000))

        low_power = np.sum(power[low_indices])
        mid_power = np.sum(power[mid_indices])
        high_power = np.sum(power[high_indices])

        # Display frequency band powers
        low_freq_label = Label(root, text=f"Low Frequency Band Power: {low_power}")
        low_freq_label.place(x=20, y=40)

        mid_freq_label = Label(root, text=f"Mid Frequency Band Power: {mid_power}")
        mid_freq_label.place(x=20, y=60)

        high_freq_label = Label(root, text=f"High Frequency Band Power: {high_power}")
        high_freq_label.place(x=20, y=80)

        dominant_freq_label = Label(root, text=f"Dominant Frequency: {round(dominant_frequency)}Hz")
        dominant_freq_label.place(x=20, y=100)

        # Plot the waveform
        fig_waveform = Figure(figsize=(4, 3), dpi=100)
        plt_waveform = fig_waveform.add_subplot(111)
        time_waveform = np.linspace(0., duration, data.shape[0])
        plt_waveform.plot(time_waveform, data[:], label="Left channel")
        plt_waveform.legend()
        plt_waveform.set_xlabel('Time (s)')
        plt_waveform.set_ylabel('Amplitude')
        plt_waveform.margins(0.1, 0.1)  # Add padding
        canvas_waveform = FigureCanvasTkAgg(fig_waveform, master=root)
        canvas_waveform.draw()
        canvas_waveform.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Plot the RT60 for low frequency
        rt60_low = compute_rt60(frequencies[low_indices], power[low_indices], 'low')
        fig_low = Figure(figsize=(4, 3), dpi=100)
        plt_low = fig_low.add_subplot(111)
        plt_low.axvline(x=rt60_low, color='red', linestyle='--', label='RT60')
        plt_low.plot(frequencies[low_indices], power[low_indices])
        plt_low.set_title('Low Frequency Band')
        plt_low.set_xlabel('Frequency (Hz)')
        plt_low.set_ylabel('Power Spectral Density')
        plt_low.margins(0.1, 0.1)  # Add padding
        canvas_low = FigureCanvasTkAgg(fig_low, master=root)
        canvas_low.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Plot the RT60 for mid frequency
        rt60_mid = compute_rt60(frequencies[mid_indices], power[mid_indices], 'mid')
        fig_mid = Figure(figsize=(4, 3), dpi=100)
        plt_mid = fig_mid.add_subplot(111)
        plt_mid.axvline(x=rt60_mid, color='red', linestyle='--', label='RT60')
        plt_mid.plot(frequencies[mid_indices], power[mid_indices])
        plt_mid.set_title('Mid Frequency Band')
        plt_mid.set_xlabel('Frequency (Hz)')
        plt_mid.set_ylabel('Power Spectral Density')
        plt_mid.margins(0.1, 0.1)  # Add padding
        canvas_mid = FigureCanvasTkAgg(fig_mid, master=root)

        # Plot the RT60 for high frequency
        rt60_high = compute_rt60(frequencies[high_indices], power[high_indices], 'high')
        fig_high = Figure(figsize=(4, 3), dpi=100)
        plt_high = fig_high.add_subplot(111)
        plt_high.axvline(x=rt60_high, color='red', linestyle='--', label='RT60')
        plt_high.plot(frequencies[high_indices], power[high_indices])
        plt_high.set_title('High Frequency Band')
        plt_high.set_xlabel('Frequency (Hz)')
        plt_high.set_ylabel('Power Spectral Density')
        plt_high.margins(0.1, 0.1)  # Add padding
        canvas_high = FigureCanvasTkAgg(fig_high, master=root)
        canvas_high.get_tk_widget().pack_forget()

        # Switch Frequency Band Button
        switch_button = Button(
            root,
            text='Switch Frequency Band',
            command=switch_frequency_band
        )
        switch_button.pack(side=tk.BOTTOM)

def switch_frequency_band():
    global current_frequency_band, canvas_low, canvas_mid, canvas_high

    if current_frequency_band == 'low':
        current_frequency_band = 'mid'
        canvas_low.get_tk_widget().pack_forget()
        canvas_mid.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas_high.get_tk_widget().pack_forget()
    elif current_frequency_band == 'mid':
        current_frequency_band = 'high'
        canvas_low.get_tk_widget().pack_forget()
        canvas_mid.get_tk_widget().pack_forget()
        canvas_high.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    elif current_frequency_band == 'high':
        current_frequency_band = 'low'
        canvas_low.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas_mid.get_tk_widget().pack_forget()
        canvas_high.get_tk_widget().pack_forget()

# open button
open_button = Button(
    root,
    text='Open a File',
    command=select_file
)
open_button.pack(expand=True)

# run the application
root.mainloop()

)
open_button.pack(expand=True)


# run the application
root.mainloop()
