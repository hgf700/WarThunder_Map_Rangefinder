import sys
import os
import threading
from pathlib import Path
from UsableProgram.SettingsUI import SettingsUI
from UsableProgram.InGameUI import InGameUI
from UsableProgram.GenerateBackendMark import GenerateBackendMark
from UsableProgram.UsageOfYolo import UsageOfYolo

# 🔧 Znajdź katalog główny projektu niezależnie od miejsca uruchomienia
base_dir = Path(__file__).resolve().parent
usable_program = base_dir / "UsableProgram"

# 🔧 Ustal ścieżki absolutne
settings_folder = usable_program / "settings"
captures_folder = usable_program / "captures"

settings_folder.mkdir(parents=True, exist_ok=True)
captures_folder.mkdir(parents=True, exist_ok=True)

settings_path = settings_folder / "settings.txt"

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
