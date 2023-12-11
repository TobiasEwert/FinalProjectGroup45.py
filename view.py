from tkinter import *
from tkinter.messagebox import showinfo
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Main class to handle the user's view
class Main():
    def __init__(self, Model):
        self.current_frequency_band='low'
        self.model = Model
        self.root = Tk()
        self.root.title("Team 45's Final Project")
        self.root.resizable(True, True)
        self.root.geometry('1500x800')
        self.root.state('zoomed')
        self.root.minsize(500, 250)
        self.frame = Frame(self.root)
        self.root.grid_columnconfigure(1, weight=1) #Adjusting columns and rows for appearance
        self.root.grid_columnconfigure(2, weight =1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_rowconfigure(0, weight =1)
        self.root.grid_rowconfigure(1, weight =1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_rowconfigure(9, weight=6)
        #button to open a file
        self.open_button = Button(
            self.root,
            text='Open an Audio File',
            width = 25, height = 2
        )
        self.open_button.grid(row=1, column=1, columnspan=3)
        #Label displaying the file's name and path
        self.gfile_label = Label(self.root, text=self.model.gfile)
        self.gfile_label.grid(row=0, column=1, columnspan=3)

    #function to change the file name and path label
    def gfile_text(self):
        self.gfile_label.config(text=self.model.gfile)

    #function to open a success window stating the selected file
    def showfile(self):
        showinfo(
            title='Selected File',
            message=self.model.filename)

    #function to display a label with the length of the audio file in seconds
    def show_time(self):
        seconds = Label(self.root, text=("Time in seconds: " + self.model.dura[:4]))
        seconds.grid(row = 1, column =1)

    def frequencies(self):
        # Display frequency band powers
        low_freq_label = Label(self.root, text=f"Low Frequency Band Power: {round(self.model.low_power)}",
            width = 50, height = 2)
        low_freq_label.grid(row=2, column=1)

        mid_freq_label = Label(self.root, text=f"Mid Frequency Band Power: {round(self.model.mid_power)}",
            width = 50, height = 2)
        mid_freq_label.grid(row = 3, column = 1)

        high_freq_label = Label(self.root, text=f"High Frequency Band Power: {round(self.model.high_power)}",
            width = 50, height = 2)
        high_freq_label.grid(row = 4, column = 1)

        dominant_freq_label = Label(self.root, text=f"Dominant Frequency: {round(self.model.dominant_frequency)}Hz")
        dominant_freq_label.grid(row = 5, column = 1)
    def disp_plot(self):
        #Displays the graphs, with Low shown first
        canvas = FigureCanvasTkAgg(self.model.fig_waveform, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(column = 1, row = 7, rowspan = 2)
        self.canvas_low = FigureCanvasTkAgg(self.model.fig_low, master=self.root)
        self.canvas_low.get_tk_widget().grid(column = 2, row = 7, rowspan = 2)
        self.canvas_mid = FigureCanvasTkAgg(self.model.fig_mid, master=self.root)
        self.canvas_high = FigureCanvasTkAgg(self.model.fig_high, master=self.root)
        self.canvas_all = FigureCanvasTkAgg(self.model.fig_all, master=self.root)
        self.canvas_high.get_tk_widget().grid_forget()
        #button to switch between the plots
        switch_button = Button(
            self.root,
            text='Switch Frequency Band',
            command=self.switch_frequency_band,
            width = 25, height = 2
        )
        switch_button.grid(row =7, column = 3)
        #button to show the entire frequency band's graph
        self.all_button = Button(
            self.root,
            text='Combine All Frequency Plots',
            command=self.all_freq_band,
            width = 25, height = 2
        )
        self.all_button.grid(row=8, column = 3)

    #function for the switch button to switch graphs
    def switch_frequency_band(self):
        global canvas_low, canvas_mid, canvas_high
        if self.current_frequency_band == 'low':
            self.current_frequency_band = 'mid'
            self.canvas_low.get_tk_widget().grid_forget()
            self.canvas_mid.get_tk_widget().grid(column = 2, row = 7, rowspan = 2)
            self.canvas_high.get_tk_widget().grid_forget()

        elif self.current_frequency_band == 'mid':
            self.current_frequency_band = 'high'
            self.canvas_low.get_tk_widget().grid_forget()
            self.canvas_mid.get_tk_widget().grid_forget()
            self.canvas_high.get_tk_widget().grid(column = 2, row = 7, rowspan = 2)
        elif self.current_frequency_band == 'high':
            self.current_frequency_band = 'low'
            self.canvas_low.get_tk_widget().grid(column = 2, row = 7, rowspan = 2)
            self.canvas_mid.get_tk_widget().grid_forget()
            self.canvas_high.get_tk_widget().grid_forget()
        elif self.current_frequency_band == 'all':
            self.current_frequency_band = 'low'
            self.canvas_low.get_tk_widget().grid(column = 2, row = 7, rowspan = 2)
            self.canvas_mid.get_tk_widget().grid_forget()
            self.canvas_high.get_tk_widget().grid_forget()
            self.canvas_all.get_tk_widget().grid_forget()
            self.all_button.config(text='Combine All Frequency Plots')

    #function for the entire band button to change the graphs
    def all_freq_band(self):
        if self.current_frequency_band != 'all':
            self.current_frequency_band = 'all'
            self.canvas_low.get_tk_widget().grid_forget()
            self.canvas_mid.get_tk_widget().grid_forget()
            self.canvas_high.get_tk_widget().grid_forget()
            self.canvas_all.get_tk_widget().grid(column = 2, row = 7, rowspan = 2)
            self.all_button.config(text='Uncombine Plots')
        elif self.current_frequency_band == 'all':
            self.current_frequency_band = 'low'
            self.canvas_low.get_tk_widget().grid(column = 2, row = 7, rowspan = 2)
            self.canvas_mid.get_tk_widget().grid_forget()
            self.canvas_high.get_tk_widget().grid_forget()
            self.canvas_all.get_tk_widget().grid_forget()
            self.all_button.config(text='Combine All Frequency Plots')

    #Function to display and error window for an incorrect file type
    def file_error(self):
        showinfo(
            title='Filetype not supported',
            message='Please select a supported audio file type.'
        )

    #function to start the application window
    def startView(self):
        self.root.mainloop()