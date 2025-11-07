#generate .txt files 
import os
import cv2

# folder ze screenshotami


folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\ManagingData\fragmentsNew\ucz"
# folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\ManagingData\edytowaneZdj\nowe"
output_folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\ManagingData\labels\nowe\ucz"
os.makedirs(output_folder, exist_ok=True)

for i, file_name in enumerate(os.listdir(folder)):
    if file_name.endswith(".png"):
        # wczytanie obrazu (opcjonalne, tylko sprawdzenie)
        path = os.path.join(folder, file_name)
        img = cv2.imread(path)
        if img is None:
            print(f"Nie udało się wczytać {file_name}")
            continue

        # nazwa pliku txt taka sama jak obrazka
        base_name = os.path.splitext(file_name)[0]  # np. "map_001"
        txt_path = os.path.join(output_folder, f"{base_name}.txt")

        # tworzymy pusty plik txt
        with open(txt_path, 'w', encoding='utf-8') as f:
            pass

        print(f"Utworzono {txt_path}")

cv2.destroyAllWindows()
