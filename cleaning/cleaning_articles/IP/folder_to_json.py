import os
import json

# Define the directories and the target directory
root_directory = "new_json_directory/books"
directories = [
    'advertisements', 'lists & records', 'announcements & warnings',
    'manuals & instructions', 'fiction & narrative', 'other', 'guilds & societies',
    'places & people', 'histories & biographies', 'plays', 'inscriptions & epitaphs',
    'politics & propaganda', 'jokes & riddles', 'religion & legends', 'journals',
    'research', 'letters & notes', 'songs & poems'
]


# Function to process each file
def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Remove the "Tags" field
    if "Tags" in data:
        del data["Tags"]

    return data


# Function to process each directory
def process_directory(directory):
    combined_data = []
    directory_path = os.path.join(root_directory, directory)

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            processed_data = process_json_file(file_path)
            combined_data.append(processed_data)

    return combined_data


# Create a master JSON file for each directory
for directory in directories:
    combined_data = process_directory(directory)
    output_file_path = os.path.join(root_directory, f"{directory}.json")

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(combined_data, output_file, ensure_ascii=False, indent=4)

print("Processing completed.")
