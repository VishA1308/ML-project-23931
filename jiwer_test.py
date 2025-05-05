import re
import os
import json

from jiwer import wer, mer, cer

from tesseract_test import get_text


def normalize_text(text: str) -> str:
    '''
    Converts to lowercase, removes punctuation, replaces multiple spaces.

    Args:
        text (str): text for normalisation
    
    Returns: 
        (str): normalized text
    '''

    text = text.lower()
    # Remove punctuation (keeps letters, numbers, and whitespace)
    text = re.sub(r'[^\w\s]', '', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing spaces
    text = text.strip()

    return text

def calculate_metrics(predicted_txt: str, ground_truth_txt: str) -> tuple[float, float, float]:
    """
    Normalizes both predicted and ground-truth texts, then calculates errors.

    Args: 
        predicted_txt (str): text to check for errors
        ground_truth_txt (str): text to consider as reference

    Returns:
        tuple[float, float, float]: Word Error Rate, Character Error Rate, Match Error Rate
    """

    # Normalise text
    norm_prediction = normalize_text(predicted_txt)
    norm_ground_truth = normalize_text(ground_truth_txt)

    # Calculate errors
    word_error = wer(norm_ground_truth, norm_prediction)
    character_error = cer(norm_ground_truth, norm_prediction)
    matсh_error = mer(norm_ground_truth, norm_prediction)

    return word_error, character_error, matсh_error


def extract_ground_truth():
    annots_dir = 'annots'
    annots = os.listdir(annots_dir)
    
    texts = {}

    for annot_file in annots:
        label_file = open(os.path.join(annots_dir, annot_file), "r")
        with label_file:
            
            labels = json.load(label_file) 
            for label_obj in labels:
                image_name = os.path.split(label_obj['data']['ocr'])[-1]
                
                for annotation in label_obj["annotations"]:
                    ground_truth_text = []
                    for result in annotation["result"]:
                        if "text" in result["value"]:
                            ground_truth_text.append(" ".join(result["value"]["text"]))
                    texts.update({f'{image_name}': ground_truth_text})
    
    with open('ground_truth_texts.json', 'w', encoding='utf-8') as filet:
        json.dump([texts], filet)

    return texts

# print(extract_ground_truth())

with open('ground_truth_texts.json', 'r') as filet:
        data = json.load(filet)

# image_path = "templates/passive.jpg"
# ground_truth_path = 'templates/texts/passive.txt'

# with open(ground_truth_path, 'r', encoding='utf-8') as file:
#         ground_truth_text = file.read()

# predicted_text = get_text(image_path)

# print(calculate_metrics(predicted_text, ground_truth_text))

# help(normalize_text)

image_dir = 'images'
images = os.listdir(image_dir)

metrics = {}
pred_texts = {}
truth_texts = {}

for img in images:
    img_path = os.path.join(image_dir, img)
    ground_truth_text = data[0][img]
    predicted_text = get_text(img_path)
    ground_truth_text = ' '.join(ground_truth_text)
    metrics.update({img: calculate_metrics(predicted_text, ground_truth_text)})
    pred_texts.update({img: predicted_text})
    truth_texts.update({img: ground_truth_text})

print(metrics)