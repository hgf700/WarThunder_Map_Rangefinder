from tkinter import *
from tkinter import ttk
from UsableProgram.ManualScale import Manual
from UsableProgram.read_settings import read_settings


def InGameUI():
    root = Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)

    modeA_M = {"mode": "auto"}

    def close_window():
        root.destroy()

    def mode_changed():
        if mode.get() == "manual":
            manual_setting_button.grid(column=1, row=3)
            modeA_M["mode"] = "manual"
        else:
            manual_setting_button.grid_remove()
            modeA_M["mode"] = "auto"

    def open_scale():
        value = Manual(root)  
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

    scale = StringVar(value=read_settings())
    ttk.Label(mainframe, text="S").grid(column=2, row=0, sticky=W)
    ttk.Entry(mainframe, textvariable=scale, state="readonly", width=10).grid(column=1, row=0, sticky=W)

    meters = StringVar()
    ttk.Label(mainframe, text="M").grid(column=2, row=1, sticky=W)
    ttk.Entry(mainframe, textvariable=meters, state="readonly", width=10).grid(column=1, row=1, sticky=W)

    manual_setting_button = ttk.Button(mainframe, text="Scale", command=open_scale, width=8)

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
    root.mainloop()

    return modeA_M["mode"]
