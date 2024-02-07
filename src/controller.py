from tools import make_df, min_col_df, max_col_df, older_id, newer_id, in_range_id
from datetime import datetime, timedelta

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
        self.update_data(True)
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
            self.table = make_df(headings, rows)
        self.total_tree = self.get_total("Montant")
        self.view.total_treeview.set(self.total_tree)

    def get_total(self, key):
        return round(float(self.table[key].sum()), self.DIGITS)
    
    def get_total_string(self, sum):
        return "Total = " + self.get_string_amount(sum) + " €"
    
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

    SECU_COEFF_B = 1.25
    SECU_COEFF_M = 1.3

    def __init__(self, model, page_view):
        super().__init__(model, page_view)
        self.cars = self.model.cars
        self.cars_tables = self.model.cars_tables
        self.data = {}
        for car in self.cars:
            self.data[str(car)] = {}
            self.data[str(car)]['max_kms'] = self.model.data['Cars'][str(car)]['end_kms']

    def start(self):
        self.view.init_args(self.model.data['Cars'])
        self.update_data(False)
        self.view.load_view(self.cars_tables)
        self.save_data()

    def update_data(self, from_view : bool):
        if from_view:
            for tab in self.view.tabs:
                self.cars_tables[tab.key]['cost'] = tab.tree_expense.get_dataframe()
                self.cars_tables[tab.key]['kms'] = tab.tree_kms.get_dataframe()
        for car in self.cars:
            min_kms = min_col_df(self.cars_tables[str(car)]['kms'], 2)
            crt_kms = max_col_df(self.cars_tables[str(car)]['kms'], 2)
            max_kms = self.data[str(car)]['max_kms']
            remaining_kms = max_kms - crt_kms
            usage_rate = (crt_kms-min_kms)/(max_kms-min_kms)

            self.view.args[str(car)]['buy_kms'].set(min_kms)
            self.view.args[str(car)]['max_kms'].set(max_kms)
            self.view.args[str(car)]['crt_kms'].set(crt_kms)
            pb_kms = int(crt_kms/max_kms*100)
            self.view.args[str(car)]['pb_kms'].set(pb_kms)

            _kms_dates = list(self.cars_tables[str(car)]['kms']['Date'])
            buy_date_id = older_id(_kms_dates)
            buy_date = self.cars_tables[str(car)]['kms']['Date'][buy_date_id]
            buy_date = datetime.strptime(buy_date, '%d/%m/%Y')
            last_date_id = newer_id(_kms_dates)
            last_date = self.cars_tables[str(car)]['kms']['Date'][last_date_id]
            last_date = datetime.strptime(last_date, '%d/%m/%Y')
            delta_date = last_date - buy_date
            used_days = int(delta_date.total_seconds()/3600/24)
            delta_kms = crt_kms - min_kms
            v_kms = delta_kms/used_days
            delta_dates = datetime.today() - last_date
            remaining_days = int(remaining_kms / v_kms) - int(delta_dates.total_seconds()/3600/24)
            self.view.args[str(car)]['remaining_months'].set(int(remaining_days/30.44))

            buy_expenses = self.cars_tables[str(car)]['cost'][self.cars_tables[str(car)]['cost']['Type'] == "Achat"]
            total_expense = float(buy_expenses[self.AKEY].sum())
            sec_total_expense = self.SECU_COEFF_B * total_expense
            rebuy_jackpot = sec_total_expense * usage_rate
            rebuy_monthly_savings = (sec_total_expense - rebuy_jackpot)/(remaining_days/30.44)
            self.view.args[str(car)]['total_buy'].set(round(total_expense, self.DIGITS))
            self.view.args[str(car)]['coeff_rebuy'].set(round(self.SECU_COEFF_B, self.DIGITS))
            self.view.args[str(car)]['jackpot_rebuy'].set(round(rebuy_jackpot, self.DIGITS))
            self.view.args[str(car)]['monthly_rebuy'].set(round(rebuy_monthly_savings, self.DIGITS))

            maint_expenses = self.cars_tables[str(car)]['cost'][self.cars_tables[str(car)]['cost']['Type'] == "Maintenance"]
            _maint_dates = list(maint_expenses['Date'])
            total_expense_maint = float(maint_expenses[self.AKEY].sum())
            
            last_date_id_m = newer_id(_maint_dates)
            last_date_m = _maint_dates[last_date_id_m]
            last_date_m = datetime.strptime(last_date_m, '%d/%m/%Y')
            
            delta_date_m = last_date_m - buy_date
            maint_days = int(delta_date_m.total_seconds()/3600/24)
            annual_cost = total_expense_maint / maint_days * 365.25
            last_year = datetime.today() - timedelta(days=365.25)
            
            in_year_exp_id = in_range_id(_maint_dates, last_year, datetime.today())
            total_maint_year = self.selected_sum(list(maint_expenses[self.AKEY]), in_year_exp_id)

            anticipated_exp_id = in_range_id(_maint_dates, datetime.today(), last_date_m)
            anticipated_exp = self.selected_sum(list(maint_expenses[self.AKEY]), anticipated_exp_id)

            remaining_jackpot = self.SECU_COEFF_M *(annual_cost-total_maint_year)
            target_jackpot = max(anticipated_exp, anticipated_exp + remaining_jackpot)

            maint_monthly_savings = (target_jackpot)/12
            
            self.view.args[str(car)]['total_yearly_maint'].set(round(annual_cost, self.DIGITS))
            self.view.args[str(car)]['total_thisyear_maint'].set(round(total_maint_year, self.DIGITS))
            self.view.args[str(car)]['coeff_maint'].set(round(self.SECU_COEFF_M, self.DIGITS))
            self.view.args[str(car)]['jackpot_maint'].set(round(target_jackpot, self.DIGITS))
            self.view.args[str(car)]['monthly_maint'].set(round(maint_monthly_savings, self.DIGITS))

    def update_model(self):
        self.model.cars_tables = self.cars_tables

    @staticmethod
    def selected_sum(complete_list, id_list):
        selected_values = []
        for n in id_list:
            selected_values.append(complete_list[n])
        if selected_values == []:
            return 0.
        return sum(selected_values)
