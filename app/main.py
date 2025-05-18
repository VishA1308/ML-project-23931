import json
from typing import Annotated
from tesseract_test import get_text
from ustranenie_in_text import filter_text
from extraction import nlp_extraction
from fastapi import FastAPI, HTTPException, File, UploadFile
import tempfile
import os

app = FastAPI()

@app.post("/process/")
async def process(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        try:
            
            contents = await file.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name
            
            
            rec_text = get_text(temp_file_path)
            filt_text = filter_text(rec_text)

            response_dict = {"rec_text": rec_text, "text": filt_text}

            res = nlp_extraction(filt_text)

            
            return response_dict
        finally:
            temp_file.close()
            os.unlink(temp_file_path)
