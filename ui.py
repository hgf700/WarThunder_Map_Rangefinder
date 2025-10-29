from tkinter import *
from tkinter import ttk
from ocr_module import run_ocr
from yolo_module import run_yolo
from settings import save_settings

def start_ui(settings):
    root = Tk()
    root.title("Analyzer")
    root.geometry("350x250+600+300")
    root.attributes('-topmost', False)

    mainframe = ttk.Frame(root, padding=10)
    mainframe.grid(column=0, row=0, sticky="nsew")

    # --- Dane z ustawień ---
    res_text = StringVar(value=f"{settings['width']}x{settings['height']}" if settings else "Brak danych")

    # --- Pole wyników ---
    result_text = StringVar(value="Oczekiwanie na analizę...")

    # --- Przyciski ---
    def analyze():
        # wykonaj analizę tylko na żądanie użytkownika
        yolo_result = run_yolo()
        ocr_result = run_ocr()
        result_text.set(f"YOLO: {yolo_result}\nOCR: {ocr_result}")

    def save_example():
        # przykładowe zapisanie ustawień
        save_settings(1920, 1080, 1584, 741, 1904, 1066)
        res_text.set("1920x1080 (zapisano)")

    ttk.Label(mainframe, text="Current Resolution:").grid(column=0, row=0, sticky=W)
    ttk.Entry(mainframe, textvariable=res_text, state="readonly", width=20).grid(column=1, row=0, sticky=W)

    ttk.Button(mainframe, text="Analyze", command=analyze).grid(column=0, row=1, pady=10)
    ttk.Button(mainframe, text="Save Settings", command=save_example).grid(column=1, row=1, pady=10)

    ttk.Label(mainframe, text="Results:").grid(column=0, row=2, sticky=W)
    ttk.Entry(mainframe, textvariable=result_text, state="readonly", width=40).grid(column=0, row=3, columnspan=2, pady=5)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(1, weight=1)

    root.mainloop()
