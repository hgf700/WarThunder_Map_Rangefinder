import os

folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\ManagingData\edytowaneZdj\nowe"
prefix = "map_" 
ext = ".png"

files = sorted([f for f in os.listdir(folder) if f.endswith(ext)])  # tylko .png

for index, file in enumerate(files, start=72):  # zaczynasz od 72
    old_path = os.path.join(folder, file)
    new_name = f"{prefix}{index:03d}{ext}"  # np. map_072.png
    new_path = os.path.join(folder, new_name)
    os.rename(old_path, new_path)
    print(f"{file} -> {new_name}")
