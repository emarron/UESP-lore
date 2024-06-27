import json
from pathlib import Path

# Define the source and destination directories
source_directory = Path('imperial_library_sorted')
destination_directory = Path('new_json_directory')

# Ensure the destination directory exists
destination_directory.mkdir(parents=True, exist_ok=True)


# Function to sanitize titles for filenames
def sanitize_title(title):
    return title.replace(' ', '_').replace(',', '').replace(':', '').replace('\'', '').replace('"', '')


# Function to reformat a single JSON file
def reformat_json(source_path, destination_path_base):
    with open(source_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Split the "Released in" field into a list
    released_in_list = [item.strip() for item in data.get('Released in', '').split(',')]

    # Check if Formatted_Books is present
    if 'Formatted_Books' in data:
        formatted_books = data['Formatted_Books']
        # Handle the case where Formatted_Books is a dictionary
        if isinstance(formatted_books, dict):
            formatted_books = [formatted_books]
        for index, book in enumerate(formatted_books, start=1):
            new_data = {
                'Title': book.get('Title', ''),
                'Tags': data.get('Tags', []),
                'Released In': released_in_list,
                'Category': data.get('Category', ''),
                'Author': data.get('Author', ''),
                'Series': data.get('True_Title', ''),
                'Synopsis': data.get('Synopsis', ''),
                'Contents': book.get('Contents', '')
            }
            # Create the destination path for each formatted book
            base_title = sanitize_title(data.get('Title', 'Untitled'))
            destination_path = destination_path_base.parent / f"{base_title}_{index}.json"

            # Ensure the destination subdirectory exists
            destination_path.parent.mkdir(parents=True, exist_ok=True)

            with open(destination_path, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, indent=4, ensure_ascii=False)
    else:
        new_data = {
            'Title': data.get('True_Title', ''),
            'Tags': data.get('Tags', []),
            'Released In': released_in_list,
            'Category': data.get('Category', ''),
            'Author': data.get('Author', ''),
            'Synopsis': data.get('Synopsis', ''),
            'Contents': data.get('Formatted_Content', ''),
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
