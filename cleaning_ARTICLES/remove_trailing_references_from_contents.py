import json
import re
from pathlib import Path

from chat_bot_resources.config import DATA_DIRECTORY


def clean_references_from_contents(contents):
    if isinstance(contents, str):
        return re.sub(r'references\s*', '', contents, flags=re.IGNORECASE).strip()
    elif isinstance(contents, list):
        return [clean_references_from_contents(item) for item in contents]
    elif isinstance(contents, dict):
        return {k: clean_references_from_contents(v) for k, v in contents.items()}
    return contents


def process_json_file(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if 'Contents' in data:
        data['Contents'] = clean_references_from_contents(data['Contents'])

    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def traverse_and_process(directory):
    path = Path(directory)
    for json_file in path.rglob('*.json'):
        process_json_file(json_file)


if __name__ == "__main__":
    # Replace 'your_directory_path' with the path to your directory
    your_directory_path = DATA_DIRECTORY
    traverse_and_process(your_directory_path)
