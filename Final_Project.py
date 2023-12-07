import tkinter as tk
import wave
import contextlib
import matplotlib.pyplot as plt
import numpy as np
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

from pydub import AudioSegment
output = "result.wav"
gfile = ''
# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('300x150')

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

    gfile_label = ttk.Label(root, text=gfile)
    gfile_label.pack(side="bottom")

    with contextlib.closing(wave.open(gfile, 'r')) as f:
        print("num channels: ", f.getnchannels())
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        print(duration)
        sig = np.frombuffer(f.readframes(16000), dtype=np.int16)
        sig = sig[:]

        plt.figure(1)
        plt.title("Clap")
        plt.plot(sig)
        plt.show()



# open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)

open_button.pack(expand=True)

# run the application
root.mainloop()