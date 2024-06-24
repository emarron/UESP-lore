import json
from pathlib import Path
from bs4 import BeautifulSoup

# Path to the JSON dump file
json_dump_file = Path('MORROWIND_GOTY_TR_DUMP/Morrowind_DUMP.json')
output_file = Path('MORROWIND_GOTY_TR_DUMP/Morrowind_BOOKS.json')
log_file = Path('book_extraction_log.txt')


# Function to read and parse the JSON dump file
def read_json_objects(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON file: {e}")
            return []


# Function to clean the book text
def clean_text(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text(separator="\n").strip()


# Function to extract Book type objects
def extract_books(json_objects):
    books = []
    for obj in json_objects:
        if obj.get('type') == 'Book':
            book_info = {
                'name': obj.get('name', ''),
                'text': clean_text(obj.get('text', ''))
            }
            books.append(book_info)
    return books


# Function to log issues
def log_issues(json_objects, log_file):
    with open(log_file, 'w', encoding='utf-8') as log:
        for obj in json_objects:
            if obj.get('type') == 'Book' and ('name' not in obj or 'text' not in obj):
                log.write(f"Issue with object: {json.dumps(obj)}\n")


# Main function to execute the extraction
def main():
    json_objects = read_json_objects(json_dump_file)
    books_list = extract_books(json_objects)

    # Save extracted books to JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(books_list, file, indent=4)

    # Log issues
    log_issues(json_objects, log_file)

    print(f"Extracted books saved to: {output_file}")
    print(f"Log of issues saved to: {log_file}")


if __name__ == "__main__":
    main()
