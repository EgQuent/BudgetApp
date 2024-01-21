import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from CustomTk import TreeviewEdit

class MainView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        print("Class MainView init.")

        # Create grid for sidebar and main content
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=9, uniform='a')
        self.rowconfigure(0, weight=1)

        self.controller = None
        self.menuView = None
        self.page = None

    def load_menu_view(self, buttons):
        self.menuView = Menu(self, buttons)

    def load_incomes_view(self):
        print("Button incomes clicked.")
        self.save_current()
        df = self.controller.get_vm('Incomes')
        self.page = SimpleTreeView(self, 'Incomes', df)
        #self.view.create_treeview_page(list(self.model.df.columns), self.model.df.to_numpy().tolist())

    def load_savings_view(self):
        print("Button savings clicked.")
        self.save_current()
        self.controller.get_vm('Savings')
        self.page = None

    def set_controller(self, controller):
        print("Class MainView set_controller.")
        self.controller = controller

    def save_current(self):
        if self.page is not None:
            if self.page.save_modification():
                self.controller.save_view_data()
            self.page.destroy()
            self.page = None


class Menu(ttk.Frame):
    def __init__(self, parent, buttons):
        super().__init__(parent)
        print("Class Menu init.")
        self.grid(row=0,column=0,sticky="nsew")
        for button in buttons:
            if button == "Incomes":
                income_button = ttk.Button(self,text='Revenus', command=parent.load_incomes_view)
                income_button.pack(expand=False, fill="x")
            elif button == "Savings":
                savings_button = ttk.Button(self,text='Epargnes', command=parent.load_savings_view)
                savings_button.pack(expand=False, fill="x")
        ttk.Label(self, background="grey").pack(expand=True, fill="both")

class SimpleTreeView(ttk.Frame):
    def __init__(self, parent, title, data):
        super().__init__(parent)
        self.parent = parent
        self.tree = None
        self.grid(row=0,column=1,sticky="nsew")
        self.init_view(title, data)
        

    def init_view(self, title, data):
        columns = list(data.columns)
        rows = data.to_numpy().tolist()
        print("Class CSV Tree View init.")
        self.columnconfigure(0, weight=9, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')
        self.rowconfigure(0, weight=1, uniform='c')
        self.rowconfigure(1, weight=19, uniform='c')

        title_label = tk.Label(self, text=SimpleTreeView.titled(title))
        title_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

        data_frame = ttk.Frame(self)
        data_frame.grid(row=1,column=0,sticky="nsew")
        
        self.tree = TreeviewEdit(data_frame, columns=columns, show='headings')
        for column in self.tree['columns']:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100)
        for row in rows:
            self.tree.insert('', tk.END, values=row)
        self.tree.modified = False
        self.tree.pack(fill='both', expand=True)
    
        add_button = ttk.Button(self, text='+', command= self.add_incomes)
        add_button.grid(row=1,column=1,sticky="new")

    def add_incomes(self):
        print("Adding incomes.")
        self.tree.insert('', 0)
        
    def titled(title):
        if title == "Incomes":
            return "Revenus"
    
    def save_modification(self):
        if self.tree.modified :
            return askyesno("Sauvegarder ?", "Voulez-vous sauvez les modifications ?")



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