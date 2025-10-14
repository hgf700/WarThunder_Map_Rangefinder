# meassuring and selecting mark, player, and meters and then normalize positon of data to save in .txt 
# aditionaly shows range on map of taken width and heights of objects
import cv2
import os

file = "map_731"
img_path = f"C:\\Users\\USER098\\Documents\\GitHub\\balistic-calculator-WT\\TrainingData\\images\\val\\{file}.png"
# # img_path = f"C:\\Users\\USER098\\Documents\\GitHub\\balistic-calculator-WT\\ManagingData\\fragmentsNew\\{file}.png"
# label_folder = f"C:\\Users\\USER098\\Documents\\GitHub\\balistic-calculator-WT\\ManagingData\\labels\\nowe"

label_folder = f"C:\\Users\\USER098\\Documents\\GitHub\\balistic-calculator-WT\\TrainingData\\labels\\val"
os.makedirs(label_folder, exist_ok=True)
label_path = os.path.join(label_folder, f"{file}.txt")

img = cv2.imread(img_path)

if img is None:
    print("Nie udało się wczytać obrazu!")
    exit()

scale = 1
small_img = cv2.resize(img, (0, 0), fx=scale, fy=scale)

# Wymiary całej minimapy
image_height, image_width = img.shape[:2]

# Domyślny rozmiar prostokąta
obj_width = 30
obj_height = 30
value = 0  # 0 = gracz, 1 = ping, 2 = metry (auto)


def click_event(event, x, y, flags, param):
    global obj_width, obj_height, value

    if event == cv2.EVENT_LBUTTONDOWN:
        # Ustaw tryb automatycznie
        if value == 0:  # Gracz
            obj_width = 20
            obj_height = 20
            print("Tryb: Gracz (20x20)")
        elif value == 1:  # Ping
            obj_width = 30
            obj_height = 30
            print("Tryb: Ping (30x30)")

        # Przeskaluj kliknięcie jeśli obraz został zmniejszony
        orig_x = int(x / scale)
        orig_y = int(y / scale)

        # YOLO box (dla gracza/pingu)
        x1 = max(orig_x - obj_width//2, 0)
        y1 = max(orig_y - obj_height//2, 0)
        x2 = min(orig_x + obj_width//2, image_width)
        y2 = min(orig_y + obj_height//2, image_height)
        fragment = img[y1:y2, x1:x2]

        # Podgląd kliknięcia
        cv2.imshow("Fragment", fragment)
        cv2.waitKey(500)
        cv2.destroyWindow("Fragment")

        # Rysowanie prostokąta
        cv2.rectangle(small_img, (int(x1*scale), int(y1*scale)),
                      (int(x2*scale), int(y2*scale)), (0, 255, 0), 1)
        cv2.putText(small_img, str(value),
                    (int(x2 * scale) + 5, int(y1 * scale) + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
        cv2.imshow("Mapa", small_img)

        # YOLO label (dla kliknięcia)
        x_center = orig_x / image_width
        y_center = orig_y / image_height
        width = obj_width / image_width
        height = obj_height / image_height

        line = f"{value} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
        with open(label_path, "a") as f:
            f.write(line)
        print(f"Zapisano: {line.strip()}")

        # Jeśli był PING → dodaj od razu METRY
        if value == 1:
            meters_x_center = 0.600000
            meters_y_center = 0.969231
            meters_width = 0.300000
            meters_height = 0.076923
            meters_value = 2

            meters_line = f"{meters_value} {meters_x_center:.6f} {meters_y_center:.6f} {meters_width:.6f} {meters_height:.6f}\n"
            with open(label_path, "a") as f:
                f.write(meters_line)
            print(f"[AUTO] Dodano METRY: {meters_line.strip()}")

            value = 0  # Zresetuj cykl → GRACZ
        else:
            value = 1  # Następny tryb → PING


cv2.imshow("Mapa", small_img)
cv2.setMouseCallback("Mapa", click_event)

# ESC zamyka program
while True:
    key = cv2.waitKey(0) & 0xFF
    if key == 27:  # ESC
        break
    if value==1:
        break
    

cv2.destroyAllWindows()
