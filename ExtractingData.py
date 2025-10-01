import os
import cv2

# folder ze screenshotami
folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\TrainingData\ManagingData"
output_folder = os.path.join(folder, "fragments")
os.makedirs(output_folder, exist_ok=True)

# obszar minimapy w pikselach (x1, y1, x2, y2)
x1, y1, x2, y2 = 1584, 741, 1904, 1066

# opcjonalnie: skala jeśli chcesz zmniejszyć obraz do ekranu laptopa
laptop = False

if laptop:
    scale_x = 1366 / 1920
    scale_y = 768 / 1080
else:
    scale_x = 1
    scale_y = 1

for file in os.listdir(folder):
    if file.endswith(".png"):
        path = os.path.join(folder, file)
        img = cv2.imread(path)
        if img is None:
            print(f"Nie udało się wczytać {file}")
            continue

        # przeliczenie współrzędnych jeśli skala
        left = int(x1 * scale_x)
        top = int(y1 * scale_y)
        width = int((x2 - x1) * scale_x)
        height = int((y2 - y1) * scale_y)

        fragment = img[top:top+height, left:left+width]  # wycięcie fragmentu
        cv2.imshow("fragment", fragment)
        cv2.waitKey(500)  # pokaż na pół sekundy

        # zapis do folderu
        output_path = os.path.join(output_folder, file)
        cv2.imwrite(output_path, fragment)
        print("completed")
    else:
        print("?")

cv2.destroyAllWindows()
