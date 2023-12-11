import tkinter as tk
import wave
import contextlib
import matplotlib.pyplot as plt
import numpy as np
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

output = "result.wav"
gfile = ''
# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(True, True)
root.geometry('1000x500')
frame = tk.Frame(root)
'''
tkinter.filedialog.askopenfilenames(**options)
Create an Open dialog and 
return the selected filename(s) that correspond to 
existing file(s).
'''
def to_single_channel(filename):
    raw_audio = AudioSegment.from_file(filename, format="wav")
    channel_count = raw_audio.channels
    mono_wav = raw_audio.set_channels(1)
    mono_wav.export(filename, format="wav")
def convert_to_wav(filename):
    main, extension = path.splitext(filename)
    if extension != ".wav":
        extension = ".wav"
        sound = AudioSegment.from_file(filename)
        sound.export(main + extension, format="wav")
        gfile = main + extension
    else:
        gfile = filename
    to_single_channel(gfile)
    return gfile

def select_file():
    filetypes = (
        ('Audio files', ".wav"),
        ('Audio files' , ".m4a"),
        ('Audio files', ".mp3"),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    try:
        gfile = convert_to_wav(filename)
        # tkinter.messagebox — Tkinter message prompts
        showinfo(
            title='Selected File',
            message=filename
        )

        gfile_label = Label(root, text=gfile)
        gfile_label.pack(side="bottom")

        #finds and prints time of sound
        with contextlib.closing(wave.open(gfile, 'r')) as f:
            numch = f.getnchannels()
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            dura = str(duration)
            seconds = Label(root, text=("Time in seconds: " + dura[:4]))
            seconds.place(x=20, y=20)


        #finds frequencies
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
        fig = Figure(figsize=(3, 4), dpi=100)
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

    except:
        showinfo(
            title='Filetype not supported',
            message='Please select a supported audio file type.'
        )

# open button
open_button = Button(
    root,
    text='Open a File',
    command=select_file
)
open_button.pack(expand=True)


# run the application
root.mainloop()