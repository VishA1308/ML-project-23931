from tesseract_test import get_text
from ustranenie_in_text import filter_text

image_path = 'templates/vitD.jpg'

result_text = get_text(image_path)

print(result_text)