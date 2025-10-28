import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Ścieżki
input_file = "map_100"  # Upewnij się, że to obraz, nie plik .txt
input_folder = fr"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\TrainingData\images\train\{input_file}.png"
output_folder = fr"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\testing\test\image_tresholding"
os.makedirs(output_folder, exist_ok=True)

image = cv2.imread(input_folder, cv2.IMREAD_GRAYSCALE)

if image is None:
    raise FileNotFoundError(f"Nie znaleziono obrazu: {input_folder}")

height = image.shape[0]
width = image.shape[1]

cut_ratio = 0.075  
cut_start = int(height * (1 - cut_ratio))

# Podziel obraz
upper_part = image[:cut_start, :]
lower_part = image[cut_start:, :]

# 🔧 Parametry progowania
lower_thresh = 0   # dolna granica (ciemniejsze piksele)
upper_thresh = 40  # górna granica (jaśniejsze piksele)

# 🔲 Zostaw tylko obszary w tym zakresie kontrastu (czyli tekst)
mask = cv2.inRange(lower_part, lower_thresh, upper_thresh)

# 🧾 Odwrócenie, żeby tekst był czarny na białym tle
result_lower = cv2.bitwise_not(mask)

# Połączenie z górną częścią (niezmienioną)
combined = np.vstack((upper_part, result_lower))

# Wyświetlenie wyników
fig, axes = plt.subplots(1, 2, figsize=(10,5))
axes[0].imshow(image, cmap="gray")
axes[0].set_title("Oryginalny obraz")
axes[0].axis("off")

axes[1].imshow(combined, cmap="gray")
axes[1].set_title("Progowanie dolnej części")
axes[1].axis("off")
plt.show()

# Zapis wyniku
output_path = os.path.join(output_folder, f"tresholded_{input_file}")
cv2.imwrite(output_path, combined)
