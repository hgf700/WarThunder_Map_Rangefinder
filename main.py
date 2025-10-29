from UsableProgram.SettingsUI import start_ui
from UsableProgram.InGameUI import InGameRangeFinder

def main():
    res = start_ui()
    if res:
        print(f"Ustawiono rozdzielczość: {res}")
        ingame=InGameRangeFinder()





    else:
        print("Nie wybrano rozdzielczości")

    








if __name__ == "__main__":
    main()
