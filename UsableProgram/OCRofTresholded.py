import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pytesseract

# 🔧 Ścieżki
input_file = "map_100"
input_folder = fr"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\TrainingData\images\train\{input_file}.png"
output_folder = fr"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\testing\test\image_tresholding\OCR"
os.makedirs(output_folder, exist_ok=True)

# 🔧 Jeśli Tesseract nie jest w PATH:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 📷 Wczytaj obraz w skali szarości
image = cv2.imread(input_folder, cv2.IMREAD_GRAYSCALE)
if image is None:
    raise FileNotFoundError(f"Nie znaleziono obrazu: {input_folder}")

height, width = image.shape
cut_ratio_h = 0.075  
cut_ratio_w = 0.4

cut_start_h = int(height * (1 - cut_ratio_h))
cut_start_w = int(width * (1 - cut_ratio_w))

roi = image[cut_start_h:, cut_start_w:] 

# height, width = image.shape
# cut_ratio = 0.075  
# cut_start = int(height * (1 - cut_ratio))

# # 🔪 Wytnij dolną część obrazu
# upper_part = image[:cut_start, :]
# lower_part = image[cut_start:, :]

# ⚙️ Progowanie kontrastowe
lower_thresh = 0
upper_thresh = 40
mask = cv2.inRange(roi, lower_thresh, upper_thresh)

# 🔄 Odwrócenie (czarny tekst na białym tle)
processed = cv2.bitwise_not(mask)

# 💡 Drobne czyszczenie i skalowanie
processed = cv2.GaussianBlur(processed, (3,3), 0)
processed = cv2.resize(processed, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# 🔤 OCR
config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789mM'
text = pytesseract.image_to_string(processed, config=config, lang='eng')

print("Rozpoznany tekst:")
print(text)

# 💾 Zapis tekstu
base_name = os.path.splitext(input_file)[0]
txt_path = os.path.join(output_folder, f"{base_name}.txt")
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Wynik OCR zapisany w: {txt_path}")

# 🖼️ Opcjonalnie pokaż wynikowy obraz
plt.imshow(processed, cmap='gray')
plt.axis('off')
plt.show()
