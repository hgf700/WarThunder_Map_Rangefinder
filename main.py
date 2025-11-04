import sys
# from PyQt5.QtWidgets import QApplication
from UsableProgram.SettingsUI import SettingsUI
from UsableProgram.InGameUI import InGameUI
from UsableProgram.GenerateBackendMark import GenerateBackendMark
from UsableProgram.UsageOfYolo import UsageOfYolo
import os
from pynput import mouse, keyboard
import threading

# Globalny overlay
overlay = None
app = None  # globalna aplikacja

settings = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\settings"
os.makedirs(settings, exist_ok=True)
settings_path = os.path.join(settings, "settings.txt")

label_path = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\captures"
os.makedirs(label_path, exist_ok=True)

def main():
    global overlay, app

    # 1. Uruchom UI ustawień
    res = SettingsUI()
    if not res or res == "error":
        print("Nie wybrano rozdzielczości lub błąd.")
        return

    print(f"Ustawiono rozdzielczość: {res}")

    backend_thread = threading.Thread(
        target=GenerateBackendMark, args=(settings_path, label_path),daemon=True
    )
    backend_thread.start()

    mode = InGameUI()
    
    



    # sys.exit(app.exec_())  # <-- WAŻNE: to uruchamia całą aplikację
if __name__ == "__main__":
    main()