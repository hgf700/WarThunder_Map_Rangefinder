import cv2
import numpy as np
import pyautogui
from ultralytics import YOLO
import time

# 🔹 Załaduj model YOLO
model="train_yolo_wt"
model_path = fr"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\runs\detect\{model}\weights\last.pt"
model = YOLO(model_path)

x1, y1, x2, y2 = 1584, 741, 1904, 1066

# 🔹 Okno do pokazywania kliknięć i wyników
window_name = "Click Detector"
cv2.namedWindow(window_name)

# Globalne zmienne
click_point = None
image_display = np.zeros((720, 1280, 3), dtype=np.uint8)


def mouse_callback(event, x, y, flags, param):
    global click_point
    if 1584 <= x1 <= 1904 and 741 <= y1 <= 1066 and 1584 <= x2 <= 1904 and 741 <= y2 <= 1066:
            if event == cv2.EVENT_LBUTTONDOWN:
                click_point = (x, y)
                print(f"[INFO] Kliknięto w punkt: {click_point}")

                # 🔸 Narysuj znacznik
                img_mark = image_display.copy()
                cv2.drawMarker(img_mark, click_point, (0, 255, 0), markerType=cv2.MARKER_CROSS, 
                            markerSize=20, thickness=2)

                cv2.imshow(window_name, img_mark)

                # 🔸 Screenshot ekranu
                screenshot = pyautogui.screenshot()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                # 🔸 Analiza YOLO
                results = model.predict(frame, verbose=False)
                for r in results:
                    for box in r.boxes:
                        x1, y1, x2, y2 = box.xyxy[0]
                        conf = float(box.conf[0])
                        cls = int(box.cls[0])
                        print(f"Klasa: {cls}, Confidence: {conf:.2f}, BBox: ({x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f})")

                # 🔸 Zapisz wynik YOLO
                annotated = results[0].plot()
                cv2.imshow("YOLO wynik", annotated)
                cv2.imwrite("yolo_result.png", annotated)
                print("[INFO] Zapisano wynik YOLO do yolo_result.png")

# 🔹 Ustaw callback myszy
cv2.setMouseCallback(window_name, mouse_callback)

print("Kliknij w okno, aby zaznaczyć punkt i uruchomić analizę YOLO.")
cv2.imshow(window_name, image_display)

while True:
    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break

cv2.destroyAllWindows()
