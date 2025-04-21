import cv2
import numpy as np
import pytesseract
from PIL import Image
from skimage.filters import threshold_sauvola
from spellchecker import SpellChecker 

from preprocess_of_image import make_image, analyze_image, get_parametres

image_path = 'templates/analiz_3.jpg'
image = cv2.imread(image_path, 0) # read image in gray-scale
scale_percent = 200  # Increase for small text (200% works well for 300dpi scans)
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)

# Extracting parameters for preprocessing
mean_bright, std_bright = get_parametres(image)
contr_adj, bright_adj, adj_type = analyze_image(mean_bright, std_bright)

# Preprocessing
processed_image = make_image(Image.fromarray(image), adj_type, 
                                bright_adj, 
                                contr_adj)

clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
enhanced = clahe.apply(processed_image)

thresh_sauvola = threshold_sauvola(enhanced, window_size=25)
binary = (enhanced > thresh_sauvola).astype(np.uint8) * 255

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel, iterations=1)

final = cv2.edgePreservingFilter(morph, flags=1, sigma_s=60, sigma_r=0.4)


# threshold for text segmentation
# adaptive_thresh = cv2.adaptiveThreshold(
#     processed_image, 255,
#     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#     cv2.THRESH_BINARY_INV, 21, 10
# )
# _, binary_image = cv2.threshold(adaptive_thresh, 100, 255, cv2.THRESH_BINARY_INV)

# contours
contours, _ = cv2.findContours(255-final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# contours, _ = cv2.findContours(adaptive_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# recognise text in all contours
recognized_texts = []
print(f"Number of contours found: {len(contours)}")
image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)
for contour in contours:
    # bounding coordinates of text
    x, y, w, h = cv2.boundingRect(contour)
    cropped_image = image[y:y+h, x:x+w]

    bordered = cv2.copyMakeBorder(
        cropped_image, 10, 10, 10, 10,
        cv2.BORDER_CONSTANT,
        value=[255, 255, 255]
    )

    scaled = cv2.resize(bordered, None, fx=2, fy=2, 
                        interpolation=cv2.INTER_CUBIC)
    # recognition on cropped part
    text = pytesseract.image_to_string(
        Image.fromarray(scaled), 
        config='-l rus+eng'
    ).strip()
    
    if text:
        recognized_texts.append(text)
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 1)

# visualization
print("Распознанный текст:", ' '.join(recognized_texts))

cv2.imshow('Image with Contours', image)
cv2.imshow('binary', final)
cv2.waitKey(0)
cv2.destroyAllWindows()
