# test generate frontend sign on minimap
import cv2

# Wczytaj obraz
img = cv2.imread(r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\TrainingData\ManagingData\podejscieTest\map_001.png")

if img is None:
    print("Nie udało się wczytać obrazu!")
    exit()

scale = 0.65
small_img = cv2.resize(img, (0, 0), fx=scale, fy=scale)

annotated_img = small_img.copy()

# 🔲 Oryginalne granice minimapy (z pełnego obrazu)
# MIN_X_ORIG, MAX_X_ORIG = 1584, 1904
# MIN_Y_ORIG, MAX_Y_ORIG = 741, 1066

MIN_X_ORIG, MAX_X_ORIG = 0,320
MIN_Y_ORIG, MAX_Y_ORIG = 0,325

# 🔁 Przeskalowane granice na small_img
MIN_X = int(MIN_X_ORIG * scale)
MAX_X = int(MAX_X_ORIG * scale)
MIN_Y = int(MIN_Y_ORIG * scale)
MAX_Y = int(MAX_Y_ORIG * scale)

def click_event(event, x, y, flags, param):
    global annotated_img
    if event == cv2.EVENT_LBUTTONDOWN:

        # ✅ Sprawdź czy kliknięcie jest w dozwolonym obszarze
        if MIN_X <= x <= MAX_X and MIN_Y <= y <= MAX_Y:

            # Przeskalowanie kliknięcia na oryginalne współrzędne
            orig_x = int(x / scale)
            orig_y = int(y / scale)
            

            cv2.circle(annotated_img, (x, y), 8, (0, 140, 255), 2)  # 
            print(f"[OK] Klik w minimapie → ORIG({orig_x}, {orig_y}) | SMALL({x}, {y})")
        else:
            print(f"[Ignoruję] Klik poza minimapą: {x}, {y}")

        cv2.imshow("Mapa", annotated_img)

# Wyświetl obraz
cv2.imshow("Mapa", annotated_img)
cv2.setMouseCallback("Mapa", click_event)

while True:
    key = cv2.waitKey(1)
    if key == ord('s'):
        cv2.imwrite("annotated_map.png", annotated_img)
        print("Zapisano jako annotated_map.png")
    if key == 27:
        break

cv2.destroyAllWindows()
