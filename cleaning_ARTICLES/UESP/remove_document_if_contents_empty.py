import os
import json

from chat_bot_resources.config import DATA_DIRECTORY

# Define the root directory containing the JSON files
root_dir = DATA_DIRECTORY


def is_content_empty(content):
    return not content.strip()


def process_json_files(root_dir):
    deleted_files = []

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                filepath = os.path.join(subdir, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Check if 'Contents' field is empty
                    if 'Contents' in data and is_content_empty(data['Contents']):
                        os.remove(filepath)
                        deleted_files.append(filepath)

                except (json.JSONDecodeError, OSError) as e:
                    print(f"Error processing file {filepath}: {e}")

    return deleted_files


if __name__ == "__main__":
    deleted_files = process_json_files(root_dir)
    print("Deleted files:")
    for file in deleted_files:
        print(file)
