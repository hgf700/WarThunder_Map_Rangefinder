import sys
import os
import threading
from Program.LogicOfProgram.SettingsUI import SettingsUI
from Program.LogicOfProgram.InGameUI import InGameUI
from Program.LogicOfProgram.GenerateBackendMark import GenerateBackendMark
from Program.LogicOfProgram.UsageOfYolo import UsageOfYolo
from Program.LogicOfProgram.PathToPrograms import settings_path
from Program.LogicOfProgram.PathToPrograms import captures_folder

# 🌐 Globalne zmienne
overlay = None
app = None  # globalna aplikacja

def when_capture_ready(number):
    print(f"[YOLO] Uruchamiam detekcję dla {number}")
    UsageOfYolo()

def main():
    global overlay, app

    # 1️⃣ Uruchom UI ustawień
    res = SettingsUI()
    if not res or res == "error":
        print("Nie wybrano rozdzielczości lub błąd.")
        return

    print(f"Ustawiono rozdzielczość: {res}")

    # 2️⃣ Uruchom backend do generowania markerów
    backend_thread = threading.Thread(
        target=GenerateBackendMark,
        args=(settings_path, captures_folder, when_capture_ready),
        daemon=True
    )
    backend_thread.start()

    # 3️⃣ Uruchom interfejs gry
    print("Otwieram InGameUI()...")
    InGameUI()
    print("Zamknąłem InGameUI()")


if __name__ == "__main__":
    main()
