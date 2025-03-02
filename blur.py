from PIL import Image, ImageEnhance
import numpy as np
import cv2

def calculate_contrast(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contrast = np.std(gray)
    return contrast

def calculate_temp(contrast):
    return (1 + contrast * 5 / 130)

def adaptive_bilateral_filter(image):
    height, width = image.shape[:2]

    std_color = np.std(image, axis=(0, 1))
    avg_std_color = np.mean(std_color)

    contrast = calculate_contrast(image)

    print(contrast)

    temp = calculate_temp(contrast) / 1.5
    d = int(max(5, min(width, height) // 10) / temp)
    sigmaColor = int(max(10, int(avg_std_color * 2)) / temp)
    sigmaSpace = int(max(5, min(width, height) // 20) / temp)

    filtered_image = cv2.bilateralFilter(image, d=d, sigmaColor=sigmaColor, sigmaSpace=sigmaSpace)

    return filtered_image

for i in range(1, 5):
    image_cv2 = cv2.imread(f'image{i}.jpg')
    image = adaptive_bilateral_filter(image_cv2)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = Image.fromarray(gray_image)
    img.save(f'image{i}_r.jpg')


