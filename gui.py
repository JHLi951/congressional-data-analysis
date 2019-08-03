import tkinter as tk
from tkinter import *
import congressional_data


def get_member_info():
    name = "{} {}".format(e1.get(), e2.get())
    # print(name)
    info = congressional_data.get_specific_member(name)
    linfo.config(text=info)

# def on_configure(event):
#     # update scrollregion after starting 'mainloop'
#     # when all widgets are in canvas
#     canvas.configure(scrollregion=canvas.bbox('all'))

m = tk.Tk()
m.title("Congressional Data")

# canvas = tk.Canvas(root)
# canvas.pack(side=tk.LEFT)

# scrollbar = tk.Scrollbar(root, command=canvas.yview)
# scrollbar.pack(side=tk.LEFT, fill='y')
# canvas.configure(yscrollcommand=scrollbar.set)


# canvas.bind('<Configure>', on_configure)

# m = tk.Frame(canvas)
# canvas.create_window((0, 0), window=m, anchor='nw')

ltitle = Label(m, text='Congressional Data Book')
ltitle.grid(row=0, column=1)
lfname = Label(m, text='First Name')
lfname.grid(row=1) 
llname = Label(m, text='Last Name')
llname.grid(row=2) 
e1 = tk.Entry(m) 
e2 = tk.Entry(m) 
e1.grid(row=1, column=2) 
e2.grid(row=2, column=2)

Button(master=m, text='Get Member Info', command=get_member_info).grid(row=3, column=1)
linfo = Label(m, text='Member Info Here', wraplength=500)
linfo.grid(row=4, column=1)




m.mainloop()
