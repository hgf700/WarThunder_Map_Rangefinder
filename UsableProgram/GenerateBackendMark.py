import mss
import cv2
import numpy as np
from pynput import mouse, keyboard
import os
import sys

# ----- Ustawienia -----
MIN_X, MAX_X = 0, 1366
MIN_Y, MAX_Y = 0, 768

label_path = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\captures"
os.makedirs(label_path, exist_ok=True)

# Parametry kółka do wizualnego feedbacku
CIRCLE_RADIUS = 20
CIRCLE_COLOR = (0, 255, 0)  # zielony
CIRCLE_ALPHA = 0.4          # półprzezroczyste

# ----- Funkcje -----
def capture_region(x1, y1, x2, y2):
    with mss.mss() as sct:
        monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
        img = sct.grab(monitor)
        img_bgr = np.array(img)
        img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_RGBA2BGR)
        return img_bgr

def draw_marker(img, x, y, radius=CIRCLE_RADIUS, color=CIRCLE_COLOR, alpha=CIRCLE_ALPHA):
    overlay = img.copy()
    cv2.circle(overlay, (x - MIN_X, y - MIN_Y), radius, color, -1)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    return img

def handle_region_click(x, y):
    print(f"[+] Kliknięto w dozwolonym zakresie: ({x},{y})")
    img = capture_region(MIN_X, MIN_Y, MAX_X, MAX_Y)
    img = draw_marker(img, x, y)
    filename = os.path.join(label_path, "capture.png")
    cv2.imwrite(filename, img)
    print(f"[+] Screenshot zapisany jako {filename}")

    # Podgląd (opcjonalnie)
    cv2.imshow("Preview", img)
    cv2.waitKey(500)
    cv2.destroyAllWindows()

# ----- Listener globalny myszy -----
def on_click(x, y, button, pressed):
    if pressed:
        if MIN_X <= x <= MAX_X and MIN_Y <= y <= MAX_Y:
            handle_region_click(x, y)
        else:
            print(f"[Ignoruję kliknięcie poza minimapą]: ({x},{y})")

# ----- Obsługa ESC -----
def on_press(key):
    try:
        if key == keyboard.Key.esc:
            print("\n[!] ESC wciśnięty — zamykam program.")
            os._exit(0)
    except Exception as e:
        print(f"Błąd przy obsłudze klawiatury: {e}")

# ----- Start -----
if __name__ == "__main__":
    print("[*] Listener myszy i klawiatury uruchomiony.")
    print("[*] Kliknij w minimapę, lub naciśnij ESC aby zakończyć.")

    # Uruchamiamy dwa listenery równolegle
    with mouse.Listener(on_click=on_click) as mouse_listener, \
         keyboard.Listener(on_press=on_press) as key_listener:
        mouse_listener.join()
        key_listener.join()
