import json
from pathlib import Path

# Path to the input JSON file
input_file = Path('MORROWIND_GOTY_TR_DUMP\Morrowind_DIALOGUE_TOPICS.json')
output_file = Path('MORROWIND_GOTY_TR_CLEANED\Morrowind_DIALOGUE.jsonl')


# Read and parse the JSON file
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# Process the data to keep only unique text fields
def process_data(json_objects):
    unique_texts = set()
    processed_data = []

    for obj in json_objects:
        text = obj.get('text')
        if text and text not in unique_texts:
            unique_texts.add(text)
            processed_data.append({"text": text})

    return processed_data


# Write the processed data to a JSONL file
def write_jsonl(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for entry in data:
            file.write(json.dumps(entry) + '\n')


# Main function to execute the processing
def main():
    json_objects = read_json(input_file)
    processed_data = process_data(json_objects)
    write_jsonl(processed_data, output_file)

    print(f"Processed data saved to: {output_file}")


if __name__ == "__main__":
    main()
