import requests
import os
import json

# Load JSON data from file
json_file_path = 'data/data.json'
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Ensure the data/ folder exists
os.makedirs('data', exist_ok=True)

# Function to download and save an image
def download_image(url, path):
    # Check if the file already exists
    if not os.path.exists(path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                f.write(response.content)
        print(f"Downloaded {os.path.basename(path)}")
    else:
        print(f"File {os.path.basename(path)} already exists. Skipping download.")

# Iterate through each item in the JSON list
for item in json_data:
    image_url = item.get('imageURL')
    if image_url:  # Check if the imageURL is not null
        file_name = os.path.basename(image_url)
        save_path = os.path.join('data', file_name)
        download_image(image_url, save_path)
