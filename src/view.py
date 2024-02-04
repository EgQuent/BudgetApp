import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from customTk import TreeviewEdit, BetterLabel, AmountVar
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
        self.page = CarsView(self, "Savings")
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
        self.columnconfigure(1, weight=1, uniform='b')
        self.rowconfigure(0, weight=1, uniform='c')
        self.rowconfigure(1, weight=18, uniform='c')
        self.rowconfigure(2, weight=1, uniform='c')

        title_label = tk.Label(self, text=self.titled(self.title))
        title_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

  

    def load_view(self, columns, rows):

        data_frame = ttk.Frame(self)
        data_frame.grid(row=1,column=0,sticky="nsew")
        
        # Create TreeView
        self.tree = TreeviewEdit(data_frame, columns=columns, show='headings')
        for column in self.tree['columns']:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=50)
        for row in rows:
            self.tree.insert('', tk.END, values=row)
        self.tree.modified = False
        self.tree.pack(fill='both', expand=True)
    
        # Add buttons frame
        buttons_frame = ttk.Frame(self)
        buttons_frame.grid(row=1,column=1,sticky="nsew")

        # Add button new line
        add_button = ttk.Button(buttons_frame, text='+', command= self.add_incomes)
        add_button.pack(fill='x', expand=False)

        # Add delete button
        add_button = ttk.Button(buttons_frame, text='-', command= self.tree.on_delete_pressed)
        add_button.pack(fill='x', expand=False)

        # Add total at the end
        total_label = BetterLabel(self, "Total :", self.total_treeview, "€")
        total_label.grid(row=2, column=0, sticky="nse")

        self.tree.set_update_function(self.updated_view)

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
        self.columnconfigure(0, weight=10, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')
        self.columnconfigure(2, weight=8, uniform='b')
        self.rowconfigure(0, weight=1, uniform='c')
        self.rowconfigure(1, weight=18, uniform='c')
        self.rowconfigure(2, weight=1, uniform='c')

        title_label = tk.Label(self, text=self.titled(self.title))
        title_label.grid(row=0, column=0, columnspan=3, sticky="nsew")


    def load_view(self, columns, rows):
        super().load_view(columns, rows)

        balance_frame = ttk.Frame(self)
        balance_frame.grid(row=1,column=2, rowspan=2, sticky="nsew")

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

    def load_view(self, tabs_name: list):
        for tab in tabs_name:
            crt_tab = ttk.Frame(self.notebook)
            self.notebook.add(crt_tab, text=tab)
        self.notebook.grid(row=1,column=0, sticky="nsew")


class CarsView(NotebookView):
    
    def load_view(self, tabs_name: list):
        super().load_view(tabs_name)
        tabs = self.notebook.children
        for tab in tabs:
            tab.columnconfigure(0, weight=11, uniform='e')
            tab.columnconfigure(1, weight=8, uniform='e')
            tab.rowconfigure(0, weight=1, uniform='f')
            tab.rowconfigure(1, weight=1, uniform='f')


class Page(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0,column=1,sticky="nsew")
        ttk.Label(self, background="blue").pack(expand=True, fill="both")
        # Create a Notebook (tabbed layout)
        self.notebook = ttk.Notebook(self)

        # Create and add tabs
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Tab 1")
        self.notebook.add(self.tab2, text="Tab 2")
        self.notebook.add(self.tab3, text="Tab 3")

        # Pack the notebook to make it visible
        self.notebook.pack(fill='both', expand=True)

        # Add content to the tabs (you can customize this)
        self.create_tab1_content()
        self.create_tab2_content()
        self.create_tab3_content()

    def create_tab1_content(self):
        label = ttk.Label(self.tab1, text="Content for Tab 1")
        label.pack(padx=10, pady=10)

        # Add more widgets as needed

    def create_tab2_content(self):
        label = ttk.Label(self.tab2, text="Content for Tab 2")
        label.pack(padx=10, pady=10)

        # Add more widgets as needed

    def create_tab3_content(self):
        label = ttk.Label(self.tab3, text="Content for Tab 3")
        label.pack(padx=10, pady=10)

        # Add more widgets as needed