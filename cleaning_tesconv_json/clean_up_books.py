import json
from pathlib import Path

# Path to the input JSON file
input_file = Path('MORROWIND_GOTY_TR_DUMP/Morrowind_BOOKS.jsonl')
output_file = Path('MORROWIND_GOTY_TR_DUMP/Morrowind_BOOKS.jsonl')


# Read and parse the JSON file
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# Clean the text by removing all newline characters
def clean_text(text):
    return text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()


# Process the data to clean the text fields and remove duplicates
def process_data(json_objects):
    unique_texts = set()
    cleaned_data = []

    for obj in json_objects:
        if 'text' in obj:
            cleaned_text = clean_text(obj['text'])
            if cleaned_text not in unique_texts:
                unique_texts.add(cleaned_text)
                obj['text'] = cleaned_text
                cleaned_data.append(obj)

    return cleaned_data


# Write the cleaned data to a JSONL file
def write_jsonl(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for entry in data:
            file.write(json.dumps(entry) + '\n')


# Main function to execute the processing
def main():
    json_objects = read_json(input_file)
    cleaned_data = process_data(json_objects)
    write_jsonl(cleaned_data, output_file)

    print(f"Cleaned data saved to: {output_file}")


if __name__ == "__main__":
    main()
