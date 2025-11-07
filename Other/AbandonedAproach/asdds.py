import tkinter as tk
import threading
import time
import mss
import cv2
import numpy as np
import os

# ----- Ustawienia -----
SAVE_PATH = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\captures"
os.makedirs(SAVE_PATH, exist_ok=True)

SCREEN_W, SCREEN_H = 1366, 768
CIRCLE_RADIUS = 20
CIRCLE_COLOR = "#ffa500"  # pomarańczowy
CIRCLE_ALPHA = 0.4        # przezroczystość (0-1)
VISIBLE_TIME = 1.5        # ile sekund marker ma być widoczny


# ----- Funkcje -----
def capture_screenshot(x, y, width=SCREEN_W, height=SCREEN_H):
    """Zrób screenshot całego ekranu (lub obszaru)"""
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": width, "height": height}
        img = sct.grab(monitor)
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)

        filename = os.path.join(SAVE_PATH, f"capture_{int(time.time())}.png")
        cv2.imwrite(filename, img)
        print(f"[+] Screenshot zapisany jako {filename}")
        return filename


def draw_marker(canvas, x, y, duration=VISIBLE_TIME):
    """Rysuje kółko w miejscu kliknięcia i usuwa po czasie"""
    # Tkinter nie wspiera alfa kanału, więc zrobimy przez kolor wypełnienia z lekko przeźroczystym odcieniem
    circle = canvas.create_oval(
        x - CIRCLE_RADIUS, y - CIRCLE_RADIUS,
        x + CIRCLE_RADIUS, y + CIRCLE_RADIUS,
        outline="", fill=CIRCLE_COLOR
    )

    def remove_circle():
        time.sleep(duration)
        canvas.delete(circle)

    threading.Thread(target=remove_circle, daemon=True).start()


def on_click(event):
    print(f"[+] Kliknięto: ({event.x}, {event.y})")
    draw_marker(canvas, event.x, event.y)
    capture_screenshot(event.x, event.y)


# ----- GUI -----
root = tk.Tk()
root.attributes('-fullscreen', True)
root.attributes('-alpha', CIRCLE_ALPHA)   # przezroczyste tło okna
root.attributes('-topmost', True)
root.config(bg='black')
root.overrideredirect(True)               # bez ramki
canvas = tk.Canvas(root, width=SCREEN_W, height=SCREEN_H, bg='', highlightthickness=0)
canvas.pack(fill="both", expand=True)

canvas.bind("<Button-1>", on_click)

print("[*] Kliknij w dowolne miejsce, by wygenerować marker i screenshot.")
root.mainloop()
