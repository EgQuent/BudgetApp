import tkinter as tk
from view import MainView
from controller import Controller
from model import Model

class App(tk.Tk):

    STD_SIZE_X = 920
    STD_SIZE_Y = 650
    DATA_FILE = "./resources/data.json"

    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.geometry(f"{self.STD_SIZE_X}x{self.STD_SIZE_Y}")
        self.minsize(self.STD_SIZE_X, self.STD_SIZE_Y)

        # create a controller
        model = Model(self.DATA_FILE)

        # create a view and place it on the root window
        view = MainView(self)
        self.protocol("WM_DELETE_WINDOW", view.on_closing)
        view.pack(expand=True, fill="both")

        # create a controller
        controller = Controller(model, view)
        print(controller.model)

        # set the controller to view
        view.set_controller(controller)

        # start controller
        controller.start()

        print("END")

    @classmethod
    def set_window(cls):
        pass


if __name__ == '__main__':
    app = App("Py Budget Application")
    app.mainloop()