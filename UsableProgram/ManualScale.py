from tkinter import *
from tkinter import ttk
import os

folder_path = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\scale"
os.makedirs(folder_path, exist_ok=True)
file_path = os.path.join(folder_path, "scale.txt")

def read_scale() -> str:
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read().strip()

def save_scale(value: str):
    with open(file_path, "w") as f:
        f.write(value)

def Manual(parent=None):
    root = Toplevel(parent) if parent else Tk()
    root.title("Scale")
    root.attributes('-topmost', False)
    root.grab_set()

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
        ScaleM_output.set(value)
        ManualScale["scale"] = value
        save_scale(value)
        print(value)
        return ManualScale["scale"]

    ttk.Button(mainframe, text="Set", command=ScaleM_put).grid(column=0, row=1, sticky=E)

    ttk.Label(mainframe, text="Seted").grid(column=1, row=1, sticky=W)
    scale_entry = ttk.Entry(mainframe, textvariable=ScaleM_output, state="readonly", width=10)
    scale_entry.grid(column=2, row=1, sticky=(W))

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(2, weight=1)
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    if not parent:
        root.mainloop()
        
    return ManualScale["scale"]     


# Manual()