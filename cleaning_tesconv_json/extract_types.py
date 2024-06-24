import json
from pathlib import Path

# Path to the JSON dump file
json_dump_file = Path('MORROWIND_GOTY_TR_DUMP/TR_Mainland_DUMP.json')
output_file = Path('MORROWIND_GOTY_TR_DUMP/unique_types.json')
log_file = Path('MORROWIND_GOTY_TR_DUMP/processing_log.txt')


# Function to read and parse the JSON dump file
def read_json_objects(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON file: {e}")
            return []


# Function to extract all unique types
def extract_unique_types(json_objects):
    unique_types = set()
    for obj in json_objects:
        if 'type' in obj:
            unique_types.add(obj['type'])
    return list(unique_types)


# Function to log issues
def log_issues(json_objects, log_file):
    with open(log_file, 'w', encoding='utf-8') as log:
        for obj in json_objects:
            if 'type' not in obj:
                log.write(f"Issue with object: {json.dumps(obj)}\n")


# Main function to execute the extraction
def main():
    json_objects = read_json_objects(json_dump_file)
    unique_types_list = extract_unique_types(json_objects)

    # Save unique types to JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(unique_types_list, file, indent=4)

    # Log issues
    log_issues(json_objects, log_file)

    print(f"Unique types saved to: {output_file}")
    print(f"Log of issues saved to: {log_file}")


if __name__ == "__main__":
    main()