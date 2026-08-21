import cv2
import matplotlib.pyplot as plt
import functools
import pytesseract
from Program.LogicOfProgram.Development import (
    showImagePLT,
    development
)
from Program.LogicOfProgram.PathToPrograms import (
    tresholding_PNG_path,
    tresholding_TXT_path,
    scale_path,
    cleanPhoto_raw_path
)
from Program.LogicOfProgram.GenerateBackendMark import load_settings_box, capture_region
from Program.LogicOfProgram.logger import setup_logger

logger = setup_logger(__name__)
print = functools.partial(print, flush=True)

def OCR_A_andTresholdingPhoto():
    MIN_X, MIN_Y, MAX_X, MAX_Y = load_settings_box()
    
    captureRegionClean = capture_region(MIN_X, MIN_Y, MAX_X, MAX_Y)
    cv2.imwrite(cleanPhoto_raw_path, captureRegionClean)

    # Wczytanie obrazu
    if development == 1:
        photo = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\Program\photo\image.png"
        image = cv2.imread(str(photo), cv2.IMREAD_GRAYSCALE)
    else:
        image = cv2.imread(str(cleanPhoto_raw_path), cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise FileNotFoundError(f"image not found: {image}")

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # Wycięcie ROI (dolna prawa część)
    height, width = image.shape[:2]
    crop_width = 120
    crop_height = 25
    offset_from_end = 10  # ile px przed końcem obrazu w poziomie zaczyna się wycinek

    # Współrzędne prostokąta
    y_start = height - crop_height       
    y_end = height                       
    x_start = width - crop_width - offset_from_end  
    x_end = width - offset_from_end

    # Wycięcie prostokąta
    roi = image[y_start:y_end, x_start:x_end]

    # Progowanie kontrastowe
    lower_thresh = 0
    upper_thresh = 40
    mask = cv2.inRange(roi, lower_thresh, upper_thresh)

    # Odwrócenie (tekst czarny -> 255)
    processed = cv2.bitwise_not(mask)

    # Odszumianie i morphologia rozszerzenie biale na sasiednie a potem zmniejszenie na normalne rozmiary
    processed = cv2.GaussianBlur(processed, (3, 3), 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    processed = cv2.morphologyEx(processed, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite(tresholding_PNG_path, processed)

    # OCR
    config = r'--oem 1 --psm 7 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(processed, config=config, lang='eng')

    if showImagePLT == 1:
        plt.imshow(processed, cmap='gray')
        plt.axis('off')
        plt.show()

    try:
        value_string = "".join(text.split())
        value_int = int(value_string)
        logger.debug(f"OCR recognized: {value_int}")
        print(f"OCR recognized: {value_int}")

        with open(scale_path, "w") as f:
            f.write(value_string)
        with open(tresholding_TXT_path, 'w', encoding='utf-8') as f:
            f.write(value_string)

        return value_int
    except ValueError:
        logger.warning(f"OCR failed, text='{text}'")
        print(f"OCR failed, text={text}")
        return None

# OCR_A_andTresholdingPhoto()