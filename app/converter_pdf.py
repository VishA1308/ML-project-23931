from pdf2image import convert_from_path
from PIL import Image
def convert_to_png(input_file_path: str) -> str:
    output_file_path = tempfile.mktemp(suffix=".png")

    file_extension = os.path.splitext(input_file_path)[1].lower()

    if file_extension == '.pdf':
        # Конвертируем PDF в изображения
        images = convert_from_path(input_file_path)
        if images:
            images[0].save(output_file_path, 'PNG')  # Сохраняем только первую страницу
    elif file_extension in ['.jpg', '.jpeg', '.bmp']:
        # Конвертируем изображения в PNG
        with Image.open(input_file_path) as img:
            img.save(output_file_path, 'PNG')
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF or an image.")

    return output_file_path
