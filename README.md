# Task2

# Computer Vision – Weight Extraction from Weighing Scale

##  Problem Statement

**Goal:**  
Given an image of a digital weighing scale, the task is to extract and return the numerical weight displayed on the screen (e.g., `3.92`).

>  This task is not about building a scalable or efficient pipeline — it's about solving the problem quickly using existing technologies.

---

## 🔍 Approach

To solve the task efficiently, the following pipeline was implemented:

### 1. **Preprocessing (OpenCV)**
- **Grayscale Conversion**: Improves contrast for OCR
- **Otsu Thresholding**: Separates digits from the background
- **Noise Removal**: Median blur helps remove pixel-level noise
- **(Optional Deskewing)**: Corrects tilted images for better OCR accuracy

### 2. **OCR (Tesseract)**
- Used `pytesseract` with custom configuration:
  - `--oem 3`: Default LSTM OCR engine
  - `--psm 6`: Assume a single uniform block of text
- Extracted raw text from the preprocessed image

### 3. **Postprocessing**
- Cleaned up OCR output
- Used regex (`\b\d+\.\d+\b`) to extract valid decimal numbers like `3.92`
- Returned the first valid positive match as the weight

---

## Tools & Libraries Used

- Python
- OpenCV (`cv2`)
- NumPy
- Tesseract OCR via `pytesseract`
- Regular Expressions (`re`)

---

##  Example Output

Given the image below:
![Sample Weighing Scale](image.png)

The console output will be:
