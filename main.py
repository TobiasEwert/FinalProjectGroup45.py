from model import Model
from view import Main

#Controller class to control both the model and view
class Controller:
    def __init__(self, Model, Main):
        self.model = Model
        self.frame = Main
        self.open_button()
    #open_button function gives the open file button a command
    def open_button(self):
        #on_click function contains all of the model and view functions that the button needs to run
        def on_click():
            try:
                self.model.select_file()
                self.frame.showfile(),
                self.frame.gfile_text()
                self.model.show_time()
                self.frame.show_time()
                self.model.freq_calc()
                self.frame.frequencies()
                self.frame.disp_plot()
            except:
                self.frame.file_error()
        self.frame.open_button.config(command=lambda: on_click())
    #start function to start the view
    def start(self):
        self.frame.startView()
#main function to create the model, view, and controller objects and start the application
def main():
    model = Model()
    view = Main(model)
    controller = Controller(model, view)
    controller.start()
if __name__=='__main__':
    main()

