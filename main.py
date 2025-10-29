from UsableProgram.SettingsUI import start_ui
from UsableProgram.InGameUI import InGameRangeFinder

def main():
    res = start_ui()  # <- otwiera pierwsze okno
    if res and res != "error":
        print(f"Ustawiono rozdzielczość: {res}")
        RangeFinder = InGameRangeFinder()  
        if RangeFinder == "manual":
            print("Tryb manualny wybrany")


        elif RangeFinder == "auto":
            print("Tryb automatyczny wybrany")


        else:
            print("error in RangeFinder function")


    else:
        print("Nie wybrano rozdzielczości lub błąd odczytu.")

if __name__ == "__main__":
    main()
