import os
import json
from bs4 import BeautifulSoup

# Directory containing your JSON files
json_directory = "data/imperial_library_cleaned/content/"
transcripts_directory = "data/transcript/legends/"


def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)


def extract_title_and_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract title
    title_tag = soup.find('h1', class_='entry-title', itemprop='headline')
    reference_title = title_tag.get_text().strip() if title_tag else ""

    links_by_header = []

    # Extract headers and links within each section
    current_header = None
    current_subheader = None

    for tag in soup.find_all(['h4', 'h5', 'div']):
        if tag.name == 'h4' and 'wp-block-heading' in tag.get('class', []):
            current_header = tag.get_text().strip()
            current_subheader = None
        elif tag.name == 'h5' and 'wp-block-heading' in tag.get('class', []):
            current_subheader = tag.get_text().strip()
        elif tag.name == 'div' and 'book-listing' in tag.get('class', []):
            links = []
            for item in tag.find_all('div', class_='listing-item'):
                a_tag = item.find('a', href=True)
                if a_tag:
                    link = a_tag['href'].split('/')[-1].replace('.html', '.json')
                    excerpt_tag = item.find('span', class_='excerpt')
                    context = excerpt_tag.get_text().strip() if excerpt_tag else ""
                    links.append((link, context))
            if links:
                links_by_header.append((current_header, current_subheader, links))

    return reference_title, links_by_header


def update_json_with_tags_and_synopsis(filepath, reference_title, context, header, subheader):
    json_content = load_json_file(filepath)
    if 'Tags' not in json_content:
        json_content['Tags'] = []
    if reference_title not in json_content['Tags']:
        json_content['Tags'].append(reference_title)
    if 'Transcript' not in json_content['Tags']:
        json_content['Tags'].append("Transcript")
    json_content['Synopsis'] = context
    if subheader:
        json_content['Quest Line'] = f"{header} - {subheader}"
    else:
        json_content['Quest Line'] = header
    return json_content


def save_json_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=4)


# Load the reference JSON file
reference_file = "data/imperial_library_cleaned/transcripts/elder-scrolls-legends-transcripts.json"

reference_content = load_json_file(reference_file)

html_content = reference_content.get("Contents", "")
reference_title, links_by_header = extract_title_and_links(html_content)

# Ensure the transcripts directory exists
if not os.path.exists(transcripts_directory):
    os.makedirs(transcripts_directory)

# Process the JSON files based on the extracted links and context
for header, subheader, links in links_by_header:
    for link, context in links:
        source_filepath = os.path.join(json_directory, link)
        if os.path.exists(source_filepath):
            updated_content = update_json_with_tags_and_synopsis(source_filepath, reference_title, context, header,
                                                                 subheader)
            target_filepath = os.path.join(transcripts_directory, link)
            save_json_file(target_filepath, updated_content)
