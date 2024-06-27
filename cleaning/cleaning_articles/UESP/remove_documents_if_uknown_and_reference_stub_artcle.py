import json
from pathlib import Path
import re


def should_delete_file(json_data):
    contents = json_data.get("Contents", "")
    print(f"Checking contents: {contents}")  # Debugging line
    return bool(re.search(r"\bmay refer to\b", contents))


# Define the directory path containing the JSON files
directory_path = Path("CLEANED_OUTPUT/UNCLASSIFIED")

# Iterate through all JSON files in the directory
for json_file in directory_path.glob('*.json'):
    print(f"Processing file: {json_file}")  # Debugging line
    with json_file.open('r', encoding='utf-8') as file:
        try:
            json_data = json.load(file)
            print(f"Loaded JSON: {json_data}")  # Debugging line
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {json_file}")
            continue

    # Ensure the file is closed before attempting to delete it
    if should_delete_file(json_data):
        print(f"Deleting file: {json_file}")
        json_file.unlink()  # This will delete the file
    else:
        print(f"File does not meet delete criteria: {json_file}")  # Debugging line

print("Script completed.")
