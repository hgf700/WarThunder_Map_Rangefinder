from ultralytics import YOLO
import cv2
import functools
from pathlib import Path

print = functools.partial(print, flush=True)

# 🔹 Ustawienia ścieżek
base_dir = Path(__file__).resolve().parent.parent
usable_program = base_dir / "UsableProgram"

file = "train_yolo_wt"
model_file = "last.pt"
capture_file = "capture.png"

# 🔹 Folder i plik modelu
model_path = base_dir / "runs" / "detect" / file / "weights" / model_file

# 🔹 Folder i plik z obrazem do analizy
captures_folder = usable_program / "captures"
captures_folder.mkdir(parents=True, exist_ok=True)
captures_path = captures_folder / capture_file

# 🔹 Folder na wyniki
output_folder = captures_folder / "wyniki"
output_folder.mkdir(parents=True, exist_ok=True)
output_image_path = output_folder / "prediction.png"
output_txt_path = output_folder / "prediction.txt"


def UsageOfYolo():
    # 🔸 Sprawdź, czy model i obraz istnieją
    if not model_path.exists():
        print(f"❌ Nie znaleziono modelu: {model_path}")
        return
    if not captures_path.exists():
        print(f"❌ Nie znaleziono pliku obrazu: {captures_path}")
        return

    # 🔹 Załaduj model
    print(f"🔄 Ładowanie modelu: {model_path}")
    model = YOLO(model_path)

    # 🔹 Wykonaj predykcję
    print(f"🧠 Wykonywanie predykcji na {captures_path}...")
    results = model.predict(source=str(captures_path))

    # 🔹 Zapis wyników do pliku TXT
    with open(output_txt_path, "w", encoding="utf-8") as f:
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = box.conf[0]
                cls = int(box.cls[0])
                line = f"{cls} {conf:.2f} {x1:.0f} {y1:.0f} {x2:.0f} {y2:.0f} "
                f.write(line)
                print(line.strip())

    # 🔹 Podgląd i zapis obrazu z bounding boxami
    img_pred = results[0].plot()
    cv2.imshow("Predykcja", img_pred)

    while True:
        key = cv2.waitKey(1)
        if key == 27:  # ESC, aby zamknąć okno
            break

    cv2.destroyAllWindows()
    cv2.imwrite(str(output_image_path), img_pred)

    print(f"✅ Wyniki zapisano w:\n  - {output_txt_path}\n  - {output_image_path}")



# UsageOfYolo()