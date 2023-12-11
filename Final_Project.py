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
from pydub import AudioSegment
from scipy.io import wavfile
from scipy.signal import welch

gfile = ''
# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('1000x500')
frame = tk.Frame(root)
'''
tkinter.filedialog.askopenfilenames(**options)
Create an Open dialog and 
return the selected filename(s) that correspond to 
existing file(s).
'''


def select_file():
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

    gfile_label = Label(root, text=gfile)
    gfile_label.pack(side="bottom")

    #finds and prints time of sound
    with contextlib.closing(wave.open(gfile, 'r')) as f:
        numch = f.getnchannels()
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        dura = str(duration)
        seconds = Label(root, text = ("Time in seconds: " + dura[:4]))
        seconds.place(x=70, y=90)


    #finds freq
    sample_rate, data = wavfile.read(gfile)
    frequencies, power = welch(data, sample_rate, nperseg = 4096)
    dominant_frequency = frequencies[np.argmax(power)]
    print(f'dominant_frequency is {round(dominant_frequency)}Hz')

    #plots the waveform
    fig = Figure(figsize = (5,5), dpi = 100)
    plt = fig.add_subplot(111)
    time = np.linspace(0., duration, data.shape[0])
    plt.plot(time, data[:], label="Left channel")
    plt.legend()
    canvas = FigureCanvasTkAgg(fig,
                               master = root)
    canvas.draw()
    canvas.get_tk_widget().pack()


# open button
open_button = Button(
    root,
    text='Open a File',
    command=select_file
)
open_button.pack(expand=True)


# run the application
root.mainloop()