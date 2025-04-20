import re

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

# image_path = "templates/passive.jpg"
# ground_truth_path = 'templates/texts/passive.txt'

# with open(ground_truth_path, 'r', encoding='utf-8') as file:
#         ground_truth_text = file.read()

# predicted_text = get_text(image_path)

# print(calculate_metrics(predicted_text, ground_truth_text))

# help(normalize_text)