import os

folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\TrainingData\labels\val"
os.makedirs(folder, exist_ok=True)

for file_name in os.listdir(folder):
    if file_name.endswith(".txt"):
        path = os.path.join(folder, file_name)

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if len(lines) >= 3:
            del lines[2]

        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
