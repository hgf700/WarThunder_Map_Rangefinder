from ultralytics import YOLO
import os
import cv2
import functools
from Program.LogicOfProgram.PathToPrograms import (
    model_path,
    prediction_raw_path,
    prediction_folder,
    prediction_path
)
from Program.LogicOfProgram.logger import setup_logger
from Program.LogicOfProgram.pyinstaller_Utility import resource_path

logger = setup_logger(__name__)

print = functools.partial(print, flush=True)

def UsageOfYolo():
    
    # MODEL_RELATIVE_PATH = "yolo_weights/last.pt"

    # model_path = resource_path(MODEL_RELATIVE_PATH)
    model = YOLO(model_path)

    # Wykonaj detekcję
    results = model.predict(source=prediction_raw_path, save=False, verbose=False)

    # Ścieżki do plików wynikowych
    output_image_path = os.path.join(prediction_folder, "prediction.png")

    # Zapis wyników do TXT
    with open(prediction_path, "w", encoding="utf-8") as f:
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = box.conf[0]
                cls = int(box.cls[0])
                f.write(f"{cls} {conf:.2f} {x1:.0f} {y1:.0f} {x2:.0f} {y2:.0f} ")
                print(f"class: {cls}, Conf: {conf:.2f}, BBox: ({x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f})")

    # Zapisz obraz z detekcjami
    img_pred = results[0].plot()
    success = cv2.imwrite(output_image_path, img_pred)

    if success:
        print(f"[✔] value saved:\n{prediction_path}\n{output_image_path}")
    else:
        print("[❌] errow while saving prediction.png")

    cv2.destroyAllWindows()

# UsageOfYolo()