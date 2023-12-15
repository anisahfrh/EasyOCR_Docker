import requests

# Replace the URL with the actual URL of your FastAPI server
url = "http://172.17.0.2:8000/ocr"

# Replace this with the path to the image file you want to send
file_path = "sample.png"

# Open the file and send it as a POST request
with open(file_path, "rb") as file:
    files = {'imagefile': ('sample.png', file, 'image/png')}
    response = requests.post(url, files=files)

# Print the response from the server
print(response.json())
