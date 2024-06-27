import json
from pathlib import Path
import json5
from data_directory_set.config import DATA_DIRECTORY

def clean_and_save_json(input_file, output_file):
    try:
        # Read the non-conforming JSON file
        with open(input_file, 'r', encoding='utf-8') as file:
            non_conforming_json = file.read()

        # Parse the non-conforming JSON using JSON5
        data = json5.loads(non_conforming_json)

        # Convert the parsed JSON5 data to standard JSON
        conforming_json = json.dumps(data, indent=2, ensure_ascii=False)

        # Save the cleaned JSON to a new file with UTF-8 encoding
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(conforming_json)

        # print(f"Successfully cleaned and saved JSON to {output_file}")

    except json5.JSONDecodeError as e:
        print(f"Error parsing JSON5: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def process_directory(directory):
    path = Path(directory)
    for file_path in path.rglob('*.json'):
        clean_and_save_json(file_path, file_path)
        # print(f"Processed file: {file_path}")


# Specify the directory containing the JSON files
directory = DATA_DIRECTORY
process_directory(directory)
