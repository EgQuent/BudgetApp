import pandas as pd

class BasicController:

    AKEY = 'Montant'
    DIGITS = 2

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
        buttons = list(self.model.data.keys())
        self.view.load_view(buttons)

    def request_incomes_view(self, page_view):
        self.page_ctrl = IncomesController(self.model, page_view)
        page_view.set_controller(self.page_ctrl)
        self.page_ctrl.start(self.AKEY)

    def request_savings_view(self, page_view):
        self.page_ctrl = SavingsController(self.model, page_view)
        page_view.set_controller(self.page_ctrl)
        self.page_ctrl.start(self.AKEY)

    def request_cars_view(self, page_view):
        self.page_ctrl = CarsController(self.model, page_view)
        page_view.set_controller(self.page_ctrl)
        self.page_ctrl.start()

class PageController(BasicController):

    def update_data(self, from_view : bool):
        pass

    def update_model(self):
        pass

    def save_data(self):
        self.update_data(False)
        self.update_model()
        self.model.save()


class TreeViewController(PageController):

    def __init__(self, model, page_view):
        super().__init__(model, page_view)
        self.table = None
        self.total_tree = None

    def start(self, key):
        columns = list(self.table.columns)
        rows = self.table.to_numpy().tolist()
        self.update_data(False)
        self.view.load_view(columns, rows)
        self.save_data()

    def update_data(self, from_view : bool):
        if from_view:
            headings = self.view.tree['columns']
            rows =[]
            for row_id in self.view.tree.get_children():
                rows.append(self.view.tree.item(row_id)['values'])
            self.table = self.remake_df(headings, rows)
        self.total_tree = self.get_total("Montant")
        self.view.total_treeview.set(self.total_tree)

    def get_total(self, key):
        return round(float(self.table[key].sum()), self.DIGITS)
    
    def get_total_string(self, sum):
        return "Total = " + self.get_string_amount(sum) + " €"
    
    @staticmethod
    def remake_df(headings, rows):
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
        return pd.DataFrame(data)


class IncomesController(TreeViewController):

    def __init__(self, model, page_view):
        super().__init__(model, page_view)
        self.table = self.model.incomes_table
        self.total_tree = round(self.model.data['Incomes']['total'], self.DIGITS)

    def update_model(self):
        self.model.incomes_table = self.table
        self.model.data['Incomes']['total'] = round(self.total_tree, self.DIGITS)
    
class SavingsController(TreeViewController):
    
    def __init__(self, model, page_view):
        super().__init__(model, page_view)
        self.table = self.model.savings_table
        self.rate = int(self.model.data['Savings']['save_rate'])
        self.total_tree = round(self.model.data['Savings']['total_saved'], self.DIGITS)
        self.balance = round(self.model.data['Savings']['balance'], self.DIGITS)
        self.total_incomes = round(self.model.data['Incomes']['total'], self.DIGITS)
        self.total_obj = round(self.model.data['Savings']['total_obj'], self.DIGITS)

    def update_data(self, from_view: bool):
        super().update_data(from_view)
        if from_view :
            self.rate = self.view.rate.get()
        self.view.total_inc.set(self.total_incomes)
        self.view.rate.set(int(self.rate))
        self.total_obj = round(self.rate/100*self.total_incomes, self.DIGITS)
        self.view.total_obj.set(self.total_obj)
        self.view.saved.set(self.total_tree)
        self.balance = self.total_tree - self.total_obj
        self.view.balance.set(self.balance)

    def update_model(self):
        self.model.savings_table = self.table
        self.model.data['Savings']['save_rate'] = round(self.rate, self.DIGITS)
        self.model.data['Savings']['total_saved'] = round(self.total_tree, self.DIGITS)
        self.model.data['Savings']['total_obj'] = round(self.total_obj, self.DIGITS)
        self.model.data['Savings']['balance'] = round(self.balance, self.DIGITS)
    
class CarsController(PageController):

    def __init__(self, model, page_view):
        super().__init__(model, page_view)
        self.cars = self.model.cars
        self.cars_tables = self.model.cars_tables

    def start(self):
        self.update_data(False)
        cars_name = []
        for car in self.cars:
            cars_name.append(self.model.data['Cars'][car]['name'])
        self.view.load_view(cars_name)
        self.save_data()