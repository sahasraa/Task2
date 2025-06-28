import cv2
import numpy as np
import pytesseract
import re

# preprocessing funcs

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def remove_noise(image):
    return cv2.medianBlur(image, 5)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def canny(image):
    return cv2.Canny(image, 100, 200)

def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def extract_weight_from_image(image_path):
    # Step 1: Read image
    image = cv2.imread(image_path)
    if image is None:
        print("Failed to load image.")
        return

    # Step 2: Preprocessing
    gray = get_grayscale(image)
    thresh = thresholding(gray)
    processed = remove_noise(thresh)

    # Step 3: OCR
    custom_config = r'--oem 3 --psm 6'
    raw_text = pytesseract.image_to_string(processed, config=custom_config)

    # Step 4: Clean and extract weight
    cleaned_text = raw_text.replace('\n', ' ').replace('\x0c', '').strip()
    matches = re.findall(r"\b\d+\.\d+\b", cleaned_text)

    print('-----------------------------------------')
    print('OCR Raw Output:\n', raw_text)
    print('-----------------------------------------')

    if matches:
        print("Extracted Weight:", matches[0])
    else:
        print("No valid positive weight found.")

if __name__ == "__main__":
    image_path = "image.png"  # Set your image file here
    extract_weight_from_image(image_path)
