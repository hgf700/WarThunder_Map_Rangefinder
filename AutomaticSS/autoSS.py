import cv2
import numpy as np
import pyautogui
import time
import os

# 📁 Foldery na zrzuty i wzorce
output_folder = "C:/Screenshots"
os.makedirs(output_folder, exist_ok=True)

template_folder = "C:/Templates"
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

# ⚙️ Ustawienia
threshold = 0.8      # próg dopasowania (0–1)
count = 0
max_shots = 970
interval = 5         # odstęp po wykryciu (sekundy)
region = (1584, 741, 1904, 1066)  # (x, y, szerokość, wysokość)

while count < max_shots:
    # 🎮 Pobierz zrzut określonego fragmentu ekranu (np. minimapy)
    screenshot = pyautogui.screenshot(region=region)
    frame = np.array(screenshot)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 🔍 Wykryj którykolwiek wzorzec
    for name, template in templates:
        res = cv2.matchTemplate(frame_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        # 📸 Jeśli wzorzec znaleziony
        if len(loc[0]) > 0 and count <= max_shots:
            filename = os.path.join(output_folder, f"detected_{count:04d}.png")
            screenshot.save(filename)
            print(f"ilosc {count}")
            count += 1
            time.sleep(interval)  # pauza po wykryciu
            break  # przejdź do następnej iteracji pętli głównej

    # 🔁 Krótka przerwa między sprawdzeniami
    time.sleep(1)