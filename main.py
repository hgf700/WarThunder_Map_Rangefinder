import sys
import os
import threading
from Program.LogicOfProgram.SettingsUI import SettingsUI
from Program.LogicOfProgram.InGameUI import InGameUI
from Program.LogicOfProgram.GenerateBackendMark import GenerateBackendMark
from Program.LogicOfProgram.UsageOfYolo import UsageOfYolo
from Program.LogicOfProgram.CalculateMetersPerPX import CalculateMetersPerPX
from Program.LogicOfProgram.PathToPrograms import settings_path, prediction_raw_path

# 🌐 Globalne zmienne
overlay = None
app = None  # globalna aplikacja

def when_capture_ready(number):
    print(f"[YOLO] Uruchamiam detekcję dla {number}")
    UsageOfYolo()

def main():
    global overlay, app

    res = SettingsUI()
    if not res or res == "error":
        print("Nie wybrano rozdzielczości lub błąd.")
        return

    print(f"Ustawiono rozdzielczość: {res}")

    backend_thread = threading.Thread(
        target=GenerateBackendMark,
        args=(settings_path, prediction_raw_path, when_capture_ready),
        daemon=True
    )
    backend_thread.start()

    print("[DEBUG] Uruchamiam InGameUI w osobnym wątku.")
    meterperPX_thread = threading.Thread(
        target=CalculateMetersPerPX,
        args=(res,),  # <- poprawka tutaj
        daemon=True
    )
    meterperPX_thread.start()
    print("[DEBUG] Przechodzę do CalculateMetersPerPX...")

    InGameUI()


if __name__ == "__main__":
    main()
