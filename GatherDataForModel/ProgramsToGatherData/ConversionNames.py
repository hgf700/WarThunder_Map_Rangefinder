import os

# folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\ManagingData\fragmentsNew\ucz"
# folder = r"C:\Users\USER098\Desktop\WT_SS_data"
# folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\TrainingData\images\train"
# folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\TrainingData\labels\train"
folder = r"C:\Users\USER098\Desktop\nowe1"

prefix = "map_" 
ext = ".png"

# files = sorted([f for f in os.listdir(folder)])  # tylko .txt convert
# ext = ".txt"

files = sorted([f for f in os.listdir(folder) if f.endswith(ext)])  # tylko .png

starti=1548

for index, file in enumerate(files, start=starti):  
    old_path = os.path.join(folder, file)
    new_name = f"{prefix}{index:04d}{ext}"  # np. map_072.png
    new_path = os.path.join(folder, new_name)
    os.rename(old_path, new_path)
    print(f"{file} -> {new_name}")
