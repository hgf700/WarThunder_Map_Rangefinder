import os

def ReadFromFile(file_path):
    # brak pliku
    if not os.path.exists(file_path):
        return None  
    with open(file_path, "r") as f:
        line = f.readline().strip()
        return line