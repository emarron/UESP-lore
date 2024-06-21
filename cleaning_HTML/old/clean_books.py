# cleaner.py
# you can tell this is the first one made. but it works so whatever.


from bs4 import BeautifulSoup
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import re
import json

# Define the directory where the HTML files are saved
lore_dump_dir = Path('LORE_DUMP')
output_dir = Path('BOOKS_CLEANED')
log_file = output_dir / 'processing_log.txt'

# Create the LORE_JSON directory if it doesn't exist
output_dir.mkdir(exist_ok=True)


# Function to sanitize filenames by removing invalid characters
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


# Function to remove references like [1], [2], etc.
def remove_references(text):
    return re.sub(r'\[\d+\]', '', text)


# Function to extract book content and save as JSON
def extract_and_save_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract title
    title = soup.find('title').text.replace(' - The Unofficial Elder Scrolls Pages (UESP)', '')

    # Check if the content division is a book
    content_div = soup.find('div', class_='book')
    if not content_div:
        print(f"Skipping non-book file: {filepath.name}")
        return

    # Extract provenance information
    info_box = soup.find('table', class_='infobox')

    if info_box:
        writer = ''
        seen_in = []

        # Find the writer
        writer_row = info_box.find('th', text='Writer')
        if writer_row:
            writer = writer_row.find_next_sibling('td').get_text(strip=True)

        # Find the seen_in
        seen_in_row = info_box.find('th', text='Seen In:')
        if seen_in_row:
            seen_in_links = seen_in_row.find_next_sibling('td').find_all('a')
            seen_in = [link.get_text(strip=True) for link in seen_in_links]

        provenance = {
            'Article': title,
            'Writer': writer,
            'Seen In': ', '.join(seen_in)
        }

        # Extract book information
        book_info = soup.find('div', style='text-align:center; margin:0 auto; display:table;')
        synopsis = book_info.get_text(separator='\n', strip=True) if book_info else "Synopsis not found"
        synopsis = remove_references(synopsis)

        # Extract contents
        article_text = content_div.get_text(separator='\n', strip=True)
        article_text = remove_references(article_text)
    else:
        provenance = {
            'Article': title,
            'Writer': '',
            'Seen In': ''
        }
        synopsis = "Book information not found."
        article_text = "Main article content not found."

        # Log the issue
        with open(log_file, 'a', encoding='utf-8') as log:
            log.write(f"Issue with file: {filepath.name}\n")

        return

    book_data = {
        'title': title,
        'provenance': provenance,
        'synopsis': synopsis,
        'contents': article_text
    }

    json_filename = sanitize_filename(filepath.stem + '.json')
    json_filepath = output_dir / json_filename

    with open(json_filepath, 'w', encoding='utf-8') as json_file:
        json.dump(book_data, json_file, indent=4)

    print(f"Extracted JSON saved to: {json_filepath}")


# Main function to execute the extraction in multithreaded mode
def main():
    html_files = list(lore_dump_dir.glob('*.html'))

    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(extract_and_save_json, html_files)


if __name__ == "__main__":
    main()
