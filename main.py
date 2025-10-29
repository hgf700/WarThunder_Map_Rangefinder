from UsableProgram.SettingsUI import start_ui
from UsableProgram.InGameUI import InGameRangeFinder
from UsableProgram.ManualScale import Manual 

def main():
    res = start_ui()  # <- otwiera pierwsze okno
    if res and res != "error":
        print(f"Ustawiono rozdzielczość: {res}")
        RangeFinder = InGameRangeFinder()  



    else:
        print("Nie wybrano rozdzielczości lub błąd odczytu.")

if __name__ == "__main__":
    main()
