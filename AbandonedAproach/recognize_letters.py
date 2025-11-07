import cv2
import numpy as np
import os

img_path = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\photo\image.png"
save_folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\concepts\save"
match_folder = r"C:\Users\USER098\Documents\GitHub\balistic-calculator-WT\concepts\match"

os.makedirs(save_folder, exist_ok=True)
os.makedirs(match_folder, exist_ok=True)

# --- create template (letter A) dynamically ---
font = cv2.FONT_HERSHEY_SIMPLEX
letter = 'b'

# create single-channel (grayscale) template, draw letter on it
template_h, template_w = 50, 40
template = np.zeros((template_h, template_w), dtype=np.uint8)
cv2.putText(template, letter, (5, 40), font, 1.5, 255, 2, cv2.LINE_AA)

template_path = os.path.join(save_folder, "template_A.png")
cv2.imwrite(template_path, template)

# --- load target image and convert to grayscale ---
image_bgr = cv2.imread(img_path)
if image_bgr is None:
    raise FileNotFoundError(f"Image not found: {img_path}")

image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

# optional: preprocess (increase contrast / threshold) to help matching
# thresh = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                cv2.THRESH_BINARY, 11, 2)
# use image_gray or thresh depending on results:
search_image = image_gray  # or use thresh

# --- template matching ---
res = cv2.matchTemplate(search_image, template, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

print(f"Best match value: {max_val:.3f} at {max_loc}")

# threshold to consider a valid match (adjust between 0.5..0.9)
threshold = 0.4
result_path = os.path.join(match_folder, "match_result.png")

if max_val >= threshold:
    top_left = max_loc  # (x, y)
    bottom_right = (top_left[0] + template_w, top_left[1] + template_h)
    # draw rectangle on original BGR image for visualization
    cv2.rectangle(image_bgr, top_left, bottom_right, (0, 255, 0), 2)
    cv2.imwrite(result_path, image_bgr)
    print(f"Letter A found. Result saved to: {result_path}")
else:
    print("Letter A not found with sufficient confidence. Try lowering threshold or preprocessing.")
