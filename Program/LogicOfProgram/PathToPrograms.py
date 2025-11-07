from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
logic_of_program = base_dir  / "LogicOfProgram"

# print(base_dir)

scale_folder = logic_of_program / "scale"
scale_folder.mkdir(parents=True, exist_ok=True)
scale_path = scale_folder / "scale.txt"

meters_folder = logic_of_program / "meters"
meters_folder.mkdir(parents=True, exist_ok=True)
meters_path = meters_folder / "meters.txt"

settings_folder = logic_of_program / "settings"
settings_folder.mkdir(parents=True, exist_ok=True)
settings_path = settings_folder / "settings.txt"

captures_folder = logic_of_program / "captures" 
captures_folder.mkdir(parents=True, exist_ok=True)
captures_path = captures_folder / "capture.png"

prediction_folder = logic_of_program / "captures" / "wyniki"
prediction_folder.mkdir(parents=True, exist_ok=True)
prediction_path = prediction_folder / "prediction.txt"

project_root = logic_of_program.parent
file = "train_yolo_wt"

model_folder = project_root / "runs" / "detect" / file / "weights"
model_folder.mkdir(parents=True, exist_ok=True)
model_path = model_folder / "last.pt"

photo_folder = base_dir / "photo"
photo_folder.mkdir(parents=True, exist_ok=True)
photo_path = photo_folder / "image.png"

MetersPerPx_folder = base_dir / "FindValueOfMetersPerPx"
MetersPerPx_folder.mkdir(parents=True, exist_ok=True)
MetersPerPx_path = MetersPerPx_folder / "result" / "result.txt"

Letters_various_resolution_folder= base_dir / "LettersForVariuousResolutions"
Letters_various_resolution_folder.mkdir(parents=True, exist_ok=True) 

def Letters_various_func(number: int):
    folder= Letters_various_resolution_folder / f"res{number}"
    folder.mkdir(parents=True, exist_ok=True)

def Letters_return_func(number: int):
    folder= Letters_various_resolution_folder / f"res{number}"
    folder.mkdir(parents=True, exist_ok=True)
    B_path=folder/"B.png"
    D_path=folder/"D.png"
    F_path=folder/"F.png"
    return B_path, D_path, F_path

