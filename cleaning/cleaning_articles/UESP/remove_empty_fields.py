import json
import pathlib

from data_directory_set.config import DATA_DIRECTORY


def remove_empty_specific_fields(data, title):
    fields_to_check = ['Synopsis', 'Provenance', 'References', 'Person_Info', 'Place_Info']

    for field in fields_to_check:
        if field in data:
            if isinstance(data[field], dict) and not any(data[field].values()):
                print(f"Removing empty field '{field}' from article '{title}'")
                del data[field]
            elif isinstance(data[field], list) and not data[field]:
                print(f"Removing empty field '{field}' from article '{title}'")
                del data[field]
            elif isinstance(data[field], str) and not data[field].strip():
                print(f"Removing empty field '{field}' from article '{title}'")
                del data[field]


def process_json_files(directory_path):
    directory_path = pathlib.Path(directory_path)

    for json_file in directory_path.rglob('*.json'):
        with json_file.open('r', encoding='utf-8') as file:
            data = json.load(file)

        title = data.get('Title', 'Unknown')
        print(f"\nProcessing article '{title}'")
        remove_empty_specific_fields(data, title)

        with json_file.open('w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

# Example usage
directory_path = DATA_DIRECTORY
process_json_files(directory_path)
