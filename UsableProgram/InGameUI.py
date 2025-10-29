from tkinter import *
from tkinter import ttk

def InGameRangeFinder():
    root = Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)

    def close_window():
        root.destroy()

    def mode_changed(*args):
        if mode.get() == "manual":
            manual_setting_button.grid(column=1, row=3) 
        else:
            manual_setting_button.grid_remove()  

    def start_move(event):
        root.x = event.x
        root.y = event.y

    def stop_move(event):
        root.x = None
        root.y = None

    def do_move(event):
        deltax = event.x - root.x
        deltay = event.y - root.y
        x = root.winfo_x() + deltax
        y = root.winfo_y() + deltay
        root.geometry(f"+{x}+{y}")

    style = ttk.Style()
    style.configure("Close.TButton", background="red", foreground="red")

    mainframe = ttk.Frame(root)
    mainframe.grid(column=0, row=0)

    close_button = ttk.Button(mainframe, text="✕", command=close_window, width=2, style="Close.TButton")
    close_button.grid(column=2, row=2, sticky=W) 

    scale = StringVar()
    ttk.Label(mainframe, text="S").grid(column=2, row=0, sticky=W)
    scale_entry = ttk.Entry(mainframe, textvariable=scale, state="readonly", width=10)
    scale_entry.grid(column=1, row=0, sticky=(W))

    meters = StringVar()
    ttk.Label(mainframe, text="M").grid(column=2, row=1, sticky=W)
    meters_entry = ttk.Entry(mainframe, textvariable=meters, state="readonly", width=10)
    meters_entry.grid(column=1, row=1, sticky=(W))

    manual_setting_button = ttk.Button(mainframe, text="Scale", command=lambda: None, width=8)

    mode = StringVar(value="auto")
    auto_button = ttk.Radiobutton(mainframe, text="A", variable=mode, value="auto", command=mode_changed)
    manual_button = ttk.Radiobutton(mainframe, text="M", variable=mode, value="manual",command=mode_changed)
    auto_button.grid(column=1, row=2, sticky=E)
    manual_button.grid(column=1, row=2, sticky=W)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(2, weight=1)
    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    mainframe.bind("<Button-1>", start_move)
    mainframe.bind("<ButtonRelease-1>", stop_move)
    mainframe.bind("<B1-Motion>", do_move)

    manual_setting_button.grid_remove()
    root.mainloop()

InGameRangeFinder()