import model
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Main():
    def __init__(self, Model):
        self.gfile_string = " "
        self.model = Model
        self.root = Tk()
        self.root.title('Tkinter Open File Dialog')
        self.root.resizable(True, True)
        self.root.geometry('1000x800')
        self.root.minsize(500, 250)
        self.frame = Frame(self.root)
        self.open_button = Button(
            self.root,
            text='Open a File'
        )
        self.open_button.pack(expand=True)



        #self.model.show_time()
        #seconds = Label(self, text=("Time in seconds: " + self.model.dura[:4]))
        #seconds.place(x=20, y=20)
    def gfile_text(self):
        self.gfile_label = Label(self.root, text = self.model.gfile)
        self.gfile_label.pack(side="bottom")
    def showfile(self):
        showinfo(
            title='Selected File',
            message=self.model.filename)
    def show_time(self):
        seconds = Label(self.root, text=("Time in seconds: " + self.model.dura[:4]))
        seconds.place(x=20, y=20)
    def frequencies(self):
        # Display frequency band powers
        low_freq_label = Label(self.root, text=f"Low Frequency Band Power: {self.model.low_power}")
        low_freq_label.place(x=20, y=60)

        mid_freq_label = Label(self.root, text=f"Mid Frequency Band Power: {self.model.mid_power}")
        mid_freq_label.place(x=20, y=80)

        high_freq_label = Label(self.root, text=f"High Frequency Band Power: {self.model.high_power}")
        high_freq_label.place(x=20, y=100)

        dominant_freq_label = Label(self.root, text=f"Dominant Frequency: {round(self.model.dominant_frequency)}Hz")
        dominant_freq_label.place(x=20, y=120)
    def disp_plot(self):
        canvas = FigureCanvasTkAgg(self.model.fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #canvas_low = FigureCanvasTkAgg(self.model.fig_low, master=self.root)
        #canvas_low.get_tk_widget().pack_forget()
    def startView(self):
        self.root.mainloop()





