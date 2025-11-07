# meassuring and selecting mark, player, and meters and then normalize positon of data to save in .txt 
# aditionaly shows range on map of taken width and heights of objects
import cv2
import os

start = 786
end = 793  # ustaw, ile chcesz

for i in range(start, end + 1):

    file = f"map_{i}"
    img_path = f"C:\\Users\\USER098\\Documents\\GitHub\\balistic-calculator-WT\\ManagingData\\fragmentsNew\\{file}.png"
    label_folder = f"C:\\Users\\USER098\\Documents\\GitHub\\balistic-calculator-WT\\ManagingData\\labels\\nowe"
    os.makedirs(label_folder, exist_ok=True)
    label_path = os.path.join(label_folder, f"{file}.txt")

    img = cv2.imread(img_path)
    if img is None:
        print(f"Nie udało się wczytać obrazu {file}, pomijam!")
        continue

    scale = 1
    small_img = cv2.resize(img, (0, 0), fx=scale, fy=scale)

    image_height, image_width = img.shape[:2]

    obj_width = 30
    obj_height = 30
    value = 0  # 0 = gracz, 1 = ping, 2 = metry (auto)

    def click_event(event, x, y, flags, param):
        global obj_width, obj_height, value

        if event == cv2.EVENT_LBUTTONDOWN:
            if value == 0:
                obj_width = 20
                obj_height = 20
                print("Tryb: Gracz (20x20)")
            elif value == 1:
                obj_width = 30
                obj_height = 30
                print("Tryb: Ping (30x30)")

            orig_x = int(x / scale)
            orig_y = int(y / scale)

            x1 = max(orig_x - obj_width//2, 0)
            y1 = max(orig_y - obj_height//2, 0)
            x2 = min(orig_x + obj_width//2, image_width)
            y2 = min(orig_y + obj_height//2, image_height)

            cv2.rectangle(small_img, (int(x1*scale), int(y1*scale)),
                          (int(x2*scale), int(y2*scale)), (0, 255, 0), 1)
            cv2.putText(small_img, str(value),
                        (int(x2 * scale) + 5, int(y1 * scale) + 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
            cv2.imshow("Mapa", small_img)

            x_center = orig_x / image_width
            y_center = orig_y / image_height
            width = obj_width / image_width
            height = obj_height / image_height

            line = f"{value} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
            with open(label_path, "a") as f:
                f.write(line)
            print(f"Zapisano: {line.strip()}")

            if value == 1:
                # meters_line = "2 0.771875 0.966154 0.437500 0.076923\n"
                # with open(label_path, "a") as f:
                #     f.write(meters_line)
                # print(f"[AUTO] Dodano METRY: {meters_line.strip()}")
                value = 0
            else:
                value = 1

    cv2.imshow("Mapa", small_img)
    cv2.setMouseCallback("Mapa", click_event)

    # CZEKAJ NA ESC → TYLKO PRZERWIJ TEN OBRAZEK I PRZEJDŹ DALEJ
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            print(f"Pomijam {file}, przechodzę do kolejnego...")
            break

    cv2.destroyAllWindows()
