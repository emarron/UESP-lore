import json
from pathlib import Path

# Path to the extracted dialogue JSON file
dialogue_json_file = Path('MORROWIND_GOTY_TR_DUMP/Tamriel_Data_DIALOGUE.json')
output_file = Path('MORROWIND_GOTY_TR_DUMP/Tamriel_Data_DIALOGUE_TOPICS.json')
log_file = Path('topics_log.txt')


# Function to read and parse the JSON file
def read_json_objects(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON file: {e}")
            return []


# Function to filter DialogueInfo objects with dialogue_type as "Topic"
def filter_topics(json_objects):
    topics = []
    for obj in json_objects:
        if obj.get('type') == 'DialogueInfo' and obj.get('data', {}).get('dialogue_type') == 'Topic':
            topic_info = {
                'id': obj.get('id', ''),
                'dialogue_type': obj['data'].get('dialogue_type', ''),
                'speaker_id': obj.get('speaker_id', ''),
                'speaker_race': obj.get('speaker_race', ''),
                'speaker_class': obj.get('speaker_class', ''),
                'speaker_faction': obj.get('speaker_faction', ''),
                'player_faction': obj.get('player_faction', ''),
                'text': obj.get('text', '')
            }
            topics.append(topic_info)
    return topics


# Function to log issues
def log_issues(json_objects, log_file):
    with open(log_file, 'w', encoding='utf-8') as log:
        for obj in json_objects:
            if obj.get('type') == 'DialogueInfo' and 'data' not in obj:
                log.write(f"Issue with object: {json.dumps(obj)}\n")


# Main function to execute the extraction
def main():
    json_objects = read_json_objects(dialogue_json_file)
    topics_list = filter_topics(json_objects)

    # Save filtered topics to JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(topics_list, file, indent=4)

    # Log issues
    log_issues(json_objects, log_file)

    print(f"Filtered topics saved to: {output_file}")
    print(f"Log of issues saved to: {log_file}")


if __name__ == "__main__":
    main()
