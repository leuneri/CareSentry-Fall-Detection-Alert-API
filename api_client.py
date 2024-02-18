import numpy as np
from fastapi import FastAPI, HTTPException
from keras.models import load_model
import cv2
import os
import logging
from pathlib import Path
from typing import List
# import shutil
send_every_n_frames = 60  # Adjust based on your needs
# Load your pre-trained model (adjust the path to your saved model correctly)
current_directory = Path.cwd()
model_path = current_directory / "model.keras"  # Use pathlib for OS-agnostic path handling
try:
    model = load_model(model_path)
except Exception as e:
    logging.error(f"Failed to load model: {e}")

folder_path = current_directory / "vidframes1" 


def clear_folder():
    # Loop through all items in the folder
    for item_name in os.listdir(folder_path):
        # Create the full path to the item
        item_path = os.path.join(folder_path, item_name)
        # Deletes item in path
        if os.path.isfile(item_path):
            os.remove(item_path)

def send_frame_to_folder(frames):
    frame_number = 10
    # Encode frame as JPEG
    for frame in frames:
        _, encoded_image = cv2.imencode('.jpg', frame)
    # image_bytes = encoded_image.tobytes()
        filename = f"frame_{frame_number}.jpg"
        image_path = os.path.join(folder_path, filename)
        frame_number += 1

        # Write the encoded image to a file
        with open(image_path, 'wb') as file:
            file.write(encoded_image)


def load_and_preprocess_images(folder_path):
    images = []
    # Use .iterdir() to iterate over the contents of the folder
    for path in folder_path.iterdir():
        if path.is_file():  # Ensure it's a file
            image_path = str(path)  # Convert Path object to string
            image = cv2.imread(image_path)
            if image is None:
                logging.warning(f"Failed to load image: {image_path}")
                continue
            image = cv2.resize(image, (128, 96))
            image = image / 255.0  # Normalize pixel values
            images.append(image)
    if len(images) != send_every_n_frames:
        raise ValueError("Expected 60 images, found {}".format(len(images)))
    images_array = np.array(images)
    images_array = np.expand_dims(images_array, axis=0)  # Add batch dimension
    return images_array

    
def predict_from_folder():   
    try:
        # Load and preprocess images
        images_array = load_and_preprocess_images(folder_path)
        # if images_array.ndim == 5:  # Ensure the input shape is correct
        #     images_array = np.expand_dims(images_array, axis=0)
        # Predict
        prediction = model.predict(images_array)
        # Assume the model outputs a sigmoid activation and use 0.5 as the threshold for binary classification
        result = (prediction > 0.5).astype('int').tolist()
        return {"result": result}
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")


    

# Initialize the camera
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

frame_count = 0

frames = []

try:
    while True:
        ret, frame = cap.read()

        # # Check if frame is captured
        # if not ret:
        #     break

        # Display the captured frame
        cv2.imshow('Camera Output', frame)

        frames.append(frame)

        # Increment the frame count
        frame_count += 1

        # Send every Nth frame to the API
        if frame_count % send_every_n_frames == 0:
            clear_folder()
            send_frame_to_folder(frames)
            load_and_preprocess_images(folder_path)
            result = predict_from_folder()
            frame_count = 0
            if result["result"][0][0] == 1:
                print("this actually worked")
                break
                # continue
                #TODO: add logic here to imform nurse

        # Break the loop with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()
