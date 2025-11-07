import os

def ReadFromFile(file_path):
    if not os.path.exists(file_path):
        return None  # brak pliku
    with open(file_path, "r") as f:
        line = f.readline().strip()
        return line