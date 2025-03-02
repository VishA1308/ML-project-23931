import pytesseract
from PIL import Image

from preprocess_of_image import *
from ustranenie_in_text import *


image_path = 'test_images/vitD.jpg'
image = cv2.imread(image_path, 0)
img = Image.fromarray(image)

processed_image = make_image(img)

string = pytesseract.image_to_string(processed_image, lang='rus', config='--psm 6')

print(string)