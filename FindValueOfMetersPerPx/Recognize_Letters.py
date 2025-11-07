import cv2
import numpy as np
import os

resolution = 1

resoltuion_img_file = fr"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\Resolutions_Photo\res{resolution}"
img_path = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\photo"
match_folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\Find_value_of_meters_in_px\match"

os.makedirs(resoltuion_img_file, exist_ok=True)
os.makedirs(img_path, exist_ok=True)
os.makedirs(match_folder, exist_ok=True)

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
_, max_val_B, _, max_loc_B = cv2.minMaxLoc(Capture_B)
_, max_val_D, _, max_loc_D = cv2.minMaxLoc(Capture_D)
_, max_val_F, _, max_loc_F = cv2.minMaxLoc(Capture_F)

print(f"B found at: {max_loc_B} with confidence: {max_val_B:.3f}")
print(f"D found at: {max_loc_D} with confidence: {max_val_D:.3f}")
print(f"F found at: {max_loc_F} with confidence: {max_val_F:.3f}")

# konwersja na BGR do kolorowych ramek
output_img = cv2.cvtColor(capture_img, cv2.COLOR_GRAY2BGR)

# narysuj prostokąty dla każdej litery
for (loc, letter, color, label) in [
    (max_loc_B, B_letter, (0, 255, 0), 'B'),
    (max_loc_D, D_letter, (255, 0, 0), 'D'),
    (max_loc_F, F_letter, (0, 0, 255), 'F')
]:
    h, w = letter.shape
    top_left = loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(output_img, top_left, bottom_right, color, 2)
    cv2.putText(output_img, label, (top_left[0], top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

# zapis wyniku
output_path = os.path.join(match_folder, "letters_detected.png")
cv2.imwrite(output_path, output_img)

print(f"\n✅ Obramowania zapisane w pliku: {output_path}")
