import json
from pathlib import Path

# Path to the JSON dump file
json_dump_file = Path('MORROWIND_GOTY_TR_DUMP/Tamriel_Data_DUMP.json')
output_file = Path('MORROWIND_GOTY_TR_DUMP/Tamriel_Data_DIALOGUE.json')
log_file = Path('processing_log.txt')


# Function to read and parse the JSON dump file
def read_json_objects(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON file: {e}")
            return []


# Function to filter specific types
def filter_dialogues(json_objects, types):
    return [obj for obj in json_objects if obj.get('type') in types]


# Function to log issues
def log_issues(json_objects, log_file, filtered_objects):
    filtered_ids = {obj['id'] for obj in filtered_objects if 'id' in obj}
    with open(log_file, 'w', encoding='utf-8') as log:
        for obj in json_objects:
            if 'type' not in obj or 'id' not in obj or obj['id'] not in filtered_ids:
                log.write(f"Issue with object: {json.dumps(obj)}\n")


# Main function to execute the extraction
def main():
    json_objects = read_json_objects(json_dump_file)
    dialogue_types = {"DialogueInfo", "Dialogue"}
    filtered_dialogues = filter_dialogues(json_objects, dialogue_types)

    # Save filtered dialogues to JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(filtered_dialogues, file, indent=4)

    # Log issues
    log_issues(json_objects, log_file, filtered_dialogues)

    print(f"Filtered dialogues saved to: {output_file}")
    print(f"Log of issues saved to: {log_file}")


if __name__ == "__main__":
    main()
