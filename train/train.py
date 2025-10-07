from ultralytics import YOLO

model = YOLO("yolov8n.pt")  
model.train(data=r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\TrainingData\data.yaml", epochs=50, imgsz=640 ,augment=True,name="train_wt" )

# model = YOLO("runs/detect/train5/weights/best.pt")
# model.train(data=r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\TrainingData\data.yaml", epochs=50, imgsz=800 ,augment=True,name="train_aug" )
