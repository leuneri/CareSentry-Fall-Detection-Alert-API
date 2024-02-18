import requests
import os

# The URL of the API endpoint
url = 'http://127.0.0.1:8000/predict/'

# Path to the folder containing your images
folder_path = 'vidframes1'

# Collecting files to send
files = [('files', (filename, open(os.path.join(folder_path, filename), 'rb'), 'image/jpeg'))
         for filename in os.listdir(folder_path) if filename.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Making the request
response = requests.post(url, files=files)

# Assuming your endpoint returns JSON with a 'result' key
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)
