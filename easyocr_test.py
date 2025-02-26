import easyocr

# Create an OCR reader object
reader = easyocr.Reader(['ru'])

# Read text from an image
result = reader.readtext('vitD.png')

# Print the extracted text
for detection in result:
    print(detection[1])