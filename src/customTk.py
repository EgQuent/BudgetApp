import tkinter as tk
from tkinter import ttk
from tools import get_string_amount, make_df
from tkinter.simpledialog import Dialog

class ChoiceMessage(Dialog):

    def __init__(self, parent, choices: list, answer: tk.StringVar = None):
        self.choices = choices
        self.answer = answer
        super().__init__(parent)
    
    def body(self, _):
        box = tk.Frame(self)

        for choice in self.choices:
            tk.Radiobutton(box, text=str(choice), variable=self.answer, value=choice).pack(anchor = tk.W)
        box.pack()


class AmountVar(tk.StringVar):

    def __init__(self, parent, value, *args, **kwargs):
        super().__init__(parent, '', *args, **kwargs)
        self.value = self.get_string(value)
        
    def set(self, value):
        super().set(self.get_string(value))
        
    @staticmethod
    def get_string(value):
        if isinstance(value, (int, float)):
            return get_string_amount(value)
        return value


class BetterLabel(tk.Frame):

    def __init__(self, parent, front_text: str, dynamic_text: tk.StringVar, end_text: str = None):
        super().__init__(parent)

        self.columnconfigure(0, weight=3, uniform='b')
        self.columnconfigure(1, weight=3, uniform='b')
        self.columnconfigure(2, weight=1, uniform='b')
        self.rowconfigure(0, weight=1, uniform='c')

        tk.Label(self, text=front_text).grid(row=0, column=0, sticky="nse")
        tk.Label(self, textvariable=dynamic_text).grid(row=0, column=1, sticky="nsew")
        tk.Label(self, text=end_text).grid(row=0, column=2, sticky="nsew")


class TreeviewEdit(ttk.Treeview):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.update_function = None
        self.bind("<Double-Button-1>", self.on_double_click)
        self.bind("<Delete>", self.on_delete_pressed)

    def set_update_function(self, update_function):
        self.update_function = update_function

    def insert(self, *args, **kwargs):
        if self.update_function:
            self.update_function()
        return super().insert(*args, **kwargs)

    def on_double_click(self, event):
        region_clicked = self.identify_region(event.x, event.y)
        if region_clicked not in ("tree", "cell"):
            return None
        
        column = self.identify_column(event.x)
        selected_id =self.focus()
        self.create_editable_cell(column, selected_id)

    def create_editable_cell(self, column, selected_id):
        column_box = self.bbox(selected_id, column=column)
        
        selected_values = self.item(selected_id)
        if column =='#0':
            selected_text = selected_values.get("text")
        else:
            column_index = int(column[1:])-1
            selected_text = selected_values.get('values')[column_index]
    
        entry_edit = ttk.Entry(self.parent, width=column_box[2])
        entry_edit.place (x=column_box[0], y=column_box[1],
                          width=column_box[2], height=column_box[3])
        entry_edit.insert(0, selected_text)
        entry_edit.select_range(0, tk.END)

        entry_edit.editing_column_index = column_index
        entry_edit.editing_item_id = selected_id
        
        entry_edit.focus()
        entry_edit.bind("<FocusOut>", self.on_focus_out)
        entry_edit.bind("<Return>", self.on_enter_pressed)
        entry_edit.bind("<Tab>", self.on_tab_pressed)

    def on_tab_pressed(self, event):
        self.on_enter_pressed(event)
        nbCols = len(self.item(event.widget.editing_item_id).get("values")) + 1
        trgCol = event.widget.editing_column_index + 1 + 1
        if  trgCol >= nbCols :
            event.widget.destroy()
            return None

        column = '#' + str(trgCol)
        self.create_editable_cell(column, event.widget.editing_item_id)

    def on_enter_pressed(self, event):
        new_text = event.widget.get()
        selected_id = event.widget.editing_item_id
        column_index = event.widget.editing_column_index

        if column_index == -1:
            self.item(selected_id, text=new_text)
        else :
            current_values = self.item(selected_id).get("values")
            current_values[column_index] = new_text
            self.item(selected_id, values=current_values)
        if self.update_function:
            self.update_function()
        event.widget.destroy()

    def on_delete_pressed(self, event = None):
        selected_id = self.focus()
        if isinstance(selected_id, str):
            if len(selected_id) == 4:
                if selected_id[0] == 'I':
                    self.delete(selected_id)
                    if self.update_function:
                        self.update_function()

    def on_focus_out(self, event):
        event.widget.destroy()

class PopUpTreeview(TreeviewEdit):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.choices = None
        self.target_col = None

    def set_choices(self, choices: list, target_col: int):
        self.choices = choices
        self.target_col = "".join(['#', str(target_col)])

    def on_double_click(self, event):
        region_clicked = self.identify_region(event.x, event.y)
        if region_clicked not in ("tree", "cell"):
            return None
        
        column = self.identify_column(event.x)
        selected_id =self.focus()
        if column == self.target_col:
            self.create_pop_up(column, selected_id)
        else :
            self.create_editable_cell(column, selected_id)

    def on_tab_pressed(self, event):
        self.on_enter_pressed(event)
        nbCols = len(self.item(event.widget.editing_item_id).get("values")) + 1
        trgCol = event.widget.editing_column_index + 1 + 1
        if  trgCol >= nbCols :
            event.widget.destroy()
            return None
        column = '#' + str(trgCol)
        if column == self.target_col:
            self.create_pop_up(column, event.widget.editing_item_id)
        else :
            self.create_editable_cell(column, event.widget.editing_item_id)

    def create_pop_up(self, column, selected_id):
        answer = tk.StringVar()
        ChoiceMessage(self, self.choices, answer)
        if not answer.get() == '':
            self.on_ok_click(answer.get(), column, selected_id)

    def on_ok_click(self, new_text, column, selected_id):
        column_index = int(column[1:])-1
        if column_index == -1:
            self.item(selected_id, text=new_text)
        else :
            current_values = self.item(selected_id).get("values")
            current_values[column_index] = new_text
            self.item(selected_id, values=current_values)
        if self.update_function:
            self.update_function()

class BetterTreeView(PopUpTreeview):

    def __init__(self, parent, rows, *args, **kwargs):
        self.frame = ttk.Frame(parent)
        super().__init__(self.frame, *args, **kwargs)
        self._load(rows)

    def grid(self, *args, **kwargs):
       self.frame.grid(*args, **kwargs)

    def add(self):
        empty_list = [''] * len(self['columns'])
        self.insert('', 0, values=empty_list)

    def _add(self):
        self.add()

    def _load(self, rows):
        self.frame.columnconfigure(0, weight=18, uniform='bb')
        self.frame.columnconfigure(1, weight=1, uniform='bb')
        self.frame.rowconfigure(0, weight=1, uniform='cc')

        for column in self['columns']:
            self.heading(column, text=column)
            self.column(column, width=50)
        for row in rows:
            self.insert('', tk.END, values=row)
        self.modified = False
        super().grid(row=0, column=0, sticky="nsew")
    
        # Add buttons frame
        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.grid(row=0,column=1,sticky="nsew")

        # Add button new line
        add_button = ttk.Button(buttons_frame, text='+', command= self._add)
        add_button.pack(fill='x', expand=False)

        # Add delete button
        add_button = ttk.Button(buttons_frame, text='-', command= self.on_delete_pressed)
        add_button.pack(fill='x', expand=False)

class PandasTreeView(BetterTreeView):

    def __init__(self, parent, dataframe, *args, **kwargs):
        columns = list(dataframe.columns)
        if 'Date' in columns :
            dataframe.sort_values(by='Date', ascending = False, inplace = True)
        rows = dataframe.to_numpy().tolist()
        super().__init__(parent, rows, *args, columns=columns, **kwargs)

    def get_dataframe(self):
        headings = self['columns']
        rows =[]
        for row_id in self.get_children():
            rows.append(self.item(row_id)['values'])
        return make_df(headings, rows)