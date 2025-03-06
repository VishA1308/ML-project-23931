import pytesseract
from PIL import Image
import cv2

from preprocess_of_image import make_image, analyze_image, get_parametres

def get_text(image_path):
    image = cv2.imread(image_path, 0) # read image in gray-scale
    image = Image.fromarray(image)

    mean_bright, std_bright= get_parametres(image)
    contr_adj, bright_adj, adj_type = analyze_image(mean_bright, std_bright)

    processed_image = make_image(image, adj_type, 
                                 bright_adj, 
                                 contr_adj)
    string = pytesseract.image_to_string(processed_image, 
                                         lang='rus+eng',
                                         config='--psm 6')
    
    return string

