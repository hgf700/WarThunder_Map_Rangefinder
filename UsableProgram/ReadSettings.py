import os

folder_path = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\UsableProgram\settings"
os.makedirs(folder_path, exist_ok=True)
file_path = os.path.join(folder_path, "settings.txt")

def read_settings():
    if not os.path.exists(file_path):
        return None  # brak pliku
    with open(file_path, "r") as f:
        line = f.readline().strip()
        return line

settings = read_settings()
if settings:
    # Rozdzielenie wartości i zamiana na int
    values = list(map(int, settings.split()))
    if len(values) == 6:
        Width, Height, MiniMapStartX, MiniMapStartY, MiniMapEndX, MiniMapEndY = values
        print("Width:", Width)
        print("Height:", Height)
        print("MiniMapStartX:", MiniMapStartX)
        print("MiniMapStartY:", MiniMapStartY)
        print("MiniMapEndX:", MiniMapEndX)
        print("MiniMapEndY:", MiniMapEndY)
    else:
        print("Niepoprawna liczba wartości w pliku ustawień.")
else:
    print("Plik ustawień nie istnieje.")

line = input()