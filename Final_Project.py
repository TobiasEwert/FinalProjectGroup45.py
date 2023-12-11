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
# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('1000x500')
frame = tk.Frame(root)

def select_file():
    global gfile

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

        # Compute frequency bands
        low_freq_band = (20, 200)
        mid_freq_band = (200, 2000)
        high_freq_band = (2000, 20000)

        low_power = np.sum(power[(frequencies >= low_freq_band[0]) & (frequencies <= low_freq_band[1])])
        mid_power = np.sum(power[(frequencies >= mid_freq_band[0]) & (frequencies <= mid_freq_band[1])])
        high_power = np.sum(power[(frequencies >= high_freq_band[0]) & (frequencies <= high_freq_band[1])])

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
        fig = Figure(figsize=(4, 4), dpi=100)
        plt = fig.add_subplot(111)
        time = np.linspace(0., duration, data.shape[0])
        plt.plot(time, data[:], label="Left channel")
        plt.legend()
        plt.set_xlabel('Time (s)')
        plt.set_ylabel('Amplitude')
        plt.margins(0.1)  # Add padding
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# open button
open_button = Button(
    root,
    text='Open a File',
    command=select_file
)
open_button.pack(expand=True)

# run the application
root.mainloop()
