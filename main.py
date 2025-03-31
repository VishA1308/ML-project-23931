from tesseract_test import get_text
from ustranenie_in_text import filter_text

image_path = 'templates/esenin.jpg'

result_text = get_text(image_path) # processing of image, string in result

print(result_text)
print(filter_text(result_text)) # filter text from extra symbols

image_path = 'templates/vitD.jpg'

result_text = get_text(image_path) # processing of image, string in result

print(result_text)
print(filter_text(result_text)) # filter text from extra symbols

image_path = 'templates/hello_world.jpg'

result_text = get_text(image_path) # processing of image, string in result

print(result_text)
print(filter_text(result_text)) # filter text from extra symbols

image_path = 'templates/italic.jpg'

result_text = get_text(image_path) # processing of image, string in result

print(result_text)
print(filter_text(result_text)) # filter text from extra symbols
