import cv2
import requests
import numpy as np

def send_frame_to_api(frame):
    """
    Send a frame to an external API for processing.
    The frame is encoded as a JPEG before being sent.
    """
    # Encode frame as JPEG
    _, encoded_image = cv2.imencode('.jpg', frame)
    image_bytes = encoded_image.tobytes()

    # Specify your API endpoint
    api_endpoint = "http://your-api-endpoint.com/api"

    # Prepare headers for the HTTP request
    headers = {'Content-Type': 'image/jpeg'}

    # Send the frame to the API using a POST request
    response = requests.post(api_endpoint, data=image_bytes, headers=headers)

    ###TODO: consider how to send result
    if response:
        return True
        # Add true response here for how to handle
    # offer a response with location included (hard-coded for now)

# Initialize the camera
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

frame_count = 0
send_every_n_frames = 30  # Adjust based on your needs

try:
    while True:
        ret, frame = cap.read()

        # Check if frame is captured
        if not ret:
            break

        # Display the captured frame
        cv2.imshow('Camera Output', frame)

        # Increment the frame count
        frame_count += 1

        # Send every Nth frame to the API
        if frame_count % send_every_n_frames == 0:
            send_frame_to_api(frame)

        # Break the loop with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()
