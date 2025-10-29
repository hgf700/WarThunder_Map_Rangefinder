import os

folder_path = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\settings"
os.makedirs(folder_path, exist_ok=True)
file_path = os.path.join(folder_path, "settings.txt")

def save_settings(width, height, x1, y1, x2, y2):
    """Zapisuje ustawienia do pliku"""
    with open(file_path, "w") as f:
        f.write(f"{width} {height} {x1} {y1} {x2} {y2}")

def read_settings():
    """Wczytuje ustawienia z pliku"""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        line = f.readline().strip()
        if not line:
            return None
        try:
            width, height, x1, y1, x2, y2 = map(int, line.split())
            return {"width": width, "height": height, "x1": x1, "y1": y1, "x2": x2, "y2": y2}
        except ValueError:
            return None
