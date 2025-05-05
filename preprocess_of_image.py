from PIL import Image, ImageEnhance
import numpy as np
import cv2
import os

def get_parametres(img: Image) -> tuple[float, float]:
    """
    Get standart deviation and mean of image

    Args:
        img: image to get parameters from
    
    Returns:
        (img_mean, img_std) (tuple[float, float]): standart deviation and mean of image
    """

    img = np.array(img)
    img_mean = np.mean(img)
    img_std = np.std(img)

    return img_mean, img_std

def calculate_temp(contrast: float) -> float:
    """
    Calculate value for blur
    """

    return (1 + contrast * 5 / 130)

def adaptive_bilateral_filter(image):
    """
    Find parametres for blur: shape, std, mean, blur-value, d, sigmaColor, sigmaSpace
    """
    
    height, width = image.shape[:2]
    std_color = np.std(image, axis=(0, 1))
    avg_std_color = np.mean(std_color)
    contrast = np.std(image)
    temp = calculate_temp(contrast)
    d = int(max(5, min(width, height) // 10) / temp)
    sigmaColor = int(max(10, int(avg_std_color * 2)) / temp)
    sigmaSpace = int(max(5, min(width, height) // 20) / temp)

    # Apply the filter 
    filtered_image = cv2.bilateralFilter(image, d=d, sigmaColor=sigmaColor, sigmaSpace=sigmaSpace)
    return filtered_image

def analyze_image(mean_brightness, std_brightness):
    flag_brightness = 0
    flag_contrast = 0
    
    # Корректировка яркости
    if mean_brightness < 100:
        brightness_adjustment = 1 + (50 - mean_brightness) / 100  # Увеличиваем яркость
        flag_brightness = 1
    elif mean_brightness > 250:
        brightness_adjustment = 1 - (mean_brightness - 250) / 100  # Уменьшаем яркость
        flag_brightness = 1
    else:
        brightness_adjustment = 1
        
    # Корректировка контрастности
    if std_brightness < 50:
        contrast_adjustment = 1 + (50 - std_brightness) / 100  # Увеличиваем контрастность
        flag_contrast = 1
    elif std_brightness > 150:
        contrast_adjustment = 1 - (std_brightness - 150) / 100  # Уменьшаем контрастность
        flag_contrast = 1
    else:
        contrast_adjustment = 1

    adjust_type = 0
    if flag_contrast and flag_brightness:
        adjust_type = 3
    elif flag_brightness:
        adjust_type = 1
    elif flag_contrast:
        adjust_type = 2

    return contrast_adjustment, brightness_adjustment, adjust_type

def make_image(img, adjust_type=0, brightness=1, contrast=1):
    brightness = max(0.5, min(brightness, 1.5))
    contrast = max(0.5, min(contrast, 1.5))

    if adjust_type == 1:  
        img = ImageEnhance.Brightness(img).enhance(brightness)

    elif adjust_type == 2:  
        img = ImageEnhance.Contrast(img).enhance(contrast)

    elif adjust_type == 3: 
        img_brightness = ImageEnhance.Brightness(img).enhance(brightness)
        img = ImageEnhance.Contrast(img_brightness).enhance(contrast)
    else:
        print("Изменения не нужны")
    
    img = np.array(img)
    img = adaptive_bilateral_filter(img) 
    return img

'''
files = os.listdir('templates/')
os.makedirs('res/', exist_ok=True)

for filename in files:
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        image = cv2.imread(f'templates/{filename}', cv2.IMREAD_GRAYSCALE)
        img_mean, img_std = get_parametres(image)
        contrast, brightness, adjust_type = analyze_image(img_mean, img_std)
        image = Image.fromarray(image)
        res_img = make_image(image, adjust_type=adjust_type, contrast=contrast, brightness=brightness)
        cv2.imwrite(f'res/{os.path.splitext(filename)[0]}.png', res_img)
'''