import json
from pathlib import Path
import re

from chat_bot_resources.config import DATA_DIRECTORY


def clean_references(references):
    cleaned_references = []
    for reference in references:
        cleaned_reference = reference.replace('\u2014', '—').replace('^', '').strip()
        cleaned_reference = re.sub(r'^[a-z](?: [a-z])*\s', '', cleaned_reference)

        cleaned_references.append(cleaned_reference)
    return cleaned_references


def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if "References" in data:
        data["References"] = clean_references(data["References"])

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def process_directory(directory_path):
    for path in Path(directory_path).rglob('*.json'):
        process_json_file(path)


# Replace 'your_directory_path' with the path to your nested directory structure
your_directory_path = DATA_DIRECTORY
process_directory(your_directory_path)

print("Completed cleaning references in JSON files.")
