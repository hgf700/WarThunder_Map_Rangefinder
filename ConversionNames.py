import os

folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\TrainingData\ManagingData"
prefix = "map_"   # nowa nazwa + numer
ext = ".jpg"      # rozszerzenie plików
new=".png"

files = sorted(os.listdir(folder))  # sortowanie alfabetyczne
for i, file in enumerate(files):
    if file.endswith(ext):
        old_path = os.path.join(folder, file)
        new_name = f"{prefix}{i+1:03d}{new}"  # np. map_001.png
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        print(f"{file} -> {new_name}")
