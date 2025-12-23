from pathlib import Path
import sys

base_dir = Path(__file__).resolve().parent.parent
logic_of_program = base_dir  / "LogicOfProgram"

# print(base_dir)

# ─── ZASOBY (PyInstaller) ──────────────────────────────────
# APP_ROOT = Path(sys.argv[0]).resolve().parent
# if hasattr(sys, "_MEIPASS"):
#     RESOURCES_ROOT = Path(sys._MEIPASS)
# else:
#     RESOURCES_ROOT = APP_ROOT

# def resource_path(relative: str | Path) -> Path:
#     return RESOURCES_ROOT / relative

# model_path = resource_path("yolo_weights/last.pt")

# letters_root = resource_path("LettersForVariuousResolutions")

# def Letters_return_func(number: int):
#     folder = letters_root / f"res{number}"
#     return folder / "B.png", folder / "D.png", folder / "F.png"
# ─── Koniec ZASOBY (PyInstaller) ──────────────────────────────────

project_root = logic_of_program.parent
file = "train_yolo_wt"
model_folder = project_root / "runs" / "detect" / file / "weights"
model_folder.mkdir(parents=True, exist_ok=True)
model_path = model_folder / "last.pt"

scale_folder = logic_of_program / "scale"
# scale_folder.mkdir(parents=True, exist_ok=True)
scale_path = scale_folder / "scale.txt"

meters_folder = logic_of_program / "meters"
# meters_folder.mkdir(parents=True, exist_ok=True)
meters_path = meters_folder / "meters.txt"

settings_folder = logic_of_program / "settings"
# settings_folder.mkdir(parents=True, exist_ok=True)
settings_path = settings_folder / "settings.txt"

prediction_raw_folder = logic_of_program / "prediction" 
# prediction_raw_folder.mkdir(parents=True, exist_ok=True)
prediction_raw_path = prediction_raw_folder / "capture.png"
cleanPhoto_raw_path = prediction_raw_folder / "cleanPhoto.png"

prediction_folder = logic_of_program / "prediction" / "results"
# prediction_folder.mkdir(parents=True, exist_ok=True)
prediction_path = prediction_folder / "prediction.txt"

tresholding_folder = logic_of_program / "thresholding"
# tresholding_folder.mkdir(parents=True, exist_ok=True)
tresholding_TXT_path = tresholding_folder / "thresholding.txt"
tresholding_PNG_path = tresholding_folder / "tresholded.png"

PxPerMapSquare_folder = logic_of_program / "PxPerMapSquare"
# PxPerMapSquare_folder.mkdir(parents=True, exist_ok=True)
PxPerMapSquare_path = PxPerMapSquare_folder / "result.txt"

Letters_various_resolution_folder= base_dir / "LettersForVariuousResolutions"
# Letters_various_resolution_folder.mkdir(parents=True, exist_ok=True) 

def Letters_various_func(number: int):
    folder= Letters_various_resolution_folder / f"res{number}"
    # folder.mkdir(parents=True, exist_ok=True)

def Letters_return_func(number: int):
    folder= Letters_various_resolution_folder / f"res{number}"
    # folder.mkdir(parents=True, exist_ok=True)
    B_path=folder/"B.png"
    D_path=folder/"D.png"
    F_path=folder/"F.png"
    return B_path, D_path, F_path

