import re

from jiwer import wer, mer, cer

from tesseract_test import get_text


def normalize_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation (keeps letters, numbers, and whitespace)
    text = re.sub(r'[^\w\s]', '', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing spaces
    text = text.strip()
    return text


image_path = "templates/passive.jpg"
predicted_text = get_text(image_path)

with open('templates/texts/passive.txt', 'r', encoding='utf-8') as file:
    ground_truth_text = file.read()


ground_truth_text = normalize_text(ground_truth_text)
predicted_text = normalize_text(predicted_text)


word_error = wer(ground_truth_text, predicted_text)
print("word error - ", word_error)

character_error = cer(ground_truth_text, predicted_text)
print("character error - ", character_error)

matсh_error = mer(ground_truth_text, predicted_text)
print("match error - ", matсh_error)
