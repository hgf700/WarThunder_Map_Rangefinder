from tkinter import *
from tkinter import ttk

root = Tk()

mainframe = ttk.Frame(root, padding=(1,1,1,1))
mainframe.grid(column=0, row=0)

scale = StringVar()
ttk.Label(mainframe, text="S").grid(column=2, row=0, sticky=E)
scale_entry = ttk.Entry(mainframe, textvariable=scale, state="readonly", width=10)
scale_entry.grid(column=1, row=0, sticky=(W))

meters = StringVar()
ttk.Label(mainframe, text="M").grid(column=2, row=1, sticky=E)
meters_entry = ttk.Entry(mainframe, textvariable=meters, state="readonly", width=10)
meters_entry.grid(column=1, row=1, sticky=(W))

something = StringVar()
def asd():
    try:
        something.set("0")
    except ValueError:
        pass

def mode_changed(*args):
    if mode.get() == "manual":
        manual_setting_button = ttk.Button(mainframe, text="Scale", command=asd)
        manual_setting_button.grid(column=0, row=2)
    else:
        manual_setting_button.grid_remove()

mode = StringVar(value="auto")
auto_button = ttk.Radiobutton(mainframe, text="A", variable=mode, value="auto", command=mode_changed)
manual_button = ttk.Radiobutton(mainframe, text="M", variable=mode, value="manual",command=mode_changed)
auto_button.grid(column=1, row=2, sticky=E)
manual_button.grid(column=2, row=2, sticky=W)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()