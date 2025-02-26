from PIL import Image, ImageEnhance
import numpy as np
import cv2

def get_parametres_from_image(img):
    img_array = np.array(img)
    mean_brightness = np.mean(img_array)
    std_brightness = np.std(img_array)
    
    return mean_brightness, std_brightness

def analyze_image(mean_brightness, std_brightness):
    flag_brightness = 0
    flag_contrast = 0
    
    if mean_brightness < 100:
        brightness_adjustment = 2  
        adjust_type = 1
        flag_brightness = 1
    elif mean_brightness > 150:
        brightness_adjustment = 0.5
        adjust_type = 1
        flag_brightness = 1
    else:
        brightness_adjustment = 1
        
    
    if std_brightness < 50:
        contrast_adjustment = 2  
        adjust_type = 2
        flag_contrast = 1
    elif std_brightness > 150:
        contrast_adjustment = 0.5  
        adjust_type = 2
        flag_contrast = 1
    else:
        contrast_adjustment = 1

    if (flag_contrast == 1 and flag_brightness == 1):
        adjust_type = 3

    return contrast_adjustment, brightness_adjustment, adjust_type

def adaptive_bilateral_filter(image):
    height, width = image.shape[:2]
    num_pixels = height * width

    mean_color = np.mean(image, axis=(0, 1))
    std_color = np.std(image, axis=(0, 1))
    avg_std_color = np.mean(std_color)

    d = max(5, min(width, height) // 10)
    sigmaColor = int(avg_std_color * 2)
    sigmaSpace = max(5, min(width, height) // 20)

    filtered_image = cv2.bilateralFilter(image, d=d, sigmaColor=sigmaColor, sigmaSpace=sigmaSpace)

    return filtered_image


def make_image(img, adjust_type=0,brightness_adjustment =1, contrast_adjustment=1):
    if adjust_type == 1:  # Изменить только яркость
        img = ImageEnhance.Brightness(img).enhance(brightness_adjustment)
        img.save(f'Brightness-{contrast_adjustment}.jpg')

    elif adjust_type == 2:  # Изменить только контрастность
        img = ImageEnhance.Contrast(img).enhance(contrast_adjustment)
        img.save(f'Contrast-{contrast_adjustment}.jpg')

    elif adjust_type == 3:  # Изменить и яркость, и контрастность
        img_brightness = ImageEnhance.Brightness(img).enhance(brightness_adjustment)
        img = ImageEnhance.Contrast(img_brightness).enhance(contrast_adjustment)
        img.save(f'Contrast_and_Brightness-{contrast_adjustment}.jpg')
    else:
        print("Error")
    img = np.array(img)
    img = adaptive_bilateral_filter(img) 
    return img

#input_image_path = r'C:\\Users\\Alise\\Documents\Проект ML\\ex1.jpg'
input_image_path = 'templates/picture1.jpg'

image_orig = Image.open(input_image_path)
image_orig.save('original_image.jpg')
print('Оригинальное изображение сохранено как "original_image.jpg"\n')

image_path = input_image_path
image_cv2 = cv2.imread(image_path)
gray_image = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)
img = Image.fromarray(gray_image)

mean_brightness, std_brightness = get_parametres_from_image(img)
print(f"Средняя яркость: {mean_brightness}, Стандартное отклонение яркости: {std_brightness}\n")

contrast_adjustment, brightness_adjustment, adjust_type = analyze_image(mean_brightness, std_brightness)

res_img = make_image(img, adjust_type=3,
                     contrast_adjustment=contrast_adjustment,
                     brightness_adjustment = brightness_adjustment)

