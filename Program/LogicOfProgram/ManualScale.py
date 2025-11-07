from tkinter import *
from tkinter import ttk
import os
from Program.LogicOfProgram.ReadFromFile import ReadFromFile
from Program.LogicOfProgram.PathToPrograms import scale_path

def save_scale(value: str):
    with open(scale_path, "w") as f:
        f.write(value)

def ManualScale(parent=None):
    root = Toplevel(parent) if parent else Tk()
    root.title("Scale")
    root.attributes('-topmost', True)
    root.grab_set()  # blokuje interakcje z oknem głównym, dopóki to nie zostanie zamknięte

    result = StringVar()

    mainframe = ttk.Frame(root, padding=10)
    mainframe.grid(column=0, row=0, sticky="nsew")

    ScaleM_input = StringVar()
    ScaleM_output = StringVar(value=ReadFromFile(scale_path))

    ttk.Label(mainframe, text="Scale").grid(column=0, row=0, sticky=E)
    ttk.Entry(mainframe, textvariable=ScaleM_input, width=10).grid(column=1, row=0, sticky=W)
    ttk.Label(mainframe, text="m").grid(column=2, row=0, sticky=W)

    def ScaleM_put():
        value = ScaleM_input.get().strip()
        if value:
            save_scale(value)
            ScaleM_output.set(value)
            result.set(value)
            root.destroy()  # zamyka okno po kliknięciu „Set”
            print(f"manual scale : {value}")

    ttk.Button(mainframe, text="Set", command=ScaleM_put).grid(column=0, row=1, sticky=E)
    ttk.Label(mainframe, text="Seted").grid(column=1, row=1, sticky=W)
    ttk.Entry(mainframe, textvariable=ScaleM_output, state="readonly", width=10).grid(column=2, row=1, sticky=W)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # Czekaj, aż użytkownik kliknie „Set”
    root.wait_variable(result)

    return result.get()

# ManualScale()