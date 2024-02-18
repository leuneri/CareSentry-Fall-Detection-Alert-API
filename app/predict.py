import tensorflow
import os
import keras
from keras.models import load_model
import cv2
import numpy as np
# Load the model
model = load_model('model.keras')

def predict(video_path):
    processed_images = []
    
    for img in os.listdir(video_path):
        img = cv2.imread(img)
        if img is not None:
            img = cv2.resize(img, (128, 96))
            img = img / 255
            processed_images.append(img)
    processed_images = np.array(processed_images)  # Convert the list to a numpy array
    predictions = model.predict(processed_images)
    
    # Process predictions to determine if a fall is detected
    threshold = 0.5
    predicted_class = "Fall" if  predictions >= threshold else "No Fall"
    confidence_score = predictions if predicted_class == "Positive" else 1 - predictions
    print(f"Predicted Class: {predicted_class} with confidence {confidence_score[0]:.2f}")
predict("C:/Users/M/OneDrive - softromic/Documents/GitHub/fall_detection/vidframes - 1")
