import cv2
import numpy as np
import os

resolution = 1

resoltuion_img_file = fr"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\Resolutions_Photo\res{resolution}"
img_path = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\photo"
match_folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\Find_value_of_px_in_meter\match"
squrae_to_px_folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\Find_value_of_px_in_meter\result"

os.makedirs(resoltuion_img_file, exist_ok=True)
os.makedirs(img_path, exist_ok=True)
os.makedirs(match_folder, exist_ok=True)
os.makedirs(squrae_to_px_folder, exist_ok=True)

squrae_to_px_path = os.path.join(squrae_to_px_folder, "result.txt")

# ścieżki do liter
B_path = os.path.join(resoltuion_img_file, "B.png")
D_path = os.path.join(resoltuion_img_file, "D.png")
F_path = os.path.join(resoltuion_img_file, "F.png")

# wczytanie liter i konwersja do szarości
B_letter = cv2.imread(B_path, cv2.IMREAD_GRAYSCALE)
D_letter = cv2.imread(D_path, cv2.IMREAD_GRAYSCALE)
F_letter = cv2.imread(F_path, cv2.IMREAD_GRAYSCALE)

# wczytanie mapy / screena
capture_path = os.path.join(img_path, "image.png")
capture_img = cv2.imread(capture_path, cv2.IMREAD_GRAYSCALE)

if capture_img is None:
    raise FileNotFoundError(f"Nie znaleziono pliku: {capture_path}")

# dopasowanie liter
Capture_B = cv2.matchTemplate(capture_img, B_letter, cv2.TM_CCOEFF_NORMED)
Capture_D = cv2.matchTemplate(capture_img, D_letter, cv2.TM_CCOEFF_NORMED)
Capture_F = cv2.matchTemplate(capture_img, F_letter, cv2.TM_CCOEFF_NORMED)

# wyciągnięcie najlepszego dopasowania
_, confidence_B, _, location_B = cv2.minMaxLoc(Capture_B)
_, confidence_D, _, location_D = cv2.minMaxLoc(Capture_D)
_, confidence_F, _, location_F = cv2.minMaxLoc(Capture_F)

print(f"B found at: {location_B} with confidence: {confidence_B:.3f}")
print(f"D found at: {location_D} with confidence: {confidence_D:.3f}")
print(f"F found at: {location_F} with confidence: {confidence_F:.3f}")

# pozycje Y
y_B = location_B[1]
y_D = location_D[1]
y_F = location_F[1]

# lista liter z ich pozycjami# pozycje Y i odpowiadające im pozycje siatki (np. odstęp co 2 jednostki)
positions = {
    "B": (y_B, 2),
    "D": (y_D ,4),
    "F": (y_F, 6)
}

centerY = (y_B + y_D + y_F) / 3
print(f"Średnia pozycja Y: {centerY:.2f}")

# usuń literę, która najbardziej odstaje od średniej
outlier = max(positions.items(), key=lambda x: abs(x[1][0] - centerY))[0]
positions.pop(outlier)

# pozostałe dwie litery
(keys, vals) = zip(*positions.items())
(y1, grid1), (y2, grid2) = vals

# oblicz odległość w pikselach przypadającą na 1 kwadrat
pixels_per_square = abs(y1 - y2) / abs(grid1 - grid2)

print(f"\nLitery {keys[0]} i {keys[1]} zostały użyte do obliczenia skali.")
print(f"1 kwadrat = {pixels_per_square:.2f} pikseli")

def save_to_file(pixels_per_square):
    with open(squrae_to_px_path, "w") as f:
        f.write(f"{pixels_per_square}")      
    
save_to_file(pixels_per_square)