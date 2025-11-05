from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
usable_program = base_dir / "UsableProgram"

prediction_folder = usable_program / "captures" / "wyniki"
prediction_folder.mkdir(parents=True, exist_ok=True)
prediction_path = prediction_folder / "prediction.txt"

settings_folder = usable_program / "settings"
settings_folder.mkdir(parents=True, exist_ok=True)
settings_path = settings_folder / "settings.txt"

scale_folder = usable_program / "scale"
scale_folder.mkdir(parents=True, exist_ok=True)
scale_path = scale_folder / "scale.txt"

meters_folder = usable_program / "meters"
meters_folder.mkdir(parents=True, exist_ok=True)
meters_path = meters_folder / "meters.txt"
