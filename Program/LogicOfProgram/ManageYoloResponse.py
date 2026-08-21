import os
import functools
import math
from Program.LogicOfProgram.ReadFromFile import ReadFromFile
from Program.LogicOfProgram.PathToPrograms import (
    prediction_path,
    settings_path,
    scale_path,
    meters_path,
    PxPerMapSquare_path
)
from Program.LogicOfProgram.logger import setup_logger

logger = setup_logger(__name__)

print = functools.partial(print, flush=True)

def save_to_file_meters(meters):
    with open(meters_path, "w") as f:
        f.write(f"{meters}")

def ManageYoloResponse():
    parts=ReadFromFile(prediction_path)
    
    if not parts:   
        logger.debug(f"no data in file prediction.txt")
        print("[!] no data in file prediction.txt")
        return    
    
    cleaned = parts.replace(",", " ").replace("\n", " ").replace("\t", " ")
    parts = [p for p in cleaned.split(" ") if p.strip() != ""]

    parts=parts[:12]

    EXPECTED_LEN=12

    if len(parts) != EXPECTED_LEN:
        print(f"YOLO detection incomplete: expected {EXPECTED_LEN}, got {len(parts)}")
        logger.error(f"YOLO detection incomplete: expected {EXPECTED_LEN}, got {len(parts)}")

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

        #pitagoras function
        distance = math.hypot(Px - Mx, Py - My)
        print(f"[INFO] Marker: ({Mx}, {My}) | Conf: {Mpred:.2f}")
        print(f"[INFO] Player: ({Px}, {Py}) | Conf: {Ppred:.2f}")
        print(f"[INFO] distance: {distance}px")
        
        logger.debug(f"(0) Marker: ({Mx}, {My}) | Conf: {Mpred:.2f} (1) Player: ({Px}, {Py}) | Conf: {Ppred:.2f} distance: {distance}px")

        resolution =ReadFromFile(settings_path)
        parts2 = [int(x) for x in resolution.split()]

        width, height = parts2[0], parts2[1]

        scale=float(ReadFromFile(scale_path))
        PxPerMap=int(ReadFromFile(PxPerMapSquare_path))

        print(f"width {width}")
        print(f"height {height}")
        print(f"MetersPerPx {PxPerMap}")

        # distance – odległość w pikselach (np. wynik np.hypot)
        # line – długość odcinka między literami A i E w pikselach
        # scale – wartość w metrach odpowiadająca temu odcinkowi (np. 400 m)
        # przeliczenie pikseli na metry

        distance_m = (distance / PxPerMap) * scale
        # zaokrąglenie do liczby całkowitej
        distance_m = int(distance_m)             

        print(f"[INFO] 1 map square = {PxPerMap} m")
        print(f"[INFO] distance in meters: {distance_m} m")
        
        logger.debug(f"1 map square = {PxPerMap} m | distance in meters: {distance_m} m")
        save_to_file_meters(distance_m)

        return distance_m

    except ValueError as e:
        print("[!] error while converting values:", e)
        logger.debug(f"error while converting values")
        return 
        
# ManageYoloResponse()