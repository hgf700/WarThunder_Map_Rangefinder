from ultralytics import YOLO
import os
import cv2

def UsageOfYolo():
    file = "train_yolo_wt"
    model_file = "last.pt"
    capture ="capture.png"

    model_folder = fr"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\runs\detect\{file}\weights"
    os.makedirs(model_folder, exist_ok=True)

    captures_folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\captures"
    os.makedirs(captures_folder, exist_ok=True)

    model_path = os.path.join(model_folder, model_file)

    capture_path=os.path.join(captures_folder, capture)

    # Załaduj model
    model = YOLO(model_path)

    # Detekcja
    results = model.predict(source=capture_path)

    # Utwórz folder na wyniki
    output_folder = os.path.join(captures_folder, "wyniki")
    os.makedirs(output_folder, exist_ok=True)

    # Ścieżka do obrazu i pliku TXT
    output_image_path = os.path.join(output_folder, "prediction.png")
    output_txt_path = os.path.join(output_folder, "prediction.txt")

    # Zapis wyników do TXT
    with open(output_txt_path, "w", encoding="utf-8") as f:
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]  # współrzędne
                conf = box.conf[0]
                cls = int(box.cls[0])
                line = f"Klasa: {cls}, Confidence: {conf:.2f}, BBox: ({x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f})\n"
                f.write(line)
                print(line.strip())

    # Podgląd obrazu z wykryciami
    img_pred = results[0].plot()
    cv2.imshow("Predykcja", img_pred)

    while True:
        key = cv2.waitKey(1)
        if key == 27:  # ESC aby wyjść
            break

    cv2.destroyAllWindows()

    # Zapis obrazu z bounding boxami
    cv2.imwrite(output_image_path, img_pred)
    print(f"Wyniki zapisano: {output_txt_path} i {output_image_path}")

UsageOfYolo()