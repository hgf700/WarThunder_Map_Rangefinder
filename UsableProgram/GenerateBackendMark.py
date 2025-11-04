import mss
import cv2
import numpy as np
from pynput import mouse, keyboard
import os
import threading
from read_settings import read_settings
# from UsableProgram.read_settings import read_settings
import functools

print = functools.partial(print, flush=True)

settings = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\settings"
os.makedirs(settings, exist_ok=True)
settings_path = os.path.join(settings, "settings.txt")

label_path = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\captures"
os.makedirs(label_path, exist_ok=True)

def GenerateBackendMark(settings_path,label_path,on_capture=None):

    
# Parametry kółka do wizualnego feedbacku (BGR)
    radius1 = 8
    radius2 = 6
    color1 = (0, 165, 255)  # pomarańczowy
    color2 = (39, 250, 0)   # zielony
    Alpha = 0.4

    

    def load_settings_box():
        read=read_settings(settings_path)
        if not read or len(read) < 6:
            print("[!] Brak danych lub za mało wartości w settings.txt.")
            return 0 , 0 ,0,0
    
        parts = read.strip().split()
        if len(parts) < 6:
            print("[!] Za mało wartości w settings.txt:", parts)
            return 0, 0, 0, 0
        
        try:
            MIN_X, MIN_Y, MAX_X, MAX_Y = map(int, parts[2:6])

            return MIN_X, MIN_Y, MAX_X, MAX_Y
        except ValueError as e:
            print("[!] Błąd przy konwersji wartości:", e)
            return 0, 0, 0, 0
        
        # return tuple(map(int, read[2:6]))
    
    MIN_X, MIN_Y, MAX_X, MAX_Y=load_settings_box()

    def capture_region(x1, y1, x2, y2):
        """Robi screenshot tylko z określonego obszaru ekranu."""
        with mss.mss() as sct:
            monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
            img = sct.grab(monitor)
            img_bgr = np.array(img)
            img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_BGRA2BGR)
            return img_bgr


    def draw_marker(img, x, y, alpha=Alpha):
        """Rysuje marker w miejscu kliknięcia."""
        overlay = img.copy()
        cv2.circle(overlay, (x - MIN_X, y - MIN_Y), radius1, color1, 2)
        cv2.circle(overlay, (x - MIN_X, y - MIN_Y), radius2, color2, 2)
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
        return img


    def process_click(x, y):
        """Funkcja wykonywana w osobnym wątku po kliknięciu."""
        x = max(MIN_X, min(x, MAX_X))
        y = max(MIN_Y, min(y, MAX_Y))

        print(f"[DEBUG] Klik: ({x},{y}), Dozwolony: X[{MIN_X},{MAX_X}] Y[{MIN_Y},{MAX_Y}]",flush=True)
        print(f"[+] Kliknięto w dozwolonym zakresie: ({x},{y})",flush=True)

        # Zrób screenshot tylko regionu minimapy
        img = capture_region(MIN_X, MIN_Y, MAX_X, MAX_Y)

        # Narysuj marker w miejscu kliknięcia
        img = draw_marker(img, x, y)

        # Nazwa pliku z numeracją (żeby nie nadpisywać)
        filename = os.path.join(label_path, f"capture.png")
        cv2.imwrite(filename, img)
        print(f"[+] Screenshot zapisany jako {filename}")

        if on_capture:
            on_capture("1")

        # Podgląd (opcjonalny)
        cv2.imshow("Preview", img)
        cv2.waitKey(500)
        cv2.destroyAllWindows()


    def handle_region_click(x, y):
        """Uruchamia wątek, który przetworzy kliknięcie."""
        thread = threading.Thread(target=process_click, args=(x, y))
        thread.daemon = True  # zakończy się razem z programem
        thread.start()


    # ----- Listener myszy -----
    def on_click(x, y, button, pressed):
        if pressed:
            # Blokuj środkowy i prawy przycisk
            if button == mouse.Button.right or button == mouse.Button.middle:
                print(f"[Zablokowano przycisk]: {button}")
                return

            # Tylko kliknięcia w określonym zakresie
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

    print("[*] Listener myszy i klawiatury uruchomiony.")
    with mouse.Listener(on_click=on_click) as mouse_listener, \
        keyboard.Listener(on_press=on_press) as key_listener:
        mouse_listener.join()
    return 

GenerateBackendMark(settings_path,label_path)