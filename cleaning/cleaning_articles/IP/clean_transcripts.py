import json
from pathlib import Path

# Define the source and destination directories
source_directory = Path('data/imperial_library_sorted/transcript')
destination_directory = Path('data/final/')

unformatted_directory = Path('data/final/unformatted/')
failures_log = Path('data/final/failures.txt')

# Ensure the destination directories exist
destination_directory.mkdir(parents=True, exist_ok=True)
unformatted_directory.mkdir(parents=True, exist_ok=True)


# Function to sanitize titles for filenames
def sanitize_title(title):
    return title.replace(' ', '_').replace(',', '').replace(':', '').replace('\'', '').replace('"', '')


# Function to reformat a single JSON file
def reformat_json(source_path, destination_path_base):
    with open(source_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if 'Dialogue' is empty
    if not data.get('Dialogue'):
        # Check if 'Formatted_Contents' exists
        if 'Formatted_Contents' in data:
            new_data = {
                'Title': data.get('True_Title', ''),
                'Tags': data.get('Tags', []),
                'Quest Line': data.get('Quest Line', ''),
                'Synopsis': data.get('Synopsis', ''),
                'Contents': data.get('Formatted_Contents', ''),
            }

            # Ensure the unformatted destination subdirectory exists
            destination_unformatted_path_base = unformatted_directory / destination_path_base
            destination_unformatted_path_base.parent.mkdir(parents=True, exist_ok=True)

            with open(destination_unformatted_path_base, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, indent=4, ensure_ascii=False)
        else:
            # Log the failure and return
            with open(failures_log, 'a', encoding='utf-8') as log:
                log.write(f"Skipped file due to empty Dialogue and missing Formatted_Contents: {source_path}\n")
        return

    new_data = {
        'Title': data.get('True_Title', ''),
        'Tags': data.get('Tags', []),
        'Quest Line': data.get('Quest Line', ''),
        'Synopsis': data.get('Synopsis', ''),
        'Dialogue': data.get('Dialogue', ''),
    }

    # Ensure the destination subdirectory exists
    destination_path_base.parent.mkdir(parents=True, exist_ok=True)

    with open(destination_path_base, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)


# Iterate over all JSON files in the source directory
for source_path in source_directory.glob('**/*.json'):
    # Construct the destination path
    relative_path = source_path.relative_to(source_directory)
    destination_path_base = destination_directory / relative_path

    # Reformat and save the JSON file
    reformat_json(source_path, destination_path_base)

print("Reformatting complete.")
