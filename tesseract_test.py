import pytesseract
from PIL import Image


image = Image.open('vitD.png')
string = pytesseract.image_to_string(image, lang='rus', config='--psm 6')

print(string)