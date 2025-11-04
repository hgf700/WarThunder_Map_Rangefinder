import os
import math
from read_settings import read_settings
# from UsableProgram.read_settings import read_settings

import functools

print = functools.partial(print, flush=True)

prediciton_folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\captures\wyniki"
os.makedirs(prediciton_folder, exist_ok=True)
prediciton_path = os.path.join(prediciton_folder, "prediction.txt")

settings_folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\settings"
os.makedirs(settings_folder, exist_ok=True)
settings_path = os.path.join(settings_folder, "settings.txt")

def load_settings_box():
    parts=read_settings(prediciton_path)
    
    if not parts:   
        print("[!] Brak danych w pliku prediction.txt")
        return


    print(parts)

    cleaned = parts.replace(",", " ").replace("\n", " ").replace("\t", " ")
    parts = [p for p in cleaned.split(" ") if p.strip() != ""]

    parts=parts[:12]
    try:
        # 1 0.87 255 140 285 170 0 0.86 253 17 273 38  
        # mark,Mpred,Mx1,My1,Mx2,My2,player,Ppred,Px1,Py1,Px2,Py2= map(int, parts[:12])

        mark = int(parts[0])
        Mpred = float(parts[1])
        Mx1 = int(parts[2])
        My1 = int(parts[3])
        Mx2 = int(parts[4])
        My2 = int(parts[5])
        player = int(parts[6])
        Ppred = float(parts[7])
        Px1 = int(parts[8])
        Py1 = int(parts[9])
        Px2 = int(parts[10])
        Py2 = int(parts[11])

        Mx=(Mx1+Mx2)/2
        My=(My1+My2)/2
        Px=(Px1+Px2)/2
        Py=(Py1+Py2)/2

        distance = math.hypot(Px - Mx, Py - My)

        print(f"[INFO] Marker: ({Mx}, {My}) | Conf: {Mpred:.2f}")
        print(f"[INFO] Player: ({Px}, {Py}) | Conf: {Ppred:.2f}")
        print(f"[INFO] Odległość: {distance}px")

        return Mx, My, Px, Py, distance

    except ValueError as e:
        print("[!] Błąd przy konwersji wartości:", e)
        return 
        

load_settings_box()