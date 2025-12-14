from tkinter import *
from tkinter import ttk
from Program.LogicOfProgram.OCR_A_andTresholdingPhoto import OCR_A_andTresholdingPhoto
from Program.LogicOfProgram.ManualScale import ManualScale
from Program.LogicOfProgram.ReadFromFile import ReadFromFile
from Program.LogicOfProgram.PathToPrograms import scale_path,meters_path
import os
import functools
import threading

mode_selected = None
# mode_event = threading.Event()

print = functools.partial(print, flush=True)

def InGameUI():
    root = Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)

    modeA_M = {"mode": "auto"}

    # global mode_selected

    def close_window():
        # global stop_threads
        # stop_threads = True
        root.destroy()
        os._exit(0)

    def mode_changed():
        if mode.get() == "manual":
            manual_setting_button.grid(column=1, row=3)
            modeA_M["mode"] = "manual"
            auto_setting_button.grid_remove()
            # mode_selected="manual"
            # mode_event.set()
        elif mode.get() == "auto":
            auto_setting_button.grid(column=1, row=3)
            modeA_M["mode"] = "auto"
            manual_setting_button.grid_remove()
            # mode_selected="auto"
            # mode_event.set()
        else:
            modeA_M["mode"] = "error mode"
            # auto_setting_buttontest.grid_remove()
            # mode_selected="error mode"
            # mode_event.set()

    def open_scale():
        value = ManualScale(root)  
        if value:
            scale.set(value)
            print(f"ingameui: {value}")

    def auto_set_scale():
        # OCR_A_TresholdingPhoto()
        value = OCR_A_andTresholdingPhoto()  
        if value:
            scale.set(value)
            print(f"ingameui: {value}")

    def start_move(event):
        root.x = event.x
        root.y = event.y

    def do_move(event):
        x = root.winfo_x() + (event.x - root.x)
        y = root.winfo_y() + (event.y - root.y)
        root.geometry(f"+{x}+{y}")

    def stop_move(event):
        root.x = root.y = None

    style = ttk.Style()
    style.configure("Close.TButton", background="red", foreground="red")

    mainframe = ttk.Frame(root)
    mainframe.grid(column=0, row=0)

    close_button = ttk.Button(mainframe, text="✕", command=close_window, width=2, style="Close.TButton")
    close_button.grid(column=2, row=2, sticky=W)

    scale = StringVar(value=ReadFromFile(scale_path))
    ttk.Label(mainframe, text="S").grid(column=2, row=0, sticky=W)
    ttk.Entry(mainframe, textvariable=scale, state="readonly", width=10).grid(column=1, row=0, sticky=W)

    meters = StringVar(value=ReadFromFile(meters_path))
    ttk.Label(mainframe, text="M").grid(column=2, row=1, sticky=W)
    ttk.Entry(mainframe, textvariable=meters, state="readonly", width=10).grid(column=1, row=1, sticky=W)
    
    #manual button
    manual_setting_button = ttk.Button(mainframe, text="Scale", command=open_scale, width=8)

    #auto scale button
    auto_setting_button = ttk.Button(mainframe, text="Repeat Scale", command=auto_set_scale, width=8)

    mode = StringVar(value="auto")
    auto_button = ttk.Radiobutton(mainframe, text="A", variable=mode, value="auto", command=mode_changed)
    manual_button = ttk.Radiobutton(mainframe, text="M", variable=mode, value="manual", command=mode_changed)
    auto_button.grid(column=1, row=2, sticky=E)
    manual_button.grid(column=1, row=2, sticky=W)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    mainframe.bind("<Button-1>", start_move)
    mainframe.bind("<ButtonRelease-1>", stop_move)
    mainframe.bind("<B1-Motion>", do_move)

    manual_setting_button.grid_remove()

    def refresh_meters():
        last_mtime = None

        def _refresh():
            nonlocal last_mtime
            try:
                if os.path.exists(meters_path):
                    mtime = os.path.getmtime(meters_path)
                    if mtime != last_mtime:
                        new_value = ReadFromFile(meters_path)
                        meters.set(new_value)
                        last_mtime = mtime
                        print(f"[INFO] updated Meters: {new_value}")
                else:
                    print(f"[WARN] file {meters_path} do not exist.")
            except Exception as e:
                print(f"[ERROR] while reading meters: {e}")
            finally:
                root.after(500, _refresh)

        _refresh()

    refresh_meters()
    root.mainloop()

    return modeA_M["mode"]

# InGameUI()