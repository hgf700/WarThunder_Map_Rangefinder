from ultralytics import YOLO

# załaduj model tylko raz
model = YOLO("best.pt")  # <-- tu dajesz ścieżkę do swojego modelu

def run_yolo(image_path=None):
    """Uruchamia model YOLOv8 i zwraca wynik"""
    try:
        if not image_path:
            image_path = "example.png"
        results = model(image_path)
        detections = results[0].boxes
        if len(detections) > 0:
            return f"Znaleziono {len(detections)} obiektów"
        else:
            return "Brak wykryć"
    except Exception as e:
        return f"YOLO error: {e}"
