# to manually meauser pixels in x and y dimension
import cv2
import os

# Wczytaj obraz (np. screenshot minimapy)
# img = cv2.imread(r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\ManagingData\fragments\map_020.png")
# file="daniel_low_resolution1"
# img = cv2.imread(fr"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\photo\{file}.png")
img = cv2.imread(fr"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\Program\photo\image.png")


if img is None:
    print("Nie udało się wczytać obrazu!")
    exit()

scale=1
small_img = cv2.resize(img, (0,0), fx=scale, fy=scale)

image_height, image_width = img.shape[:2]

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # przeskaluj kliknięcie do oryginalnych pikseli
        orig_x = int(x / scale)
        orig_y = int(y / scale)

        x_center = orig_x / image_width
        y_center = orig_y / image_height

        color = img[orig_y, orig_x]
        print(f"Kliknięto w piksel ({orig_x}, {orig_y}), kolor (BGR): {color}")
        print(f"normalised X {x_center:.6f} Y {y_center:.6f}")

cv2.imshow("Mapa", small_img)
cv2.setMouseCallback("Mapa", click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()
