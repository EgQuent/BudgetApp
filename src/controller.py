import os.path
from copy import deepcopy
import pandas as pd
from model import BasicModel

class Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.open_file()
        self.page_ctrl = None

    def start(self):
        buttons = list(self.model.json.keys())
        self.view.load_menu_view(buttons)

    def request_incomes_view(self, page_view):
        obj_data = self.model.json[str('Incomes')]
        self.page_ctrl = SimpleTreeViewController(obj_data, page_view, 'Incomes')
        
    def save_view_data(self):
        self.crt_ctrl.save_data(self.view.page)


class SimpleTreeViewController:

    def __init__(self, obj_data, page_view, title):
        self.view = page_view
        try :
            self.model = BasicModel(os.path.join( os.getcwd(), obj_data['file']))
            self.model.open_file()
        except :
            print("Cannot load table.")
        self.view.set_controller(self)
        self.load_data_to_view(title)

    def load_data_to_view(self, title):
        columns = list(self.model.df.columns)
        rows = self.model.df.to_numpy().tolist()
        total = self.get_total_amount("Montant")
        self.view.load_view(title, columns, rows, total)

    def update_data(self):
        headings = self.view.tree['columns']
        rows =[]
        for row_id in self.view.tree.get_children():
            rows.append(self.view.tree.item(row_id)['values'])
        data = {}
        for i in range(0, len(headings)):
            col = []
            for j in range(0, len(rows)):
                row = rows[j]
                try:
                    col.append(float(row[i]))
                except ValueError:
                    col.append(row[i])
                except IndexError:
                    col.append('')
            data[headings[i]] = col
        self.model.df = pd.DataFrame(data)
        # print(self.model.df.head(4))
        self.view.total.set(self.get_total_amount("Montant"))

    
    def save_data(self):
        self.update_data()
        self.model.save_file(self.model.df)

    def get_total_amount(self, key):
        sum = self.get_string_amount(key)
        return "Total = " + str(sum) + " €"

    def get_string_amount(self, key):
        sum = self.model.df[key].sum()
        return '{:,}'.format(round(sum,2)).replace(',', ' ')