#adding to random positions special mark to detection
import cv2
import os
import random

# Folder z obrazami
input_folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\TrainingData\ManagingData\czysteZdj"
output_folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\TrainingData\ManagingData\edytowaneZdj"
os.makedirs(output_folder, exist_ok=True)

# Pozycja kółka (np. x=100, y=200 w pikselach)



for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        path = os.path.join(input_folder, filename)
        img = cv2.imread(path)

        if img is None:
            print(f"Nie udało się wczytać {filename}")
            continue

        numX = random.randint(1584,1904)
        numY = random.randint(741,1066)
        
        circle_pos = (numX, numY)

        radius1 =8
        radius2=6
        color1 = (0, 165, 255) #orange
        color2 = (39,250,00)#green
        alpha = 0.4

        overlay = img.copy()

        # Narysuj kółko
        cv2.circle(img, circle_pos, radius1, color1, 2)
        cv2.circle(img, circle_pos, radius2, color2, 2)

        img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        # Zapisz nowy obraz
        cv2.imwrite(os.path.join(output_folder, filename), img)

print("✅ Gotowe! Wszystkie obrazy zapisane.")
