from PIL import Image, ImageEnhance
import numpy as np
<<<<<<< HEAD
import cv2
import os
=======
import cv2 as cv
>>>>>>> 000044c5a4f2a2f116e1995fa70a0704cfc72184

def get_parametres_from_image(img):
    img_mean = np.mean(img)
    img_std = np.std(img)
    return img_mean, img_std 

def analyze_image(mean_brightness, std_brightness):
    adjust_type = 0
    flag_brightness = 0
    flag_contrast = 0
    adjust_type = 0
    if mean_brightness < 100:
        brightness = 2  
        adjust_type = 1
        flag_brightness = 1
    elif mean_brightness > 150:
        brightness = 0.5
        adjust_type = 1
        flag_brightness = 1
    else:
        brightness = 1
        
    
    if std_brightness < 50:
        contrast = 2  
        adjust_type = 2
        flag_contrast = 1
    elif std_brightness > 150:
        contrast = 0.5  
        adjust_type = 2
        flag_contrast = 1
    else:
        contrast = 1

    if (flag_contrast == 1 and flag_brightness == 1):
        adjust_type = 3

    return contrast, brightness, adjust_type

def calculate_temp(contrast):
    return (1 + contrast * 5 / 130)

def adaptive_bilateral_filter(image):
    height, width = image.shape[:2]

    std_color = np.std(image, axis=(0, 1))
    avg_std_color = np.mean(std_color)

    contrast = np.std(image)

    print(f'Контрастность: {contrast}\n')

    temp = calculate_temp(contrast)
    d = int(max(5, min(width, height) // 10) / temp)
    sigmaColor = int(max(10, int(avg_std_color * 2)) / temp)
    sigmaSpace = int(max(5, min(width, height) // 20) / temp)

    filtered_image = cv.bilateralFilter(image, d=d, sigmaColor=sigmaColor, sigmaSpace=sigmaSpace)

    return filtered_image

def make_image(img, adjust_type=0, brightness=1, contrast=1):
    img = Image.fromarray(img)
    if adjust_type == 1:  # Изменить только яркость
        img = ImageEnhance.Brightness(img).enhance(brightness)

    elif adjust_type == 2:  # Изменить только контрастность
        img = ImageEnhance.Contrast(img).enhance(contrast)

    elif adjust_type == 3:  # Изменить и яркость, и контрастность
<<<<<<< HEAD
        img_brightness = ImageEnhance.Brightness(img).enhance(brightness)
        img = ImageEnhance.Contrast(img_brightness).enhance(contrast)
=======
        img_brightness = ImageEnhance.Brightness(img).enhance(brightness_adjustment)
        img = ImageEnhance.Contrast(img_brightness).enhance(contrast_adjustment)
        img.save(f'Contrast_and_Brightness-{contrast_adjustment}.jpg')
    else:
        print("Изменения не нужны")
        return img
>>>>>>> 000044c5a4f2a2f116e1995fa70a0704cfc72184
    img = np.array(img)
    img = adaptive_bilateral_filter(img) 
    return img

<<<<<<< HEAD
=======
input_image_path = 'ex1.jpg'
>>>>>>> 000044c5a4f2a2f116e1995fa70a0704cfc72184

files = os.listdir('templates/')

<<<<<<< HEAD
for file in files:
    image = cv2.cvtColor(cv2.imread(f'templates/{file}'), cv2.COLOR_BGR2GRAY)
    img_mean, img_std = get_parametres_from_image(image)
    print(f"Средняя яркость: {img_mean}, Стандартное отклонение яркости: {img_std}")
=======
image_path = input_image_path
image_cv2 = cv.imread(image_path)
gray_image = cv.cvtColor(image_cv2, cv.COLOR_BGR2GRAY)
img = Image.fromarray(gray_image)


mean_brightness, std_brightness= get_parametres_from_image(img)
print(f"Средняя яркость: {mean_brightness}, Стандартное отклонение яркости: {std_brightness}\n")

contrast_adjustment, brightness_adjustment, adjust_type = analyze_image(mean_brightness, std_brightness)

res_img = make_image(img, adjust_type= adjust_type,
                     contrast_adjustment=contrast_adjustment,
                     brightness_adjustment = brightness_adjustment)
>>>>>>> 000044c5a4f2a2f116e1995fa70a0704cfc72184

    contrast, brightness, adjust_type = analyze_image(img_mean, img_std)
    res_img = make_image(image, adjust_type = adjust_type, brightness = brightness)
    cv2.imwrite(f'res/{file}', res_img)
