from tkinter import *
from tkinter import ttk
import os
from Program.LogicOfProgram.ReadFromFile import ReadFromFile
from Program.LogicOfProgram.PathToPrograms import settings_path
from Program.LogicOfProgram.development import development
import functools


print = functools.partial(print, flush=True)


def save_to_file(width, height, MiniMapStartX,MiniMapStartY,MiniMapEndX,MiniMapEndY):
    with open(settings_path, "w") as f:
        f.write(f"{width} {height} {MiniMapStartX} {MiniMapStartY} {MiniMapEndX} {MiniMapEndY}")      

def SettingsUI():
    root = Tk()
    root.title("Settings")
    root.overrideredirect(True)
    root.attributes('-topmost', False)

    result = {"resolution": None}

    mainframe = ttk.Frame(root, padding=10)
    mainframe.grid(column=0, row=0, sticky="nsew")

    # --- Pole tekstowe ---
    something = StringVar()
    ttk.Label(mainframe, text="Something").grid(column=1, row=0, sticky=E)
    ttk.Entry(mainframe, textvariable=something, width=10).grid(column=2, row=0, sticky=W)

    # --- Rozdzielczość ---
    resolution = StringVar()
    ttk.Label(mainframe, text="Resolution").grid(column=1, row=1, sticky=E)

    # --- Plik do zapisu ---
    def resolution_changed(*args):
        res = resolution.get()

        
        res2=[1920, 1080,1584, 741, 1904, 1066]
        res3=[2048, 1152, 1636, 736, 2035, 1138]
        if development==1:
            res1=[1366, 768, 987, 389, 1351, 703]

        if res == "1920x1080":
            save_to_file(res2[0],res2[1],res2[2],res2[3],res2[4],res2[5])
        elif res == "2048x1152":
            save_to_file(res3[0],res3[1],res3[2],res3[3],res3[4],res3[5])
        elif res == "1366x768":
            if development==1:
                save_to_file(res1[0],res1[1],res1[2],res1[3],res1[4],res1[5])
            else:
                print("error settingsui")
        
        result["resolution"] = res
        
    settings = ReadFromFile(settings_path)

    if settings:
        try:
            values = list(map(int, settings.split()))
            resolution.set(f"{values[0]}x{values[1]}")
        except Exception as e:
            print(f"[!] Błąd przy parsowaniu settings.txt: {e}")
            resolution.set("error")
    else:
        print("error or no seted resolution")
        resolution.set("error")

    if development==1:
        r1366x768_button = ttk.Radiobutton(mainframe, text="1366x768", variable=resolution,
                                        value="1366x768", command=resolution_changed)
        r1366x768_button.grid(column=1, row=2, sticky=E)

    r1920x1080_button = ttk.Radiobutton(mainframe, text="1920x1080", variable=resolution,
                                        value="1920x1080", command=resolution_changed)
    r1920x1080_button.grid(column=1, row=3, sticky=E)

    r2048x1152_button = ttk.Radiobutton(mainframe, text="2048x1152", variable=resolution,
                                        value="2048x1152", command=resolution_changed)
    r2048x1152_button.grid(column=1, row=4, sticky=E)

    ttk.Label(mainframe, text="Current Resolution").grid(column=1, row=5, sticky=W)
    scale_entry = ttk.Entry(mainframe, textvariable=resolution, state="readonly", width=10)
    scale_entry.grid(column=1, row=6, sticky=(W))

    def submit():
        result["resolution"] = resolution.get()
        root.destroy()

    Submit_button = ttk.Button(mainframe, text="Submit", command=submit,  style="Close.TButton")
    Submit_button.grid(column=2, row=6, sticky=W) 

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(2, weight=1)
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()
    return result["resolution"]

# SettingsUI()