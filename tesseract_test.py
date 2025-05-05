import pytesseract
from PIL import Image
import cv2

from preprocess_of_image import make_image, analyze_image, get_parametres

def get_text(image_path: str) -> str:
    """
    Recognises text on the image and returns a result string.

    Args:
        image_path (str): path to the image in string format.
    
    Returns:
        string (str): recognised with pytesseract text from image
    """ 
    image = cv2.imread(image_path, 0) # read image in gray-scale
    image = Image.fromarray(image) # convertation for further processing

    # Extracting parameters for preprocessing
    mean_bright, std_bright= get_parametres(image)
    contr_adj, bright_adj, adj_type = analyze_image(mean_bright, std_bright)

    # Preprocessing
    processed_image = make_image(image, adj_type, 
                                 bright_adj, 
                                 contr_adj)
    
    # Implementing pyteseract to recognise text
    # --psm 6 - assume a single uniform block of text
    string = pytesseract.image_to_string(processed_image, 
                                         lang='rus+eng',
                                         config='--psm 6')
    
    return string