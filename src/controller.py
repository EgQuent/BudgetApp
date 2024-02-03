import os.path
from copy import deepcopy
import pandas as pd
from model import BasicModel

class BasicController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def start(self):
        pass

class Controller(BasicController):

    def __init__(self, model, view):
        super().__init__(model, view)
        self.page_ctrl = None

    def start(self):
        buttons = list(self.model.json.keys())
        self.view.load_view(buttons)

    def request_incomes_view(self, page_view):
        obj_data = self.model.json[str('Incomes')]
        self.page_ctrl = SimpleTreeViewController(obj_data['file'], page_view)
        page_view.set_controller(self.page_ctrl)
        self.page_ctrl.start("Montant")

    def request_savings_view(self, page_view):
        obj_data = self.model.json[str('Savings')]
        self.page_ctrl = SavingsController(obj_data['file'], page_view)
        page_view.set_controller(self.page_ctrl)
        self.page_ctrl.start("Montant")

class PageController(BasicController):

    def save_data(self):
        self.update_data()
        self.model.save_file(self.model.df)

    def update_data(self):
        pass


class SimpleTreeViewController(PageController):

    def __init__(self, model, page_view):
        super().__init__(model, page_view)

    def start(self, key):
        columns = list(self.model.df.columns)
        rows = self.model.df.to_numpy().tolist()
        sum = self.get_total(key)
        total = self.get_total_string(sum)
        self.view.total.set(total)
        self.view.load_view(columns, rows)

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
        sum = self.get_total("Montant")
        self.view.total.set(self.get_total_string(sum))

    def get_total(self, key):
        return round(float(self.model.df[key].sum()), 2)

    @staticmethod
    def get_string_amount(value):
        return '{:,}'.format(value).replace(',', ' ')
    
    def get_total_string(self, sum):
        return "Total = " + self.get_string_amount(sum) + " €"
    
class SavingsController(SimpleTreeViewController):
    pass
    
