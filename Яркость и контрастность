from PIL import Image, ImageEnhance
import numpy as np

def analyze_image(input_image_path):
    img = Image.open(input_image_path)  
    img_array = np.array(img)
    mean_brightness = np.mean(img_array)  # средняя яркость
    std_brightness = np.std(img_array)  # отклонение от среднего
    
    return mean_brightness, std_brightness

def make_image(input_image_path, adjust_type=0,brightness_adjustment =1, contrast_adjustment=1):
    img_tmp = Image.open(input_image_path)
    img_tmp.save('original_image.jpg')

    if adjust_type == 1:  # Изменить только яркость
        img = ImageEnhance.Brightness(img_tmp).enhance(brightness_adjustment)
        img.save(f'Brightness-{contrast_adjustment}.jpg')

    elif adjust_type == 2:  # Изменить только контрастность
        img = ImageEnhance.Contrast(img_tmp).enhance(contrast_adjustment)
        img.save(f'Contrast-{contrast_adjustment}.jpg')

    elif adjust_type == 3:  # Изменить и яркость, и контрастность
        img_brightness = ImageEnhance.Brightness(img_tmp).enhance(brightness_adjustment)
        img_contrast = ImageEnhance.Contrast(img_brightness).enhance(contrast_adjustment)
        img_contrast.save(f'Contrast_and_Brightness-{contrast_adjustment}.jpg')

    else:
        print("Error")

input_image_path = r'C:\\Users\\Alise\\Documents\Проект ML\\ex1.jpg'
mean_brightness, std_brightness = analyze_image(input_image_path)
print(f"Средняя яркость: {mean_brightness}, Стандартное отклонение яркости: {std_brightness}")

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

    
print(adjust_type)

make_image(input_image_path, adjust_type=adjust_type, contrast_adjustment=contrast_adjustment,brightness_adjustment = brightness_adjustment )
