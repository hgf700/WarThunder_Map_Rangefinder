from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
logic_of_program = base_dir / "Program" / "LogicOfProgram"

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