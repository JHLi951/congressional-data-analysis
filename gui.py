import tkinter as tk
from tkinter import *
import congressional_data
from tkinter import ttk

def get_member_info():
    name = "{} {}".format(e1.get(), e2.get())
    # print(name)
    info = congressional_data.get_specific_member(name)
    tinfo.delete('1.0', END)
    tinfo.insert(INSERT, info)
    tinfo.tag_add('center', '1.0', 'end')

root = tk.Tk()
root.title("Congressional Data")

nb = ttk.Notebook(root)
f1 = Frame(root, width=500, height=500)
f2 = Frame(root, width=500, height=500)
nb.pack()
nb.add(f1, text='Get Member Info')
nb.add(f2, text='Get Member Spending')


ltitle = Label(f1, text='Congressional Data Book')
ltitle.grid(row=0, column=1)
lfname = Label(f1, text='First Name')
lfname.grid(row=1) 
llname = Label(f1, text='Last Name')
llname.grid(row=2) 
e1 = tk.Entry(f1) 
e2 = tk.Entry(f1) 
e1.grid(row=1, column=1) 
e2.grid(row=2, column=1)

get_info_button = Button(master=f1, text='Get Member Info', command=get_member_info)
get_info_button.grid(row=3, column=1)
# linfo = Label(f1, text='Member Info Here', wraplength=500)
# linfo.grid(row=4, column=1)
tinfo = Text(f1)
tinfo.tag_configure('center', justify='center')
tinfo.grid(row=4, column=1)



root.mainloop()
