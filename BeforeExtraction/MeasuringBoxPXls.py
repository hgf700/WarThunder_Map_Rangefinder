# saves data from inserted file to .txt file with box cordinates of ping and player
import cv2
import os

file = "map_001"

img = cv2.imread(f"C:\\Users\\USER098\\Documents\\GitHub\\balistic-calculator-WT\\TrainingData\\ManagingData\\podejscie1\\{file}.png")
txtfile = cv2.imread(f"C:\\Users\\USER098\\Documents\\GitHub\\balistic-calculator-WT\\TrainingData\\labels\\train\\{file}.txt")

if img is None:
    print("Nie udało się wczytać obrazu!")
    exit()

scale = 0.65
small_img = cv2.resize(img, (0, 0), fx=scale, fy=scale)

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # przeskaluj kliknięcie do oryginalnych pikseli
        orig_x = int(x / scale)
        orig_y = int(y / scale)

        # wymiary prostokąta
        box_width = 20
        box_height = 20

        # współrzędne w oryginalnym obrazie
        RightDownX = int((x + box_width) / scale)
        RightDownY = int((y + box_height) / scale)

        print(f"Kliknięto w piksel LeftUp ({orig_x}, {orig_y})")
        print(f"RightDown ({RightDownX}, {RightDownY})")        

        # wycinamy fragment z obrazu
        fragment = img[orig_y:RightDownY, orig_x:RightDownX]

        # pokaż wycięty fragment
        cv2.imshow("Fragment", fragment)
        cv2.waitKey(0)
        cv2.destroyWindow("Fragment")

cv2.imshow("Mapa", small_img)
cv2.setMouseCallback("Mapa", click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()
