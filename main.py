import sys
from UsableProgram.SettingsUI import SettingsUI
from UsableProgram.InGameUI import InGameUI
from UsableProgram.GenerateBackendMark import GenerateBackendMark
from UsableProgram.UsageOfYolo import UsageOfYolo
import os
from pynput import mouse, keyboard
import threading
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
usable_program = base_dir / "UsableProgram"

settings_folder = usable_program / "settings" 
settings_folder.mkdir(parents=True, exist_ok=True)
settings_path = settings_folder / "settings.txt"

label_path = usable_program / "captures" 
label_path.mkdir(parents=True, exist_ok=True)

# Globalny overlay
overlay = None
app = None  # globalna aplikacja


def when_capture_ready(number):
    print(f"[YOLO] Uruchamiam detekcję dla {number}")
    UsageOfYolo()

def main():
    global overlay, app

    # 1. Uruchom UI ustawień
    res = SettingsUI()
    if not res or res == "error":
        print("Nie wybrano rozdzielczości lub błąd.")
        return

    print(f"Ustawiono rozdzielczość: {res}")

    backend_thread = threading.Thread(
        target=GenerateBackendMark, args=(settings_path, label_path,when_capture_ready),daemon=True
    )
    backend_thread.start()

    print("Otwieram InGameUI()...")
    InGameUI()
    print("Zamknąłem InGameUI()")
    

if __name__ == "__main__":
    main()