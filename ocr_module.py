import pytesseract
import cv2

def run_ocr(image_path=None):
    """Zwraca tekst rozpoznany z obrazu (OCR)"""
    try:
        if not image_path:
            image_path = "example.png"  # tu możesz przekazać zrzut ekranu
        img = cv2.imread(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        return f"OCR error: {e}"
