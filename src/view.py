import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from customTk import BetterLabel, AmountVar, BetterTreeView, PandasTreeView
from datetime import datetime

class BasicView(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.page = None
        self.controller = None

    def save_current(self):
        if self.page is not None:
            if self.page.save_modification():
                self.controller.save_view_data()
            self.page.destroy()
        self.page = None

    def set_controller(self, controller):
        self.controller = controller

    def on_closing(self):
        if self.page :
            self.page.save_modification()
            self.parent.destroy()

    def load_view(self):
        pass


class MainView(BasicView):

    def __init__(self, parent):
        super().__init__(parent)
        parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.parent = parent
        self.menuView = None

    def load_view(self, buttons):
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=9, uniform='a')
        self.rowconfigure(0, weight=1)
        self.menuView = Menu(self)
        self.menuView.load_view(buttons)

    def request_incomes_view(self):
        self.save_current()
        self.page = SimpleTreeView(self, "Incomes")
        self.controller.request_incomes_view(self.page)
        
    def request_savings_view(self):
        self.save_current()
        self.page = SavingsView(self, "Savings")
        self.controller.request_savings_view(self.page)

    def request_cars_view(self):
        self.save_current()
        self.page = CarsView(self, "Cars")
        self.controller.request_cars_view(self.page)


class Menu(BasicView):

    def load_view(self, buttons):
        self.grid(row=0,column=0,sticky="nsew")
        for _ in range(len(buttons)):
            if "Incomes" in buttons:
                income_button = ttk.Button(self,text='Revenus', command=self.parent.request_incomes_view)
                income_button.pack(expand=False, fill="x")
                buttons.remove('Incomes')
            elif "Savings" in buttons:
                savings_button = ttk.Button(self,text='Epargnes', command=self.parent.request_savings_view)
                savings_button.pack(expand=False, fill="x")
                buttons.remove('Savings')
            elif "Cars" in buttons:
                savings_button = ttk.Button(self,text='Voitures', command=self.parent.request_cars_view)
                savings_button.pack(expand=False, fill="x")
                buttons.remove('Cars')
        ttk.Label(self, background="grey").pack(expand=True, fill="both")

class BasicPage(BasicView):
    
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title = title
        self.modified = False
        self.grid(row=0,column=1,sticky="nsew")
        self.init_layout()

    def init_layout(self):
        self.columnconfigure(0, weight=1, uniform='b')
        self.rowconfigure(0, weight=1, uniform='c')
        self.rowconfigure(1, weight=19, uniform='c')

        title_label = tk.Label(self, text=self.titled(self.title))
        title_label.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def titled(title):
        if title == "Incomes":
            return "Revenus"
        elif title == "Savings":
            return "Epargne"
        elif title == "Cars":
            return "Voitures"
        
    def updated_view(self, event = None):
        self.modified = True
        self.controller.update_data(True)
    
    def save_modification(self):
        if self.modified:
            if askyesno("Sauvegarder ?", "Voulez-vous sauvez les modifications ?"):
                self.controller.save_data()


class SimpleTreeView(BasicPage):

    def __init__(self, parent, title):
        super().__init__(parent, title)
        self.tree = None
        self.total_treeview = AmountVar(self, "- €")

    def init_layout(self):
        self.columnconfigure(0, weight=18, uniform='b')
        self.rowconfigure(0, weight=1, uniform='c')
        self.rowconfigure(1, weight=18, uniform='c')
        self.rowconfigure(2, weight=1, uniform='c')

        title_label = tk.Label(self, text=self.titled(self.title))
        title_label.grid(row=0, column=0, columnspan=3, sticky="nsew")

    def load_view(self, columns, rows):
        self.tree = BetterTreeView(self, rows, columns=columns, show='headings')
        self.tree.grid(row=1, column=0, sticky="nsew")

        self.tree.set_update_function(self.updated_view)
        self.tree.add = self.add_incomes

        # Add total at the end
        total_label = BetterLabel(self, "Total :", self.total_treeview, "€")
        total_label.grid(row=2, column=0, sticky="nse")

    def add_incomes(self):
        today = datetime.today().strftime("%d/%m/%Y")
        self.tree.insert('', 0, values=[today, "???", 0.0])

class SavingsView(SimpleTreeView):

    def __init__(self, parent, title):
        super().__init__(parent, title)
        self.total_inc = AmountVar(self, "- €")
        self.rate = tk.IntVar(self, 35)
        self.total_obj = AmountVar(self, "- €")
        self.saved = AmountVar(self, "- €")
        self.balance = AmountVar(self, "- €")

    def init_layout(self):
        self.columnconfigure(0, weight=11, uniform='b')
        self.columnconfigure(1, weight=8, uniform='b')
        self.rowconfigure(0, weight=1, uniform='c')
        self.rowconfigure(1, weight=18, uniform='c')
        self.rowconfigure(2, weight=1, uniform='c')

        title_label = tk.Label(self, text=self.titled(self.title))
        title_label.grid(row=0, column=0, columnspan=3, sticky="nsew")


    def load_view(self, columns, rows):
        super().load_view(columns, rows)

        balance_frame = ttk.Frame(self)
        balance_frame.grid(row=1,column=1, rowspan=2, sticky="nsew")

        total_inc_label = BetterLabel(balance_frame, "Revenus (total) :", self.total_inc, "€")
        total_inc_label.pack(fill='x', expand=False)

        rate_frame = ttk.Frame(balance_frame)
        rate_frame.columnconfigure(0, weight=3, uniform='e')
        rate_frame.columnconfigure(1, weight=3, uniform='e')
        rate_frame.columnconfigure(2, weight=1, uniform='e')
        rate_frame.rowconfigure(0, weight=1, uniform='f')
        rate_label = tk.Label(rate_frame, text="Taux (%) :")
        rate_entry = ttk.Entry(rate_frame, textvariable= self.rate)
        rate_entry.bind("<Return>", self.updated_view)
        rate_label.grid(row=0, column=0, sticky="nse")
        rate_entry.grid(row=0, column=1, sticky="nsew")
        rate_frame.pack(fill='x', expand=False)

        total_obj_label = BetterLabel(balance_frame, "Epargne cible :", self.total_obj, "€")
        total_obj_label.pack(fill='x', expand=False)

        total_saved_label = BetterLabel(balance_frame, "Epargne réelle :", self.saved, "€")
        total_saved_label.pack(fill='x', expand=False)

        balance_label = BetterLabel(balance_frame, "Balance :", self.balance, "€")
        balance_label.pack(fill='x', expand=False)

class NotebookView(BasicPage):

    def __init__(self, parent, title: str):
        super().__init__(parent, title)
        self.notebook = ttk.Notebook(self)
        self.tabs = []
        self.args = {}

    def init_args(self, tabs_dict: dict):
        self.tabs_keys = list(tabs_dict.keys())
        self.tabs_names = []
        for key in self.tabs_keys:
            self.tabs_names.append([str(key), tabs_dict[key]['name']])

    def load_view(self):
        for tab_name in self.tabs_names:
            crt_tab = ttk.Frame(self.notebook)
            crt_tab.key = tab_name[0]
            self.notebook.add(crt_tab, text=tab_name[1])
            self.tabs.append(crt_tab)
        self.notebook.grid(row=1,column=0, sticky="nsew")


class CarsView(NotebookView):

    CHOICES = ["Achat", "Maintenance"]

    def init_args(self, tabs_dict: dict):
        super().init_args(tabs_dict)
        for tab_key in self.tabs_keys:
            self.args[str(tab_key)] = {}
            self.args[str(tab_key)]['buy_kms'] = tk.IntVar()
            self.args[str(tab_key)]['max_kms'] = tk.IntVar(value=220000)
            self.args[str(tab_key)]['crt_kms'] = tk.IntVar()
            self.args[str(tab_key)]['pb_kms'] = tk.IntVar()
            self.args[str(tab_key)]['remaining_months'] = tk.IntVar()

            self.args[str(tab_key)]['total_buy'] = tk.DoubleVar()
            self.args[str(tab_key)]['coeff_rebuy'] = tk.DoubleVar()
            self.args[str(tab_key)]['jackpot_rebuy'] = tk.DoubleVar()
            self.args[str(tab_key)]['monthly_rebuy'] = tk.DoubleVar()

            self.args[str(tab_key)]['total_yearly_maint'] = tk.DoubleVar()
            self.args[str(tab_key)]['total_thisyear_maint'] = tk.DoubleVar()
            self.args[str(tab_key)]['coeff_maint'] = tk.DoubleVar()
            self.args[str(tab_key)]['jackpot_maint'] = tk.DoubleVar()
            self.args[str(tab_key)]['monthly_maint'] = tk.DoubleVar()

    
    def load_view(self, cars_tables: dict):
        super().load_view()
        for tab in self.tabs:
            tab.columnconfigure(0, weight=12, uniform='e')
            tab.columnconfigure(1, weight=8, uniform='e')
            tab.rowconfigure(0, weight=1, uniform='f')
            tab.rowconfigure(1, weight=1, uniform='f')

            cost_df = cars_tables[tab.key]['cost']
            kms_df = cars_tables[tab.key]['kms']

            tab.tree_expense = PandasTreeView(tab, dataframe=cost_df, show='headings')
            tab.tree_expense.grid(row=0, column=0, sticky="nsew")
            tab.tree_expense.set_update_function(self.updated_view)
            # tree_expense.add = self.add_expense

            tab.tree_kms = PandasTreeView(tab, dataframe=kms_df, show='headings')
            tab.tree_expense.set_choices(self.CHOICES, 4)
            tab.tree_kms.grid(row=1, column=0, sticky="nsew")
            tab.tree_kms.set_update_function(self.updated_view)

            box = ttk.Frame(tab)

            # KMS
            ttk.Label(box, text="--- Kilométrage ---").pack(fill='x', expand=False)
            buy_kms_label = BetterLabel(box, "Kms à l'achat :", self.args[tab.key]['buy_kms'], " (km)")
            buy_kms_label.pack(fill='x', expand=False)
            max_kms_label = BetterLabel(box, "Max kms :", self.args[tab.key]['max_kms'], " (km)")
            max_kms_label.pack(fill='x', expand=False)
            crt_kms_label = BetterLabel(box, "Kms actuels :", self.args[tab.key]['crt_kms'], " (km)")
            crt_kms_label.pack(fill='x', expand=False)
            self.args[tab.key]['pb_kms'].set(int(self.args[tab.key]['crt_kms'].get()/self.args[tab.key]['max_kms'].get()*100))
            pb = ttk.Progressbar(box,orient='horizontal',mode='determinate', variable=self.args[tab.key]['pb_kms'])
            pb.pack(fill='x', expand=False)
            remaining_days = BetterLabel(box, "Mois restants :", self.args[str(tab.key)]['remaining_months'], " (m)")
            remaining_days.pack(fill='x', expand=False)
            
            # REBUY
            ttk.Label(box, text="--- Amortissement ---").pack(fill='x', expand=False)
            buy_cost = BetterLabel(box, "Total d'achat :", self.args[str(tab.key)]['total_buy'], " (€)")
            buy_cost.pack(fill='x', expand=False)
            rebuy_coeff = BetterLabel(box, "Coeff. de sécurité :", self.args[str(tab.key)]['coeff_rebuy'], "")
            rebuy_coeff.pack(fill='x', expand=False)
            rebuy_jackpot = BetterLabel(box, "Cagnotte d'achat :", self.args[str(tab.key)]['jackpot_rebuy'], " (km)")
            rebuy_jackpot.pack(fill='x', expand=False)
            monthly_rebuy = BetterLabel(box, "Epargne :", self.args[str(tab.key)]['monthly_rebuy'], " (€/mois) ")
            monthly_rebuy.pack(fill='x', expand=False)
            
            # MAINTENANCE
            ttk.Label(box, text="--- Maintenance ---").pack(fill='x', expand=False)
            tym = BetterLabel(box, "Cout moy. :", self.args[str(tab.key)]['total_yearly_maint'], " (€/an)")
            tym.pack(fill='x', expand=False)
            ttym = BetterLabel(box, "Cout cette année :", self.args[str(tab.key)]['total_thisyear_maint'], " (€)")
            ttym.pack(fill='x', expand=False)
            maint_coeff = BetterLabel(box, "Coeff. de sécurité :", self.args[str(tab.key)]['coeff_maint'], "")
            maint_coeff.pack(fill='x', expand=False)
            maint_jackpot = BetterLabel(box, "Cagnotte maint. :", self.args[str(tab.key)]['jackpot_maint'], " (€)")
            maint_jackpot.pack(fill='x', expand=False)
            monthly_maint = BetterLabel(box, "Epargne :", self.args[str(tab.key)]['monthly_maint'], " (€/mois) ")
            monthly_maint.pack(fill='x', expand=False)

            box.grid(row=0, column=1, rowspan=2, sticky="nsew")

    def add_expense(self):
        today = datetime.today().strftime("%d/%m/%Y")
        self.tree.insert('', 0, values=[today, "???", 0.0])
    
    def add_kms(self):
        today = datetime.today().strftime("%d/%m/%Y")
        self.tree.insert('', 0, values=[today, "???", 0.0])
