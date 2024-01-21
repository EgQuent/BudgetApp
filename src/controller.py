import os.path
from copy import deepcopy
import pandas as pd
from model import BasicModel

class Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.open_file()
        self.crt_ctrl = None

    def start(self):
        buttons = list(self.model.json.keys())
        self.view.load_menu_view(buttons)

    def get_vm(self, request):
        obj_data = self.model.json[str(request)]
        print(obj_data)
        if request == "Incomes":
            self.crt_ctrl = SimpleTreeViewController(obj_data)
            return self.crt_ctrl.get_data()
        
    def save_view_data(self):
        self.crt_ctrl.save_data(self.view.page)


class SimpleTreeViewController:

    def __init__(self, obj_data):
        try :
            self.model = BasicModel(os.path.join( os.getcwd(), obj_data['file']))
            self.model.open_file()
        except :
            print("Cannot load table.")

    def get_data(self):
        return deepcopy(self.model.df)
    
    def save_data(self, page):
        headings = page.tree['columns']
        rows =[]
        for row_id in page.tree.get_children():
            rows.append(page.tree.item(row_id)['values'])
        data = {}
        for i in range(0, len(headings)):
            col = []
            for j in range(0, len(rows)):
                row = rows[j]
                try:
                    col.append(row[i])
                except IndexError:
                    col.append('')
            data[headings[i]] = col
        df = pd.DataFrame(deepcopy(data))
        self.model.save_file(df)