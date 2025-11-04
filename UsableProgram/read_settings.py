import os

# folder_path = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\settings"
# os.makedirs(folder_path, exist_ok=True)
# file_path = os.path.join(folder_path, "settings.txt")

def read_settings(file_path):
    if not os.path.exists(file_path):
        return None  # brak pliku
    with open(file_path, "r") as f:
        line = f.readline().strip()
        return line