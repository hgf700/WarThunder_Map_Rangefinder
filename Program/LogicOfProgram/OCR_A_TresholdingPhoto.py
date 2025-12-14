import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from Program.LogicOfProgram.Development import writeImage,development
from Program.LogicOfProgram.PathToPrograms import tresholding_folder,prediction_raw_path

# Ścieżki

def OCR_A_TresholdingPhoto():
    if development==1:
        photo = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\Program\photo\image.png"
        image = cv2.imread(str(photo), cv2.IMREAD_GRAYSCALE)
    else:
        image = cv2.imread(prediction_raw_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise FileNotFoundError(f"Nie znaleziono obrazu: {prediction_raw_path}")

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
    if writeImage==1:
        fig, axes = plt.subplots(1, 2, figsize=(10,5))
        axes[0].imshow(image, cmap="gray")
        axes[0].set_title("Oryginalny obraz")
        axes[0].axis("off")

        axes[1].imshow(combined, cmap="gray")
        axes[1].set_title("Progowanie dolnej części")
        axes[1].axis("off")
        plt.show()

    cv2.imwrite(os.path.join(tresholding_folder, f"tresholded.png"), combined)

# OCR_A_TresholdingPhoto()