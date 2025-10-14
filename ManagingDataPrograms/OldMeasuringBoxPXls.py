import cv2
import os

file = "map_020"
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

# Domyślny rozmiar prostokąta
obj_width = 30
obj_height = 30
value=0
click_id=0

def click_event(event, x, y, flags, param):
    global obj_width, obj_height ,value,click_id   # Umożliwiamy dostęp do rozmiaru prostokąta

    if event == cv2.EVENT_LBUTTONDOWN:
        # przeskaluj kliknięcie jeśli obraz został zmniejszony
        orig_x = int(x / scale)
        orig_y = int(y / scale)

        # fragment do podglądu o tych samych wymiarach co YOLO box
        x1 = max(orig_x - obj_width//2, 0)
        y1 = max(orig_y - obj_height//2, 0)
        x2 = min(orig_x + obj_width//2, image_width)
        y2 = min(orig_y + obj_height//2, image_height)
        fragment = img[y1:y2, x1:x2]

        cv2.imshow("Fragment", fragment)
        cv2.waitKey(500)
        cv2.destroyWindow("Fragment")
        if click_id==0:
            value=0
            click_id=1
        elif click_id == 1:
            value+=1

        show =1
        if show ==1:

            # Rysowanie prostokąta na obrazie dla podglądu
            cv2.rectangle(small_img, (int(x1*scale), int(y1*scale)), (int(x2*scale), int(y2*scale)), (0, 255, 0), 1)
            cv2.putText(
                small_img, 
                str(value),                       # <-- tu możesz wstawić np. f"({orig_x},{orig_y})"
                (int(x2 * scale) + 5, int(y1 * scale) + 15),  # pozycja tekstu (tu: obok prawego górnego rogu)
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.3, 
                (0, 255, 0), 1
            )
            cv2.imshow("Mapa", small_img)

        # YOLO label
        x_center = orig_x / image_width
        y_center = orig_y / image_height
        width = obj_width / image_width
        height = obj_height / image_height

        # class_id = 0  # np. gracz

        # line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
        line = f"{value} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"

        # zapis do pliku txt
        with open(label_path, "a") as f:
            f.write(line)

        print(f"Zapisano label do {label_path}: {line.strip()}")

cv2.imshow("Mapa", small_img)
cv2.setMouseCallback("Mapa", click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()
# Pętla główna do obsługi klawiszy
while True:
    key = cv2.waitKey(0) & 0xFF  # Czekaj na naciśnięcie klawisza
    if key == ord('1'):  # Naciśnięcie 'A'
        obj_width = 30
        obj_height = 30
        print("Zmieniono rozmiar prostokąta na 30x30 pikseli")
    elif key == ord('2'):  # Naciśnięcie 'D'
        obj_width = 30
        obj_height = 30
        print("Zmieniono rozmiar prostokąta na 30x30 pikseli")
    elif key == ord('3'):  # Naciśnięcie 'D'
        obj_width = 30
        obj_height = 30
        print("Zmieniono rozmiar prostokąta na 30x30 pikseli")
    elif key == 27:  # Naciśnięcie ESC - wyjście z programu
        break

cv2.destroyAllWindows()