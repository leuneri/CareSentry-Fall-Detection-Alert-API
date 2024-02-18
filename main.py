from fastapi import FastAPI, File, UploadFile, HTTPException
from keras.models import load_model
from fastapi.responses import JSONResponse
from typing import List
import numpy as np
import cv2
import logging
import tempfile
import shutil
import os

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Load your model as before
model = load_model("model.keras")

def load_and_preprocess_images_from_files(files: List[UploadFile]):
    with tempfile.TemporaryDirectory() as temp_dir:
        images = []
        for file in files:
            # Save temporary file
            temp_file = os.path.join(temp_dir, file.filename)
            with open(temp_file, 'wb') as f:
                shutil.copyfileobj(file.file, f)
            
            # Process the image
            image = cv2.imread(temp_file)
            if image is None:
                logging.warning(f"Failed to load image: {temp_file}")
                continue
            image = cv2.resize(image, (128, 96))
            image = image / 255.0
            images.append(image)
        
        if len(images) != 60:
            raise ValueError("Expected 60 images, found {}".format(len(images)))
        images_array = np.array(images)
        images_array = np.expand_dims(images_array, axis=0)
        return images_array

@app.post("/predict/")
async def predict_from_folder(files: List[UploadFile] = File(...)):
    try:
        # Preprocess and load images
        images_array = await load_and_preprocess_images_from_files(files)
        
        # Ensure the input shape is correct
        if images_array.ndim == 3:
            images_array = np.expand_dims(images_array, axis=0)
        
        # Predict
        prediction = model.predict(images_array)
        
        # Process prediction
        result = (prediction > 0.5).astype('int').tolist()
        return JSONResponse(content={"result": result})
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return HTTPException(status_code=500, detail=f"Prediction error: {e}")
