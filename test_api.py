import requests

# The URL of the API endpoint
url = 'http://127.0.0.1:8000/predict/'

# Send a POST request to the API endpoint
response = requests.post(url)

# Check if the request was successful
if response.status_code == 200:
    # Get the prediction result from the response
    result = response.json()['result']
    print(f"The prediction result is: {result}")
else:
    print("Failed to get a response from the API. Status code:", response.status_code)