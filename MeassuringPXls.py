# to manually meauser pixels in x and y dimension
import cv2
import os

# Wczytaj obraz (np. screenshot minimapy)
img = cv2.imread(r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\TrainingData\ManagingData\map_001.png")

if img is None:
    print("Nie udało się wczytać obrazu!")
    exit()

scale=0.65
small_img = cv2.resize(img, (0,0), fx=scale, fy=scale)

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # przeskaluj kliknięcie do oryginalnych pikseli
        orig_x = int(x / scale)
        orig_y = int(y / scale)
        color = img[orig_y, orig_x]
        print(f"Kliknięto w piksel ({orig_x}, {orig_y}), kolor (BGR): {color}")

cv2.imshow("Mapa", small_img)
cv2.setMouseCallback("Mapa", click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()
