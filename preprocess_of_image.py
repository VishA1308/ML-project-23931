from PIL import Image, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
import cv2

def get_parametres_from_image(img):
    img_array = np.array(img)
    mean_brightness = np.mean(img_array)  # средняя яркость
    std_brightness = np.std(img_array)  # отклонение от среднего
    
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

def make_image(img_tmp, adjust_type=0,brightness_adjustment =1, contrast_adjustment=1):
    if adjust_type == 1:  # Изменить только яркость
        img = ImageEnhance.Brightness(img_tmp).enhance(brightness_adjustment)
        img.save(f'Brightness-{contrast_adjustment}.jpg')
        return img

    elif adjust_type == 2:  # Изменить только контрастность
        img = ImageEnhance.Contrast(img_tmp).enhance(contrast_adjustment)
        img.save(f'Contrast-{contrast_adjustment}.jpg')
        return img

    elif adjust_type == 3:  # Изменить и яркость, и коValueError: image has wrong modeнтрастность
        img_brightness = ImageEnhance.Brightness(img_tmp).enhance(brightness_adjustment)
        img_contrast = ImageEnhance.Contrast(img_brightness).enhance(contrast_adjustment)
        img_contrast.save(f'Contrast_and_Brightness-{contrast_adjustment}.jpg')
        print('Измененное изображение сохранено как "Contrast_and_Brightness-{contrast_adjustment}.jpg"\n')
        return img_contrast

    else:
        print("Error")

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
