from tkinter import *
from tkinter import ttk
import os

root = Tk()
root.title("Settings")
root.attributes('-topmost', False)

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
folder_path = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\settings"
os.makedirs(folder_path, exist_ok=True)
file_path = os.path.join(folder_path, "settings.txt")

def save_to_file(width, height, MiniMapStartX,MiniMapStartY,MiniMapEndX,MiniMapEndY):
    with open(file_path, "w") as f:
        f.write(f"{width} {height} {MiniMapStartX} {MiniMapStartY} {MiniMapEndX} {MiniMapEndY}")  

def resolution_changed(*args):
    res = resolution.get()

    res1=[1366, 768,600, 600, 600, 600]
    res2=[1920, 1080,1584, 741, 1904, 1066]
    res3=[2560, 1440,1500,1500,1500,1500]

    if res == "1366x768":
        save_to_file(res1[0],res1[1],res1[2],res1[3],res1[4],res1[5])
    elif res == "1920x1080":
        save_to_file(res2[0],res2[1],res2[2],res2[3],res2[4],res2[5])
    elif res == "2560x1440":
        save_to_file(res3[0],res3[1],res3[2],res3[3],res3[4],res3[5])

def read_settings():
    if not os.path.exists(file_path):
        return None  # brak pliku
    with open(file_path, "r") as f:
        line = f.readline().strip()
        return line
    
settings = read_settings()

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

r2560x1440_button = ttk.Radiobutton(mainframe, text="2560x1440", variable=resolution,
                                    value="2560x1440", command=resolution_changed)
r2560x1440_button.grid(column=1, row=4, sticky=E)

ttk.Label(mainframe, text="Current Resolution").grid(column=1, row=5, sticky=W)
scale_entry = ttk.Entry(mainframe, textvariable=resolution, state="readonly", width=10)
scale_entry.grid(column=1, row=6, sticky=(W))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
