import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from customTk import TreeviewEdit
from datetime import datetime

class MainView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.parent = parent

        # Layout
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=9, uniform='a')
        self.rowconfigure(0, weight=1)

        self.controller = None
        self.menuView = None
        self.page = None

    def set_controller(self, controller):
        self.controller = controller

    def load_menu_view(self, buttons):
        self.menuView = Menu(self, buttons)

    def request_incomes_view(self):
        self.save_current()
        self.page = SimpleTreeView(self)
        self.controller.request_incomes_view(self.page)
        
    def request_savings_view(self):
        self.save_current()

    def save_current(self):
        if self.page is not None:
            if self.page.save_modification():
                self.controller.save_view_data()
            self.page.destroy()
        self.page = None

    def on_closing(self):
        if self.page :
            self.page.save_modification()
            self.parent.destroy()


class Menu(ttk.Frame):
    def __init__(self, parent, buttons):
        super().__init__(parent)
        self.grid(row=0,column=0,sticky="nsew")
        for button in buttons:
            if button == "Incomes":
                income_button = ttk.Button(self,text='Revenus', command=parent.request_incomes_view)
                income_button.pack(expand=False, fill="x")
            elif button == "Savings":
                savings_button = ttk.Button(self,text='Epargnes', command=parent.request_savings_view)
                savings_button.pack(expand=False, fill="x")
        ttk.Label(self, background="grey").pack(expand=True, fill="both")

class SimpleTreeView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.page_ctrl = None
        self.tree = None
        self.modified = False
        self.total = tk.StringVar(self)
        self.grid(row=0,column=1,sticky="nsew")

    def set_controller(self, controller):
        self.page_ctrl = controller
        

    def load_view(self, title, columns, rows, total):
        
        # Set title and layout
        self.columnconfigure(0, weight=9, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')
        self.rowconfigure(0, weight=1, uniform='c')
        self.rowconfigure(1, weight=18, uniform='c')
        self.rowconfigure(2, weight=1, uniform='c')

        title_label = tk.Label(self, text=SimpleTreeView.titled(title))
        title_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

        data_frame = ttk.Frame(self)
        data_frame.grid(row=1,column=0,sticky="nsew")
        
        # Create TreeView
        self.tree = TreeviewEdit(data_frame, columns=columns, show='headings')
        for column in self.tree['columns']:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100)
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

        self.total.set(total)
        total_label = tk.Label(self, textvariable= self.total)
        total_label.grid(row=2, column=0, sticky="nse")

        self.tree.set_update_function(self.updated_view)

    def add_incomes(self):
        today = datetime.today().strftime("%d/%m/%Y")
        self.tree.insert('', 0, values=[today, "???", 0.0])
        
    def titled(title):
        if title == "Incomes":
            return "Revenus"
        
    def updated_view(self):
        self.modified = True
        self.page_ctrl.update_data()
    
    def save_modification(self):
        if self.modified:
            if askyesno("Sauvegarder ?", "Voulez-vous sauvez les modifications ?"):
                self.page_ctrl.save_data()



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