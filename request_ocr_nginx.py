import requests

url = "http://localhost:80/ocr"

# Replace this with the path to the image file you want to send
file_path = "sample.png"

with open(file_path, "rb") as file:
    files = {'imagefile': ('sample.png', file, 'image/png')}
    response = requests.post(url, files=files)

print(response.json())
