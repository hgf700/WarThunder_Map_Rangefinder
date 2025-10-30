# UsableProgram/capture_minimap.py
import mss
import cv2
import numpy as np
from pynput import mouse
import os
import time

# ===== USTAWIENIA =====
MIN_X, MIN_Y = 800, 500
MAX_X, MAX_Y = 1366, 768

CAPTURE_FOLDER = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\captures"
os.makedirs(CAPTURE_FOLDER, exist_ok=True)

# Kółko na obrazie
CIRCLE_RADIUS = 20
CIRCLE_COLOR = (0, 255, 0)  # BGR: zielony
CIRCLE_THICKNESS = -1       # wypełnione

# Debounce (anty-spam)
_last_click = 0
DEBOUNCE = 0.3  # sekundy

# ===== FUNKCJE =====
def capture_region():
    with mss.mss() as sct:
        monitor = {"left": MIN_X, "top": MIN_Y, "width": MAX_X - MIN_X, "height": MAX_Y - MIN_Y}
        img = sct.grab(monitor)
        img_np = np.array(img)
        return cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)

def draw_marker(img, x, y):
    cv2.circle(img, (x - MIN_X, y - MIN_Y), CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)
    return img

def save_capture(x, y):
    global _last_click
    now = time.time()
    if now - _last_click < DEBOUNCE:
        return
    _last_click = now

    img = capture_region()
    img = draw_marker(img, x, y)
    
    filename = os.path.join(CAPTURE_FOLDER, f"click_{int(now)}.png")
    cv2.imwrite(filename, img)
    
    # Zapis współrzędnych (dla reszty programu)
    pos_file = os.path.join(CAPTURE_FOLDER, "..", "settings", "click_position.txt")
    os.makedirs(os.path.dirname(pos_file), exist_ok=True)
    with open(pos_file, "w") as f:
        f.write(f"{x},{y}\n")
    
    print(f"Zapisano: ({x}, {y}) → {filename}")

# ===== LISTENER MYSZY =====
def on_click(x, y, button, pressed):
    if not pressed or button != mouse.Button.left:
        return
    if MIN_X <= x <= MAX_X and MIN_Y <= y <= MAX_Y:
        save_capture(x, y)
    else:
        print(f"Poza minimapą: ({x}, {y})")

print("Listener aktywny – kliknij LPM na minimapie (800-1366, 500-768)")
print("PPM = wyjście")

with mouse.Listener(on_click=on_click) as listener:
    # Użyj klawiatury do wyjścia
    import keyboard
    while listener.running:
        if keyboard.is_pressed('esc'):
            break
        time.sleep(0.01)
    listener.stop()

print("Zakończono.")