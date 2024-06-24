import json
from pathlib import Path


def extract_info_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Convert all keys to lowercase for case insensitivity
    data = {k.lower(): v for k, v in data.items()}

    # Extract common parts
    title = data.get('title', '').replace("Lore:", "")
    contents = data.get('contents', '')

    # Extract additional parts if available
    provenance = data.get('provenance', {})
    provenance = {k.lower(): v for k, v in provenance.items()}

    basic_info = data.get('basic_info', {})
    basic_info = {k.lower(): v for k, v in basic_info.items()}

    return title, contents, provenance, basic_info


def create_prompt_response(folder, title, contents, provenance, basic_info):
    # Create prompt based on folder and title
    prompt = f"tell me about the {folder.upper()}: {title}."

    # Create response with all available information
    response_parts = []

    if provenance:
        provenance_info = ', '.join([f"{key}: {value}" for key, value in provenance.items() if value])
        response_parts.append(f"provenance: {provenance_info}")

    if basic_info:
        basic_info_data = ', '.join([f"{key}: {value}" for key, value in basic_info.items() if value])
        response_parts.append(f"basic info: {basic_info_data}")

    if contents:
        response_parts.append(f"contents: {contents}")

    response = f"{title} is a {folder.lower()} with " + '. '.join(response_parts) + '.'

    return {"prompt": prompt, "response": response}


def process_folder(folder):
    data = []
    folder_path = Path(folder)

    for file_path in folder_path.glob('*.json'):
        title, contents, provenance, basic_info = extract_info_from_json(file_path)
        prompt_response_pair = create_prompt_response(folder_path.stem, title, contents, provenance, basic_info)
        data.append(prompt_response_pair)

    return data


def main(directory):
    all_data = []
    directory_path = Path(directory)

    # Search for all folders in the given directory
    for folder in directory_path.iterdir():
        if folder.is_dir():
            folder_data = process_folder(folder)
            all_data.extend(folder_data)

    # Save dataset to JSONL file
    dataset_path = Path('dataset.jsonl')
    with dataset_path.open('w', encoding='utf-8') as f:
        for entry in all_data:
            f.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    # Provide the directory containing the folders as an argument
    directory = 'CLEANED_OUTPUT'
    main(directory)
