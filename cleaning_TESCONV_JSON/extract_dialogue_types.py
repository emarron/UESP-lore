import json
from pathlib import Path

# Path to the JSON dump file
json_dump_file = Path('MORROWIND_GOTY_TR_DUMP/TR_MAINLAND_DIALOGUE.json')
output_file = Path('MORROWIND_GOTY_TR_DUMP/dialogue_types.json')
log_file = Path('dialogue_types_log.txt')


# Function to read and parse the JSON dump file
def read_json_objects(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON file: {e}")
            return []


# Function to extract dialogue types from DialogueInfo objects
def extract_dialogue_types(json_objects):
    dialogue_types = set()
    for obj in json_objects:
        if obj.get('type') == 'DialogueInfo' and 'data' in obj:
            dialogue_type = obj['data'].get('dialogue_type')
            if dialogue_type:
                dialogue_types.add(dialogue_type)
    return list(dialogue_types)


# Function to log issues
def log_issues(json_objects, log_file):
    with open(log_file, 'w', encoding='utf-8') as log:
        for obj in json_objects:
            if obj.get('type') == 'DialogueInfo' and 'data' not in obj:
                log.write(f"Issue with object: {json.dumps(obj)}\n")


# Main function to execute the extraction
def main():
    json_objects = read_json_objects(json_dump_file)
    dialogue_types_list = extract_dialogue_types(json_objects)

    # Save dialogue types to JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(dialogue_types_list, file, indent=4)

    # Log issues
    log_issues(json_objects, log_file)

    print(f"Dialogue types saved to: {output_file}")
    print(f"Log of issues saved to: {log_file}")


if __name__ == "__main__":
    main()
