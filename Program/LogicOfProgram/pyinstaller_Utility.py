import sys
from pathlib import Path

def resource_path(relative_path: str | Path) -> str:
    if hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    else:
        # folder gdzie jest main.py
        base_path = Path(sys.argv[0]).resolve().parent

    return str(base_path / relative_path)

