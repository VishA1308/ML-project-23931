import os
import json
from argparse import ArgumentParser
import math
from hashlib import sha256
import cv2
from PIL import Image


def get_bbox_cords(value: dict, image_shape: list) -> dict:
    return {
        'x': int(math.floor(value['x'] / 100 * image_shape[1])),
        'y': int(math.floor(value['y'] / 100 * image_shape[0])),
        'width': int(math.ceil(value['width'] / 100 * image_shape[1])),
        'height': int(math.ceil(value['height'] / 100 * image_shape[0]))
    }

def add_box(text: str, bbox: dict, image_name: str, output_dir: str):
    """Create a .box file with character-level bounding boxes (simplified version)"""
    box_path = os.path.join(output_dir, f"{image_name}.box")
    
    # For simplicity, we'll create one box per character spanning the whole line
    # In a real scenario, you'd want proper character-level boxes
    with open(box_path, 'a', encoding='utf-8') as f:
        for i, char in enumerate(text):
            if char.strip():  # Skip whitespace characters
                f.write(f"{char} {bbox['x']} {bbox['y']} {bbox['x'] + bbox['width']} {bbox['y'] + bbox['height']} 0\n")


def main():
    save_dir = 'converter_res'
    os.makedirs(save_dir, exist_ok=True)
    
    sample_id = 0
    unique_texts = set()

    annots_dir = 'annots'
    annots = os.listdir(annots_dir)

    for annot_file in annots:
        label_file = open(os.path.join(annots_dir, annot_file), "r")
        with label_file:
            annotations = json.load(label_file)       
            for label_obj in annotations:
                
                image_name = os.path.split(label_obj['data']['ocr'])[-1][:-4]                

                for label_info in label_obj['annotations'][0]['result']:
                    if label_info['type'] == 'textarea':
                        text = label_info['value']['text'][0]
                        image_shape = (label_info['original_width'], 
                                        label_info['original_height'])
                        
                        # Skip duplicates
                        if text in unique_texts:
                            continue
                        unique_texts.add(text)
                        
                        # Get bounding box coordinates
                        bbox = get_bbox_cords(label_info['value'], image_shape)
                        
                        # Save in Tesseract format
                        add_box(text, bbox, image_name, save_dir)
                
                sample_id += 1
        
        print(f"Conversion complete. Saved {sample_id} samples to {save_dir}")


if __name__ == "__main__":
    main()