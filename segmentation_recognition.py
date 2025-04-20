import cv2
import pytesseract
from PIL import Image

from preprocess_of_image import make_image, analyze_image, get_parametres

image_path = 'templates/analiz_2.jpg'
image = cv2.imread(image_path, 0) # read image in gray-scale
# image = Image.fromarray(image) # convertation for further processing

# Extracting parameters for preprocessing
mean_bright, std_bright = get_parametres(image)
contr_adj, bright_adj, adj_type = analyze_image(mean_bright, std_bright)

# Preprocessing
processed_image = make_image(Image.fromarray(image), adj_type, 
                                bright_adj, 
                                contr_adj)

# threshold for text segmentation
adaptive_thresh = cv2.adaptiveThreshold(
    processed_image, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV, 15, 5
)
# _, binary_image = cv2.threshold(adaptive_thresh, 100, 255, cv2.THRESH_BINARY_INV)

# contours
contours, _ = cv2.findContours(adaptive_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# recognise text in all contours
recognized_texts = []
print(f"Number of contours found: {len(contours)}")
image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
for contour in contours:
    # bounding coordinates of text
    x, y, w, h = cv2.boundingRect(contour)
    cropped_image = image[y:y+h, x:x+w]

    # recognition on cropped part
    text = pytesseract.image_to_string(Image.fromarray(cropped_image), lang='rus+eng', config="--psm 10")
    recognized_texts.append(text.strip())

    # drawing bounding box
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 1)

# visualization
print("Распознанный текст:", ' '.join(recognized_texts))

cv2.imshow('Image with Contours', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
