from tkinter import *
from tkinter import ttk
import os

def Manual():
    root = Tk()
    root.title("Scale")
    root.attributes('-topmost', False)

    ManualScale = {"scale": None}

    mainframe = ttk.Frame(root, padding=10)
    mainframe.grid(column=0, row=0, sticky="nsew")

    # Dwie zmienne – jedna do wpisywania, druga tylko do odczytu
    ScaleM_input = StringVar()
    ScaleM_output = StringVar()

    ttk.Label(mainframe, text="Scale").grid(column=0, row=0, sticky=E)
    ttk.Entry(mainframe, textvariable=ScaleM_input, width=10).grid(column=1, row=0, sticky=W)
    ttk.Label(mainframe, text="m").grid(column=2, row=0, sticky=W)

    def ScaleM_put():
        value = ScaleM_input.get()
        ScaleM_output.set(f"{value}")
        ManualScale["scale"] 

    ttk.Button(mainframe, text="Set", command=ScaleM_put).grid(column=0, row=1, sticky=E)

    ttk.Label(mainframe, text="Seted").grid(column=1, row=1, sticky=W)
    scale_entry = ttk.Entry(mainframe, textvariable=ScaleM_output, state="readonly", width=10)
    scale_entry.grid(column=2, row=1, sticky=(W))

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(2, weight=1)
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()
    return ManualScale["scale"] 

# Manual()