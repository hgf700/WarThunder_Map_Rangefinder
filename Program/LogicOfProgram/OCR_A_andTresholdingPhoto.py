import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pytesseract
from Program.LogicOfProgram.Development import showImagePLT,development
from Program.LogicOfProgram.PathToPrograms import tresholding_PNG_path,prediction_raw_path,tresholding_TXT_path,scale_path,cleanPhoto_raw_path
from Program.LogicOfProgram.GenerateBackendMark import load_settings_box,capture_region
import functools
from Program.LogicOfProgram.logger import setup_logger

logger = setup_logger(__name__)

print = functools.partial(print, flush=True)

# 🔧 Ścieżki
def OCR_A_andTresholdingPhoto():
    MIN_X, MIN_Y, MAX_X, MAX_Y=load_settings_box()

    captureRegionClean = capture_region(MIN_X, MIN_Y, MAX_X, MAX_Y)

    cv2.imwrite(cleanPhoto_raw_path, captureRegionClean)

    if development==1:
        photo = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\Program\photo\image.png"
        image = cv2.imread(str(photo), cv2.IMREAD_GRAYSCALE)
    else:
        image = cv2.imread(str(cleanPhoto_raw_path), cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise FileNotFoundError(f"image not found: {image}")
    
    # 🔧 Unless teseract is not in path
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    height, width = image.shape[:2]
    cut_ratio_h = 0.075  
    cut_ratio_w = 0.4

    cut_start_h = int(height * (1 - cut_ratio_h))
    cut_start_w = int(width * (1 - cut_ratio_w))

    roi = image[cut_start_h:, cut_start_w:] 

    # ⚙️ Progowanie kontrastowe
    lower_thresh = 0
    upper_thresh = 40
    mask = cv2.inRange(roi, lower_thresh, upper_thresh)

    # 🔄 Odwrócenie (czarny tekst na białym tle)
    # processed = cv2.bitwise_not(mask)
    processed = mask

    if showImagePLT==1:
        fig, axes = plt.subplots(1, 2, figsize=(10,5))
        axes[0].imshow(image, cmap="gray")
        axes[0].set_title("Oryginalny obraz")
        axes[0].axis("off")

        axes[1].imshow(processed, cmap="gray")
        axes[1].set_title("Progowanie dolnej części")
        axes[1].axis("off")
        plt.show()

    
    cv2.imwrite(tresholding_PNG_path, processed)

    processed = cv2.GaussianBlur(processed, (3,3), 0)
    processed = cv2.adaptiveThreshold(
        mask,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    # 🔤 OCR
    config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(processed, config=config, lang='eng')

    if showImagePLT==1:
        plt.imshow(processed, cmap='gray')
        plt.axis('off')
        plt.show()
    
    try:
        # "" to remove all white spaces
        value_string =f"{text.strip()}"
        value_int=int(value_string)
        logger.debug(f"ocr recognized: {value_int}")
        print(f"ocr recognized: {value_int}")

        with open(scale_path, "w") as f:
            f.write(value_string)

        with open(tresholding_TXT_path, 'w', encoding='utf-8') as f:
            f.write(value_string)

        return value_int
    except ValueError:
        logger.warning(f"OCR failed, text='{value_int}'")
        return None

# OCR_A_andTresholdingPhoto()