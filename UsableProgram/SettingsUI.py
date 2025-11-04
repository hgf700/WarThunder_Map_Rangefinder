from tkinter import *
from tkinter import ttk
import os
from UsableProgram.read_settings import read_settings

folder_path = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\settings"
os.makedirs(folder_path, exist_ok=True)
file_path = os.path.join(folder_path, "settings.txt")

def save_to_file(width, height, MiniMapStartX,MiniMapStartY,MiniMapEndX,MiniMapEndY):
    with open(file_path, "w") as f:
        f.write(f"{width} {height} {MiniMapStartX} {MiniMapStartY} {MiniMapEndX} {MiniMapEndY}")      
    
def start_ui():
    root = Tk()
    root.title("Settings")
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

        res1=[1366, 768, 800, 500, 1366, 768]
        res2=[1920, 1080,1584, 741, 1904, 1066]
        res3=[2048, 1152, 1636, 736, 2035, 1138]

        if res == "1366x768":
            save_to_file(res1[0],res1[1],res1[2],res1[3],res1[4],res1[5])
        elif res == "1920x1080":
            save_to_file(res2[0],res2[1],res2[2],res2[3],res2[4],res2[5])
        elif res == "2048x1152":
            save_to_file(res3[0],res3[1],res3[2],res3[3],res3[4],res3[5])
        
        result["resolution"] = res
        
    settings = read_settings(file_path)

    if settings:
        values = list(map(int, settings.split()))
        resolution.set(f"{values[0]}x{values[1]}")
    else:
        print("error or no seted resolution")
        resolution.set("error")

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

# start_ui()