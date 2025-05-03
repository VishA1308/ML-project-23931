import json

from tesseract_test import get_text
from ustranenie_in_text import filter_text

image_path = 'templates/vitD.jpg'

rec_text = get_text(image_path)
filt_text = filter_text(rec_text)

response_dict = {"text": filt_text}

with open('response.json', 'w+') as file:
    json.dump(response_dict, file)