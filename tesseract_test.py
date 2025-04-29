import pytesseract
from PIL import Image
import cv2

from preprocess_of_image import process_image

def get_text(image_path: str) -> str:
    """
    Recognises text on the image and returns a result string.

    image_text - path to the image in string format.
    """ 
    
    processed_image = process_image(image_path)
    

    string = pytesseract.image_to_string(processed_image, 
                                         lang='rus+eng',
                                         config='--psm 6')
    
    return string


