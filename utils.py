import cv2
import numpy as np
from mss import mss

def take_screenshot(region):
    """Zwraca obraz numpy z podanego regionu"""
    with mss() as sct:
        screenshot = sct.grab(region)
        frame = np.array(screenshot)
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
