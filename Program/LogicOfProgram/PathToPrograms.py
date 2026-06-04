import sys
from pathlib import Path

APP_ROOT = Path(sys.argv[0]).resolve().parent

if hasattr(sys, "_MEIPASS"):
    DATA_PATH = APP_ROOT / "_internal"
    
else:
    DATA_PATH = Path(__file__).resolve().parents[2]  # root projektu

def resource_path(relative: str | Path) -> Path:
    return DATA_PATH / relative

model_path = resource_path(f"{DATA_PATH}/Program/train_yolo_wt/weights/best.pt")
letters_root = resource_path(f"{DATA_PATH}/Program/LettersForVariuousResolutions")

def Letters_return_func(number: int):
    folder = letters_root / f"res{number}"
    return folder / "B.png", folder / "D.png", folder / "F.png"

data_root = DATA_PATH / "Program" /"LogicOfProgram"
data_root.mkdir(exist_ok=True)

scale_folder = data_root / "scale"
scale_folder.mkdir(exist_ok=True)
scale_path = scale_folder / "scale.txt"

meters_folder = data_root / "meters"
meters_folder.mkdir(exist_ok=True)
meters_path = meters_folder / "meters.txt"

settings_folder = data_root / "settings"
settings_folder.mkdir(exist_ok=True)
settings_path = settings_folder / "settings.txt"

prediction_folder = data_root / "prediction"
prediction_folder.mkdir(exist_ok=True)
prediction_raw_path = prediction_folder / "capture.png"
prediction_path = prediction_folder / "prediction.txt"
cleanPhoto_raw_path = prediction_folder / "cleanPhoto.png"

tresholding_folder = data_root / "thresholding"
tresholding_folder.mkdir(exist_ok=True)
tresholding_TXT_path = tresholding_folder / "thresholding.txt"
tresholding_PNG_path = tresholding_folder / "tresholded.png"

PxPerMapSquare_folder = data_root / "PxPerMapSquare"
PxPerMapSquare_folder.mkdir(exist_ok=True)
PxPerMapSquare_path = PxPerMapSquare_folder / "result.txt"
