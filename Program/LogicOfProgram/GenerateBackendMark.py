import mss
import cv2
import numpy as np
from pynput import mouse, keyboard
import os
import threading
import functools
from Program.LogicOfProgram.ReadFromFile import ReadFromFile
from Program.LogicOfProgram.PathToPrograms import settings_path, prediction_raw_path
from Program.LogicOfProgram.Development import writeImage
from Program.LogicOfProgram.logger import setup_logger

print = functools.partial(print, flush=True)

logger = setup_logger(__name__)

def load_settings_box():
    read = ReadFromFile(settings_path)
    if not read:
        logger.debug(f"file {settings_path} is empty or didnt exist")
        print(f"[!] file {settings_path} is empty or didnt exist.")
        return 0, 0, 0, 0

    parts = read.strip().split()
    if len(parts) < 6:
        logger.debug(f"too small value ({len(parts)}) in settings.txt: {parts}")
        print(f"[!] too small value ({len(parts)}) in settings.txt: {parts}")
        return 0, 0, 0, 0

    try:
        MIN_X, MIN_Y, MAX_X, MAX_Y = map(int, parts[2:6])
        print(f"[OK] lodaded cordinates: {MIN_X}, {MIN_Y}, {MAX_X}, {MAX_Y}")
        return MIN_X, MIN_Y, MAX_X, MAX_Y
    except ValueError as e:
        print(f"[!] error while convertion of data: {e}")
        logger.debug(f"error while convertion of data: {e}")
        return 0, 0, 0, 0

        
        # return tuple(map(int, read[2:6]))
def capture_region(x1, y1, x2, y2):
    """ ss only in allowed area of screen."""
    with mss.mss() as sct:
        monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
        img = sct.grab(monitor)
        img_bgr = np.array(img)
        img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_BGRA2BGR)
        return img_bgr  

#on capture flaga dla callback 
# Python traktuje None jako False.
def GenerateBackendMark(settings_path,prediction_raw_path,on_capture=None):
# Parametry kółka do wizualnego feedbacku (BGR)
    radius1 = 8
    radius2 = 6
    color1 = (0, 165, 255)  # pomarańczowy
    color2 = (39, 250, 0)   # zielony
    Alpha = 0.4 
        
    MIN_X, MIN_Y, MAX_X, MAX_Y=load_settings_box()

    def draw_marker(img, x, y, alpha=Alpha):
        """Draw marker in place of click"""
        overlay = img.copy()
        cv2.circle(overlay, (x - MIN_X, y - MIN_Y), radius1, color1, 2)
        cv2.circle(overlay, (x - MIN_X, y - MIN_Y), radius2, color2, 2)
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
        return img

    alt_pressed=False

    def on_press(key):
        nonlocal alt_pressed
        if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            alt_pressed = True

    def on_release(key):
        global alt_pressed
        if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            alt_pressed = False

    def process_click(x, y):
        """function handled in different thread after click."""
        x = max(MIN_X, min(x, MAX_X))
        y = max(MIN_Y, min(y, MAX_Y))

        print(f"[DEBUG] click: ({x},{y}), allowed: X[{MIN_X},{MAX_X}] Y[{MIN_Y},{MAX_Y}]",flush=True)
        print(f"[+] click in allowed are: ({x},{y})",flush=True)

        # Zrób screenshot tylko regionu minimapy
        img = capture_region(MIN_X, MIN_Y, MAX_X, MAX_Y)

        # Narysuj marker w miejscu kliknięcia
        img = draw_marker(img, x, y)

        cv2.imwrite(prediction_raw_path, img)
        print(f"[+] ss saved as {prediction_raw_path}")

#callback 
# Python traktuje None jako False.
        if on_capture:
            on_capture("1")

        # Podgląd (opcjonalny)
        if(writeImage==1):
            cv2.imshow("Preview", img)
            cv2.waitKey(500)
        cv2.destroyAllWindows()


    def handle_region_click(x, y):
        """activate thread to handling mouse click."""
        thread = threading.Thread(target=process_click, args=(x, y))
        thread.daemon = True  # zakończy się razem z programem
        thread.start()


    # ----- Listener myszy -----
    def on_click(x, y, button, pressed):
        nonlocal  alt_pressed
        if pressed:
            # Blokuj środkowy i prawy przycisk
            if button == mouse.Button.right or button == mouse.Button.middle:
                print(f"[Ignore right and scroll]: {button}")
                return

            if button==mouse.Button.left and pressed and alt_pressed:
                print(f"alt+lpm in allowed are: {x},{y}")
                
                logger.debug(f"alt+lpm click")
                # Tylko kliknięcia w określonym zakresie
                if MIN_X <= x <= MAX_X and MIN_Y <= y <= MAX_Y:
                    handle_region_click(x, y)
                else:
                    logger.debug(f"with alt | Ignore click apart minimap: ({x},{y}")
                    logger.debug(f"with alt | X[{MIN_X},{MAX_X}] Y[{MIN_Y},{MAX_Y} ")
                    print(f"[Ignore click apart minimap]: ({x},{y})")
                    print(f"X[{MIN_X},{MAX_X}] Y[{MIN_Y},{MAX_Y})")

    # ----- Obsługa ESC -----
    # def on_press(key):
    #     try:
    #         if key == keyboard.Key.esc:
    #             print("\n[!] ESC wciśnięty — zamykam program.")
    #             os._exit(0)
    #     except Exception as e:
    #         print(f"Błąd przy obsłudze klawiatury: {e}")

    print("[*] Listener ")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as kl, \
        mouse.Listener(on_click=on_click) as ml:
        kl.join()
        ml.join()


# GenerateBackendMark(settings_path,captures_folder)