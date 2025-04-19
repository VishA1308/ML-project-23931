from PIL import Image, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
import cv2

def get_parametres(img):
    img = np.array(img)
    img_mean = np.mean(img)
    img_std = np.std(img)

    return img_mean, img_std

def calculate_temp(contrast):
    return (1 + contrast * 5 / 130)

def adaptive_bilateral_filter(image):
    height, width = image.shape[:2]
    std_color = np.std(image, axis=(0, 1))
    avg_std_color = np.mean(std_color)
    contrast = np.std(image)
    temp = calculate_temp(contrast)
    d = int(max(5, min(width, height) // 10) / temp)
    sigmaColor = int(max(10, int(avg_std_color * 2)) / temp)
    sigmaSpace = int(max(5, min(width, height) // 20) / temp)
    filtered_image = cv2.bilateralFilter(image, d=d, sigmaColor=sigmaColor, sigmaSpace=sigmaSpace)
    return filtered_image


def process_image(image_path, output_path):

    brightness, contrast = needs_processing(image_path)
        
    
    
    if (contrast == 1 or contrast == 1):
        
        img = Image.open(image_path)
        bw_img = img.convert('L')

        
        if (brightness == 1):
            print("Нужна обработка яркости")
            img_array = np.array(bw_img)
            mean_brightness = np.mean(img_array)
            
            if mean_brightness < 50:
                brightness_adjustment = 1 + (50 - mean_brightness) / 100  # Увеличиваем яркость
                
            elif mean_brightness > 100:
                brightness_adjustment = 1 - (mean_brightness - 100) / 100  # Уменьшаем яркость
            else:
                brightness_adjustment = 1
                
            enhancer = ImageEnhance.Brightness(bw_img)
            bw_img = enhancer.enhance(brightness_adjustment)

        print("Нужна обработка контрастности")
        
        img_array = np.array(bw_img)

        # Находим максимальное значение пикселей 
        max_value = np.max(img_array[img_array > 0])

        new_img_array = np.zeros_like(img_array)

        # Приводим значения к диапазону [0, max_value]
        if max_value > 0:  
           new_img_array[img_array > 0] = (img_array[img_array > 0] / max_value) * max_value
      
        new_img_array = new_img_array.astype(np.uint8)

    
        result_img = Image.fromarray(new_img_array)

        result_img_2 = np.array(result_img)
        result_img_2 = adaptive_bilateral_filter(result_img_2)
        result_img.save(output_path)

        display_images(img, result_img, result_img_2)
        return result_img_2
    
    else:
        
        print("Не нужна обработка")
        img = Image.open(image_path)
        bw_img = img.convert('L')

        img_array = np.array(bw_img)
        result_img = Image.fromarray(img_array)

        result_img_2 = np.array(result_img)
        result_img_2 = adaptive_bilateral_filter(result_img_2)
        result_img.save(output_path)

        display_images(img, result_img, result_img_2)
        return result_img_2
    




def needs_processing(image_path):
    brightness = 0
    contrast = 0
    img = Image.open(image_path)
    bw_img = img.convert('L')  
    img_array = np.array(bw_img)

    # Вычисляем среднее значение яркости и стандартное отклонение
    mean_brightness = np.mean(img_array)
    std_brightness = np.std(img_array)

    # Условия для определения необходимости обработки по яркости
    if mean_brightness < 50 or mean_brightness > 150 or std_brightness < 20:
        brightness = 1

    # Вычисляем гистограмму
    hist, _ = np.histogram(img_array.flatten(), bins=256, range=[0, 256])

    # Находим минимальное ненулевое значение и максимальное значение в гистограмме
    min_val = np.min(hist[hist > 0])
    max_val = np.max(hist)

    # Проверяем условия для необходимости обработки по гистограмме
    contrast_threshold_hist = 0.1 * max_val  
    if min_val < contrast_threshold_hist:
        contrast = 1


    return brightness, contrast






def process_image_with_shum(image_path, output_path):

    img = Image.open(image_path)
    
    
    bw_img = img.convert('L')

    img_array = np.array(bw_img)

    # Вычисляем среднее значение яркости
    mean_brightness = np.mean(img_array)

    # Корректировка яркости
    if mean_brightness < 100:
        brightness_adjustment = 1 + (100 - mean_brightness) / 100  # Увеличиваем яркость
    elif mean_brightness > 150:
        brightness_adjustment = 1 - (mean_brightness - 150) / 100  # Уменьшаем яркость
    else:
        brightness_adjustment = 1  # Без изменений

    # Обработка яркости
    enhancer = ImageEnhance.Brightness(bw_img)
    bw_img = enhancer.enhance(brightness_adjustment)  # Изменяем яркость

    img_array = np.array(bw_img)

    # Находим максимальное значение пикселей 
    max_value = np.max(img_array[img_array > 0])

    new_img_array = np.zeros_like(img_array)

    # Приводим значения к диапазону [0, max_value]
    if max_value > 0:  
        new_img_array[img_array > 0] = (img_array[img_array > 0] / max_value) * max_value
      
    new_img_array = new_img_array.astype(np.uint8)

    
    result_img = Image.fromarray(new_img_array)
    result_img_2 = np.array(result_img)
    result_img.save(output_path)
    
    return result_img_2


def display_images(original, processed, without_shum):
    plt.figure(figsize=(10, 5))
    

    plt.subplot(1, 3, 1)
    plt.imshow(original, cmap='gray')
    plt.title('Оригинальное изображение')
    plt.axis('off')  

    plt.subplot(1, 3, 2)
    plt.imshow(processed, cmap='gray')
    plt.title('Обработанное изображение c шумом')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(without_shum, cmap='gray')
    plt.title('Обработанное изображение')
    plt.axis('off')
    
    plt.show()





