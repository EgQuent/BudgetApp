import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo




if __name__ == '__main__':
    root = tk.Tk()
    root.title('Treeview demo')
    root.geometry('620x200')

    # define columns
    columns = ('first_name', 'last_name', 'email')

    tree = tk.Treeview(root, columns=columns, show='headings')

    # define headings
    tree.heading('first_name', text='First Name')
    tree.heading('last_name', text='Last Name')
    tree.heading('email', text='Email')

    # generate sample data
    contacts = []
    for n in range(1, 5):
        contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))

    # add data to the treeview
    for contact in contacts:
        tree.insert('', tk.END, values=contact)


    # def item_selected(event):
    #     for selected_item in tree.selection():
    #         item = tree.item(selected_item)
    #         record = item['values']
    #         # show a message
    #         showinfo(title='Information', message=','.join(record))


    # tree.bind('<<TreeviewSelect>>', item_selected)

    tree.grid(row=0, column=0, sticky='nsew')


    # run the app
    root.mainloop()