import json
from pathlib import Path
from bs4 import BeautifulSoup

import json
from pathlib import Path
from bs4 import BeautifulSoup


def parse_wiki_page(file_path):
    with file_path.open('r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    title = soup.find('h1', {'id': 'firstHeading'}).text.strip()
    content_div = soup.find('div', class_='mw-parser-output')
    basic_info_table = content_div.find('table', class_='wikitable infobox')

    basic_info = {'Race': '', 'Gender': '', 'Born': '', 'Died': '', 'Appears in': ''}
    if basic_info_table:
        rows = basic_info_table.find_all('tr')
        for row in rows:
            headers = row.find_all('th')
            cells = row.find_all('td')
            for i in range(len(headers)):
                header_text = headers[i].text.strip()
                if i < len(cells):
                    value = cells[i].get_text(strip=True)
                    if header_text == "Race":
                        basic_info["Race"] = value
                    elif header_text == "Gender":
                        basic_info["Gender"] = value
                    elif header_text == "Born":
                        basic_info["Born"] = value
                    elif header_text == "Died":
                        basic_info["Died"] = value
                    elif header_text == "Appears in":
                        basic_info["Appears in"] = value

    # Removing the infobox and gallery if they exist
    if basic_info_table:
        basic_info_table.decompose()
    for gallery in content_div.find_all('div', class_='gallery'):
        gallery.decompose()

    # Extract the main content text
    content_text = ''
    for element in content_div.find_all(recursive=False):
        if element.name not in ['table', 'div']:
            content_text += element.get_text(separator=' ', strip=True) + ' '

    return {
        'Title': title,
        'Contents': content_text.strip(),
        'Basic_Info': basic_info
    }


def process_html_files(directory, out_directory):
    directory_path = Path(directory)
    out_directory_path = Path(out_directory)
    out_directory_path.mkdir(parents=True, exist_ok=True)

    for file_path in directory_path.glob('*.html'):
        with file_path.open('r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            content_sub = soup.find('div', id='contentSub')
            if content_sub:
                subpages_span = content_sub.find('span', class_='subpages')
                if subpages_span and '<a href="/wiki/Lore:People"' in str(subpages_span):
                    page_data = parse_wiki_page(file_path)
                    output_file = file_path.stem + '.json'
                    output_path = out_directory_path / output_file
                    with output_path.open('w', encoding='utf-8') as outfile:
                        json.dump(page_data, outfile, ensure_ascii=False, indent=4)


def main():
    in_dir = 'LORE_DUMP'  # Replace with your directory path
    out_dir = 'PEOPLE_CLEANED'
    process_html_files(in_dir, out_dir)

if __name__ == "__main__":
    main()
