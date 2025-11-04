import os

def read_settings(file_path):
    if not os.path.exists(file_path):
        return None  # brak pliku
    with open(file_path, "r") as f:
        line = f.readline().strip()
        return line