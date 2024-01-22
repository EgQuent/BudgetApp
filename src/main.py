import tkinter as tk
import os.path
from view import MainView
from controller import Controller
from model import BasicModel

class App(tk.Tk):

    STD_SIZE_X = 600
    STD_SIZE_Y = 600
    DATA_FILE = "./resources/data.json"

    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.geometry(f"{self.STD_SIZE_X}x{self.STD_SIZE_Y}")
        self.minsize(self.STD_SIZE_X, self.STD_SIZE_Y)

        # create a model
        mainModel = BasicModel(os.path.join( os.getcwd(), self.DATA_FILE))

        # create a view and place it on the root window
        view = MainView(self)
        view.pack(expand=True, fill="both")

        # create a controller
        controller = Controller(mainModel, view)

        # set the controller to view
        view.set_controller(controller)

        #start controller
        controller.start()


if __name__ == '__main__':
    app = App("Py Budget Application")
    app.mainloop()