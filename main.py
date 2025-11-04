# main.py
import sys
from PyQt5.QtWidgets import QApplication
from UsableProgram.SettingsUI import start_ui
from UsableProgram.InGameUI import InGameRangeFinder
from UsableProgram.GenerateBackendMark import GenerateBackendMark

# Globalny overlay
overlay = None
app = None  # globalna aplikacja


def main():
    global overlay, app

    # 1. Uruchom UI ustawień
    res = start_ui()
    if not res or res == "error":
        print("Nie wybrano rozdzielczości lub błąd.")
        return

    print(f"Ustawiono rozdzielczość: {res}")

    # 2. Utwórz aplikację Qt (jeśli jeszcze nie istnieje)
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # 4. Uruchom główny tryb gry
    mode = InGameRangeFinder()  # zakładam, że to zwraca coś lub uruchamia UI

    if(mode =="manual"):
        print("manual")
        generate = GenerateMark()
    
    elif(mode=="auto"):
        print("auto")
        generate = GenerateMark()

    



    # sys.exit(app.exec_())  # <-- WAŻNE: to uruchamia całą aplikację
if __name__ == "__main__":
    main()