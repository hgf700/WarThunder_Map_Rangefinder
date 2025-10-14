from ultralytics import YOLO

model = YOLO("yolov8n.pt")  
# imgsz=640

model.train(
    data=r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\TrainingData\data.yaml",
    epochs=1,
    imgsz=640,
    augment=True,
    cache=False,
    save_hybrid=True,  # zapisuje zarówno etykiety prawdziwe jak i przewidywania
    save_txt=True,     # zapisze etykiety do plików .txt
    save=True,         # zapisze wyniki
    name="train_wt"
)

# model = YOLO("runs/detect/train5/weights/best.pt")
# model.train(data=r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\TrainingData\data.yaml", epochs=50, imgsz=800 ,augment=True,name="train_aug" )
