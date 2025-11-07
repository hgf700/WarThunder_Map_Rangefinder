import cv2
import numpy as np
from mss import mss
import time
import os

output_folder = "D:/AAAA_MojeDaneWT/output"
os.makedirs(output_folder, exist_ok=True)

template_folder = "D:/AAAA_MojeDaneWT/nowetest"
os.makedirs(template_folder, exist_ok=True)

# 📸 Wczytaj wszystkie pliki wzorców
templates = []
for file in os.listdir(template_folder):
    if file.lower().endswith(".png"):
        path = os.path.join(template_folder, file)
        template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if template is not None:
            templates.append((file, template))

if not templates:
    raise FileNotFoundError("Nie znaleziono żadnych plików PNG w folderze Templates!")

# próg dopasowania threshold = 0.2 (0–1)
#slabo treshold dziala na 0.4 na mapie nie z podeslanych danych
threshold = 0.2
count = 0
max_shots = 970
interval = 5         
monitor = {"top": 741, "left": 1584, "width": 320, "height": 325}

sct = mss()

while count < max_shots:
    screenshot = sct.grab(monitor)
    frame = np.array(screenshot)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

    # 🔍 Wykryj którykolwiek wzorzec
    for name, template in templates:
        res = cv2.matchTemplate(frame_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        # 📸 Jeśli wzorzec znaleziony
        if len(loc[0]) > 0 and count <= max_shots:
            filename = os.path.join(output_folder, f"detected_{count:04d}.png")
            cv2.imwrite(filename, frame)
            print(f"ilosc {count}")
            count += 1
            time.sleep(interval)  
            break  

    time.sleep(1)
    print("sleep")