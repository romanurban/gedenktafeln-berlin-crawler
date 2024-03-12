import json
import os

# Load the JSON data from the original data.json file
with open('data/data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# This list will store the entries for which the image file exists or imageURL is not None
filtered_data = []

for i, entry in enumerate(data):
    # Check if 'imageURL' exists and is not None
    if entry.get('imageURL'):
        # Extract the file name from the imageURL
        image_url = entry['imageURL']
        file_name = image_url.split('/')[-1]  # Adjust this line if needed

        # Construct the file path assuming the images are stored in the data/ directory
        file_path = os.path.join('data', file_name)

        # Check if the file exists on the disk
        if os.path.exists(file_path):
            # If the file exists, add the entry to the filtered_data list
            filtered_data.append(entry)
            print(f"File exists and retained for entry {i+1}: {file_name}")
        else:
            print(f"File does NOT exist for entry {i+1}: {file_name}, entry will be removed.")
    else:
        print(f"No valid imageURL for entry {i+1}, entry will be removed.")

# Write the filtered data back to a new JSON file
with open('data/data_clean.json', 'w', encoding='utf-8') as file:
    json.dump(filtered_data, file, indent=4, ensure_ascii=False)

print("Finished processing. New data.json has been saved.")
