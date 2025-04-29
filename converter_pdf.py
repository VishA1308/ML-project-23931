from pdf2image import convert_from_path
from PIL import Image
import os

def convert_to_png(input_dir, output_dir):
    
    os.makedirs(output_dir, exist_ok=True)

    
    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        file_extension = os.path.splitext(file_name)[1].lower()

        if file_extension == '.pdf':
            # Конвертируем PDF в изображения
            images = convert_from_path(file_path)
            for i in range(len(images)):
                output_file = os.path.join(output_dir, f"{os.path.basename(file_path)[:-4]}_page{i}.png")
                images[i].save(output_file, 'PNG')

        elif file_extension in ['.jpg', '.jpeg', '.bmp']:
            # Конвертируем изображения в PNG
            with Image.open(file_path) as img:
                output_file = os.path.join(output_dir, f"{os.path.basename(file_path)[:-len(file_extension)]}.png")
                img.save(output_file, 'PNG')


