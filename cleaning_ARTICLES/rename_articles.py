import json
from pathlib import Path


def process_json_files(directory):
    directory = Path(directory)

    for json_file in directory.rglob('*.json'):
        # Remove 'Lore_' from the beginning of the filename
        new_filename = json_file.name[5:] if json_file.name.startswith('Lore_') else json_file.name
        new_file_path = json_file.with_name(new_filename)

        with json_file.open('r', encoding='utf-8') as file:
            data = json.load(file)

        # Process the JSON content
        def remove_lore_prefix(item):
            if isinstance(item, str):
                return item[5:] if item.startswith('Lore:') else item
            elif isinstance(item, dict):
                return {k: remove_lore_prefix(v) for k, v in item.items()}
            elif isinstance(item, list):
                return [remove_lore_prefix(v) for v in item]
            else:
                return item

        processed_data = remove_lore_prefix(data)

        # Write the processed data back to a new file
        with new_file_path.open('w', encoding='utf-8') as file:
            json.dump(processed_data, file, indent=4, ensure_ascii=False)

        # If the filename was changed, remove the old file
        if new_file_path != json_file:
            json_file.unlink()

    print("Processing complete.")


# Usage
directory = Path('CLEANED_OUTPUT')
process_json_files(directory)