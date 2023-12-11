from model import Model
from view import Main

class Controller:
    def __init__(self, Model, Main):
        self.model = Model
        self.frame = Main
        self.open_button()
    #def seconds(self):
        #self.frame.seconds_label.config(text=("Time in seconds: " + self.model.dura[:4]))
    def gfile_text(self):
        self.frame.gfile_string = self.model.gfile
    def open_button(self):
        def on_click():
            self.model.select_file()
            self.frame.showfile(),
            self.frame.gfile_text()
            self.model.show_time()
            self.frame.show_time()
            self.model.dom_freq()
            self.model.freq_calc()
            self.frame.frequencies()
            self.model.plot_waveform()
            self.frame.disp_plot()
        self.frame.open_button.config(command=lambda: on_click())
    def start(self):

        self.frame.startView()

def main():
    model = Model()
    view = Main(model)
    controller = Controller(model, view)
    controller.start()
main()

