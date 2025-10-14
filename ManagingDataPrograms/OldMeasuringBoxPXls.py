import cv2
import os

# file = "map_009"
# file = "map_045"
# file = "map_071"
file = "map_684"
# file = "map_731"


img_path = f"C:\\Users\\USER098\\Documents\\GitHub\\balistic-calculator-WT\\TrainingData\\images\\val\\{file}.png"
label_folder = f"C:\\Users\\USER098\\Documents\\GitHub\\balistic-calculator-WT\\TrainingData\\labels\\val"

os.makedirs(label_folder, exist_ok=True)
label_path = os.path.join(label_folder, f"{file}.txt")

img = cv2.imread(img_path)

if img is None:
    print("Nie udało się wczytać obrazu!")
    exit()

scale = 1
small_img = cv2.resize(img, (0, 0), fx=scale, fy=scale)

image_height, image_width = img.shape[:2]

obj_width = 30
obj_height = 30
value = 0
click_id = 0

def click_event(event, x, y, flags, param):
    global obj_width, obj_height, value, click_id, small_img

    if event == cv2.EVENT_LBUTTONDOWN:
        orig_x = int(x / scale)
        orig_y = int(y / scale)

        x1 = max(orig_x - obj_width // 2, 0)
        y1 = max(orig_y - obj_height // 2, 0)
        x2 = min(orig_x + obj_width // 2, image_width)
        y2 = min(orig_y + obj_height // 2, image_height)
        fragment = img[y1:y2, x1:x2]

        cv2.imshow("Fragment", fragment)

        if click_id == 0:
            value = 0
            click_id = 1
        else:
            value += 1

        cv2.rectangle(small_img, (x1, y1), (x2, y2), (0, 255, 0), 1)
        cv2.putText(small_img, str(value), (x2 + 5, y1 + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
        cv2.imshow("Mapa", small_img)

        x_center = orig_x / image_width
        y_center = orig_y / image_height
        width = obj_width / image_width
        height = obj_height / image_height

        line = f"{value} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
        with open(label_path, "a") as f:
            f.write(line)

        print(f"Zapisano label do {label_path}: {line.strip()}")

cv2.imshow("Mapa", small_img)
cv2.setMouseCallback("Mapa", click_event)

while True:
    key = cv2.waitKey(1) & 0xFF  
    if key == ord('1'):
        obj_width = 30
        obj_height = 30
        print(f"Ustawiono 30x30 | Znormalizowane: {obj_width/image_width:.6f} x {obj_height/image_height:.6f}")
    elif key == ord('2'):
        obj_width = 50
        obj_height = 50
        print(f"Ustawiono 50x50 | Znormalizowane: {obj_width/image_width:.6f} x {obj_height/image_height:.6f}")
    elif key == ord('3'):
        obj_width = 140
        obj_height = 20
        print(f"Ustawiono 100x100 | Znormalizowane: {obj_width/image_width:.6f} x {obj_height/image_height:.6f}")
    elif key == 27:  # ESC
        print("Zamykam")
        break

cv2.destroyAllWindows()
