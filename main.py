from fastapi import FastAPI, HTTPException
from keras.models import load_model
import numpy as np
import cv2
import os
from typing import List
import logging
from pathlib import Path

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Load your pre-trained model (adjust the path to your saved model correctly)
current_directory = Path.cwd()
model_path = current_directory / "model.keras"  # Use pathlib for OS-agnostic path handling
try:
    model = load_model(model_path)
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    # Consider adding error handling to stop the app if critical
    # raise RuntimeError(f"Failed to load model: {e}")

# Function to load and preprocess images from a folder
def load_and_preprocess_images(folder_path: str):
    images = []
    for filename in sorted(os.listdir(folder_path)):
        # Ensure the file is an image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Read the image using OpenCV
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)
            if image is None:
                logging.warning(f"Failed to load image: {image_path}")
                continue
            # Resize and normalize the image
            image = cv2.resize(image, (128, 96))
            image = image / 255.0
            images.append(image)
    if len(images) != 60:
        raise ValueError("Expected 60 images, found {}".format(len(images)))
    images_array = np.array(images)
    # Add an extra dimension to indicate batch size, which is 1 in this case
    images_array = np.expand_dims(images_array, axis=0)
    return images_array

@app.get("/predict/")
async def predict_from_folder():
    folder_path = "C:/Users/ericl/git/fall_detection/vidframes1"

    try:
        # Load and preprocess images
        images_array = load_and_preprocess_images(folder_path)
        if images_array.ndim == 3:  # Ensure the input shape is correct
            images_array = np.expand_dims(images_array, axis=0)
        # Predict
        prediction = model.predict(images_array)
        # Assume the model outputs a sigmoid activation and use 0.5 as the threshold for binary classification
        result = (prediction > 0.5).astype('int').tolist()
        return {"result": result}
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

# Run the API with uvicorn
# Command to run: uvicorn your_script_name:app --reload
