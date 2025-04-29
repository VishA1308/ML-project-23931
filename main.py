from tesseract_test import get_text
from ustranenie_in_text import filter_text
from converter_pdf import convert_to_png
import os

image_path = r'C:\\Project ML\\test main\\image'  
output_directory = r'C:\\Project ML\\test main\\img_png' 


convert_to_png(image_path, output_directory)

# Обработка изображений в выходной директории
for image in os.listdir(output_directory):

    image_full_path = os.path.join(output_directory, image)
    
    # Проверяем, что файл является изображением
    if image.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        result_text = get_text(image_full_path)  
        print(result_text)
        print(filter_text(result_text))

