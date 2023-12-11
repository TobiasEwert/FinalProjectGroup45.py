import tkinter as tk
import wave
import contextlib
import matplotlib.pyplot as plt
import numpy as np
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from os import path
from pydub import utils, AudioSegment
from pydub.playback import play

output = "result.wav"
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
def convert_to_wav(filename):
    main, extension = path.splitext(filename)
    if extension != ".wav":
        extension = ".wav"
        sound = AudioSegment.from_file(filename)
        sound.export(main + extension, format="wav")
        gfile = main + extension
    else:
        gfile = filename
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


        gfile_label = ttk.Label(root, text=filename)
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

    except:
        showinfo(
            title='Filetype not supported',
            message= 'Please select a supported audio file type.'
        )
# open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)

open_button.pack(expand=True)

# run the application
root.mainloop()