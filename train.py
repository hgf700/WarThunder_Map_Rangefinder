from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # lekki model do testów
model.train(data="data.yaml", epochs=50, imgsz=640)
