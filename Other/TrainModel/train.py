from ultralytics import YOLO

model = YOLO("yolov8n.pt")  

model.train(
    data="/content/TrainingData/data.yaml",
    epochs=1,               
    imgsz=640,
    device=0,
    batch=8, 
    half=True,
    augment=True,
    cache=True,             
    patience=10,            
    save_period=10,         
    save_hybrid=True,
    save_txt=True,
    save=True,
    exist_ok=True, 
    name="train_yolo_wt",
    project="/content/runs" 
)
