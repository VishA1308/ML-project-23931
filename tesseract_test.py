import pytesseract
from PIL import Image
import cv2

from preprocess_of_image import process_image
from preprocess_of_image import process_image_with_shum

def get_text(image_path: str) -> str:
    """
    Recognises text on the image and returns a result string.

    image_text - path to the image in string format.
    """ 
    

    # Preprocessing
    processed_image = process_image(image_path , 'output_image.jpg')
    
    # Implementing pyteseract to recognise text
    # --psm 6 - assume a single uniform block of text
    string = pytesseract.image_to_string(processed_image, 
                                         lang='rus+eng',
                                         config='--psm 6')
    
    return string

def get_text_with_shum(image_path: str) -> str:
    """
    Recognises text on the image and returns a result string.

    image_text - path to the image in string format.
    """ 
    

    # Preprocessing
    processed_image = process_image_with_shum(image_path , 'output_image.jpg')
    
    # Implementing pyteseract to recognise text
    # --psm 6 - assume a single uniform block of text
    string = pytesseract.image_to_string(processed_image, 
                                         lang='rus+eng',
                                         config='--psm 6')
    
    return string
