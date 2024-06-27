import os
import json
from bs4 import BeautifulSoup

# Directory containing your JSON files
json_directory = "imperial_library_cleaned/content/"
books_directory = "books"

def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def extract_links_and_context(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    for item in soup.find_all('div', class_='listing-item'):
        a_tag = item.find('a', href=True)
        if a_tag:
            link = a_tag['href'].split('/')[-1].replace('.html', '.json')
            excerpt_tag = item.find('span', class_='excerpt')
            context = excerpt_tag.get_text().strip() if excerpt_tag else ""
            links.append((link, context))
    return links

def update_json_with_tags_and_synopsis(filepath, reference_title, context):
    json_content = load_json_file(filepath)
    if 'Tags' not in json_content:
        json_content['Tags'] = []
    # if reference_title not in json_content['Tags']:
    #     json_content['Tags'].append(reference_title)
    if 'Book' not in json_content['Tags']:
        json_content['Tags'].append("Book")
    json_content['Synopsis'] = context
    return json_content

def save_json_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=4)

# Load the reference JSON file
reference_file = "imperial_library_cleaned/game-books/all-elder-scrolls-books.json"

reference_content = load_json_file(reference_file)

reference_title = reference_content.get("Title", "")
html_content = reference_content.get("Contents", "")
links_and_context = extract_links_and_context(html_content)

# Ensure the books directory exists
if not os.path.exists(books_directory):
    os.makedirs(books_directory)

# Process only the JSON files that are found in the reference file
for link, context in links_and_context:
    source_filepath = os.path.join(json_directory, link)
    if os.path.exists(source_filepath):
        updated_content = update_json_with_tags_and_synopsis(source_filepath, reference_title, context)
        target_filepath = os.path.join(books_directory, link)
        save_json_file(target_filepath, updated_content)