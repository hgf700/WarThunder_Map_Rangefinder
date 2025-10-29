from UsableProgram.SettingsUI import start_ui
from UsableProgram.InGameUI import InGameRangeFinder
from UsableProgram.ManualScale import Manual 

def main():
    res = start_ui()  # <- otwiera pierwsze okno
    if res and res != "error":
        print(f"Ustawiono rozdzielczość: {res}")
        RangeFinder = InGameRangeFinder()  
        if RangeFinder == "manual":
            print("Tryb manualny wybrany")
            scale_value = Manual()
            if scale_value:
                print(f"   ➜ Wczytana skala: {scale_value}")


                
            else:
                print("   ⚠️ Nie znaleziono zapisanej wartości skali.")


        elif RangeFinder == "auto":
            print("Tryb automatyczny wybrany")


        else:
            print("error in RangeFinder function")


    else:
        print("Nie wybrano rozdzielczości lub błąd odczytu.")

if __name__ == "__main__":
    main()
