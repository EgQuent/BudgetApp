import tkinter as tk
from tkinter import ttk


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

    def on_delete_pressed(self, event):
        selected_id = self.focus()
        self.delete(selected_id)
        if self.update_function:
            self.update_function()

    def on_focus_out(self, event):
        event.widget.destroy()