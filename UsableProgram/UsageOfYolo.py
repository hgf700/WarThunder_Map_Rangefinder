from ultralytics import YOLO
import os
import cv2
import functools

print = functools.partial(print, flush=True)

def UsageOfYolo():
    file = "train_yolo_wt"
    model_file = "last.pt"
    capture = "capture.png"

    model_folder = fr"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\runs\detect\{file}\weights"
    captures_folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\captures"

    os.makedirs(captures_folder, exist_ok=True)
    model_path = os.path.join(model_folder, model_file)
    capture_path = os.path.join(captures_folder, capture)

    # Załaduj model
    model = YOLO(model_path)

    # Wykonaj detekcję
    results = model.predict(source=capture_path, save=False, verbose=False)

    # Utwórz folder na wyniki
    output_folder = os.path.join(captures_folder, "wyniki")
    os.makedirs(output_folder, exist_ok=True)

    # Ścieżki do plików wynikowych
    output_image_path = os.path.join(output_folder, "prediction.png")
    output_txt_path = os.path.join(output_folder, "prediction.txt")

    # Zapis wyników do TXT
    with open(output_txt_path, "w", encoding="utf-8") as f:
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = box.conf[0]
                cls = int(box.cls[0])
                f.write(f"{cls} {conf:.2f} {x1:.0f} {y1:.0f} {x2:.0f} {y2:.0f}\n")
                print(f"Klasa: {cls}, Conf: {conf:.2f}, BBox: ({x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f})")

    # Zapisz obraz z detekcjami
    img_pred = results[0].plot()
    success = cv2.imwrite(output_image_path, img_pred)

    if success:
        print(f"[✔] Wyniki zapisano:\n{output_txt_path}\n{output_image_path}")
    else:
        print("[❌] Błąd przy zapisie prediction.png")

    cv2.destroyAllWindows()

# UsageOfYolo()