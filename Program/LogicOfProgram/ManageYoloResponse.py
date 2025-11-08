import os
import math
from Program.LogicOfProgram.ReadFromFile import ReadFromFile
from Program.LogicOfProgram.PathToPrograms import prediction_path,settings_path,scale_path,meters_path,MetersPerPx_path
import functools

print = functools.partial(print, flush=True)

def ManageYoloResponse():
    parts=ReadFromFile(prediction_path)
    
    if not parts:   
        print("[!] Brak danych w pliku prediction.txt")
        return
    
    def save_to_file_meters(meters):
        with open(meters_path, "w") as f:
            f.write(f"{meters}")
    
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

        #pitagoras
        distance = math.hypot(Px - Mx, Py - My)

        print(f"[INFO] Marker: ({Mx}, {My}) | Conf: {Mpred:.2f}")
        print(f"[INFO] Player: ({Px}, {Py}) | Conf: {Ppred:.2f}")
        print(f"[INFO] Odległość: {distance}px")

        resolution =ReadFromFile(settings_path)
        parts2 = [int(x) for x in resolution.split()]

        width, height = parts2[0], parts2[1]

        MetersPerPx=int(ReadFromFile(MetersPerPx_path))

        print(f"width {width}")
        print(f"height {height}")
        print(f"MetersPerPx {MetersPerPx}")

        # distance – odległość w pikselach (np. wynik np.hypot)
        # line – długość odcinka między literami A i E w pikselach
        # scale – wartość w metrach odpowiadająca temu odcinkowi (np. 400 m)
         # przeliczenie pikseli na metry

        distance_m = distance * MetersPerPx

        distance_m = int(distance_m)             # zaokrąglenie do liczby całkowitej


        print(f"[INFO] 1px = {MetersPerPx:.4f} m")
        print(f"[INFO] Odległość w metrach: {distance_m} m")

        save_to_file_meters(distance_m)

        return distance_m

    except ValueError as e:
        print("[!] Błąd przy konwersji wartości:", e)
        return 
        
# ManageYoloResponse()