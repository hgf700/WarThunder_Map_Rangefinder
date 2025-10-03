import cv2
import os

file = "map_001"
img_path = f"C:\\Users\\USER098\\Documents\\GitHub\\balistic-calculator-WT\\ManagingData\\fragments\\{file}.png"
label_folder = f"C:\\Users\\USER098\\Documents\\GitHub\\balistic-calculator-WT\\ManagingData\\labels"
os.makedirs(label_folder, exist_ok=True)
label_path = os.path.join(label_folder, f"{file}.txt")

img = cv2.imread(img_path)

if img is None:
    print("Nie udało się wczytać obrazu!")
    exit()

scale = 1
small_img = cv2.resize(img, (0, 0), fx=scale, fy=scale)

# wymiary całej minimapy
image_height, image_width = img.shape[:2]

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # przeskaluj kliknięcie jeśli obraz został zmniejszony
        orig_x = int(x / scale)
        orig_y = int(y / scale)

        # YOLO box
        obj_width = 30
        obj_height = 30

        # fragment do podglądu o tych samych wymiarach co YOLO box
        x1 = max(orig_x - obj_width//2, 0)
        y1 = max(orig_y - obj_height//2, 0)
        x2 = min(orig_x + obj_width//2, image_width)
        y2 = min(orig_y + obj_height//2, image_height)
        fragment = img[y1:y2, x1:x2]

        cv2.imshow("Fragment", fragment)
        cv2.waitKey(500)
        cv2.destroyWindow("Fragment")

        # YOLO label
        x_center = orig_x / image_width
        y_center = orig_y / image_height
        width = obj_width / image_width
        height = obj_height / image_height
        class_id = 0  # np. gracz

        line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"

        # zapis do pliku txt
        with open(label_path, "a") as f:
            f.write(line)

        print(f"Zapisano label do {label_path}: {line.strip()}")

cv2.imshow("Mapa", small_img)
cv2.setMouseCallback("Mapa", click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()
