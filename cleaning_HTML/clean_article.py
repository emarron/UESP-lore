import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

# page types:Appendices,Alchemy,Artifacts,Bestiary,Cuisine,Factions,Flora,Gods,History,Linguistics,Magic,Minerals,Names,Races,
# page types_special: Books, Locations, People

article_types = []
article_types_special = ["Books"]


def parse_page(file_path):
    with file_path.open('r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    title = soup.find('h1', {'id': 'firstHeading'}).text.strip()
    content_div = soup.find('div', class_='mw-parser-output')

    # Removing the infobox and gallery if they exist
    infobox_table = content_div.find('table', class_='wikitable infobox')
    if infobox_table:
        infobox_table.decompose()
    for gallery in content_div.find_all('div', class_='gallery'):
        gallery.decompose()

    # Extracting main content text until the references section
    content_text = ''
    references_section = content_div.find('div', class_='mw-references-wrap')
    for element in content_div.find_all(recursive=False):
        if element == references_section:
            break
        if element.name not in ['table', 'div']:
            content_text += element.get_text(separator=' ', strip=True) + ' '

    return {
        'Title': title,
        'Contents': content_text.strip()
    }


def parse_people_page(file_path):
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
    references_section = content_div.find('div', class_='mw-references-wrap')
    for element in content_div.find_all(recursive=False):
        if element == references_section:
            break
        if element.name not in ['table', 'div']:
            content_text += element.get_text(separator=' ', strip=True) + ' '

    return {
        'Title': title,
        'Contents': content_text.strip(),
        'Basic_Info': basic_info
    }


def parse_places_page(file_path):
    with file_path.open('r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    title = soup.find('h1', {'id': 'firstHeading'}).text.strip()
    content_div = soup.find('div', class_='mw-parser-output')
    infobox_table = content_div.find('table', class_='wikitable infobox')

    basic_info = {'Type': '', 'Continent': '', 'Province': '', 'Region': '', 'Appears in': ''}
    if infobox_table:
        rows = infobox_table.find_all('tr')
        for row in rows:
            header = row.find('th')
            cells = row.find_all('td')
            if header:
                header_text = header.text.strip()
                value = cells[0].get_text(strip=True) if cells else ''
                if header_text == "Type":
                    basic_info["Type"] = value
                elif header_text == "Continent":
                    basic_info["Continent"] = value
                elif header_text == "Province":
                    basic_info["Province"] = value
                elif header_text == "Region":
                    basic_info["Region"] = value
                elif header_text == "Appears in":
                    basic_info["Appears in"] = value

    # Removing the infobox and gallery if they exist
    if infobox_table:
        infobox_table.decompose()
    for gallery in content_div.find_all('div', class_='gallery'):
        gallery.decompose()

    # Extract the main content text
    content_text = ''
    references_section = content_div.find('div', class_='mw-references-wrap')
    for element in content_div.find_all(recursive=False):
        if element == references_section:
            break
        if element.name not in ['table', 'div']:
            content_text += element.get_text(separator=' ', strip=True) + ' '

    return {
        'Title': title,
        'Contents': content_text.strip(),
        'Basic_Info': basic_info
    }


def parse_books_page(file_path):
    with file_path.open('r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    title = soup.find('h1', {'id': 'firstHeading'}).text.strip()
    info_box = soup.find('table', class_='infobox')
    content_div = soup.find('div', class_='book')
    if not content_div:
        print(f"Skipping non-book file: {file_path.name}")
        return {}
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
        book_info = soup.find('div', style='text-align:center; margin:0 auto; display:table;')
        synopsis = book_info.get_text(separator='\n', strip=True) if book_info else "Synopsis not found"
        article_text = content_div.get_text(separator='\n', strip=True)

    else:
        provenance = {
            'Article': title,
            'Writer': '',
            'Seen In': ''
        }
        book_info = soup.find('div', style='text-align:center; margin:0 auto; display:table;')
        synopsis = book_info.get_text(separator='\n', strip=True) if book_info else "Synopsis not found"
        article_text = content_div.get_text(separator='\n', strip=True)

    return {
        'Title': title,
        'Provenance': provenance,
        'Synopsis': synopsis,
        'Contents': article_text
    }


def process_html_files(directory, out_directory, article_types, article_types_special):
    directory_path = Path(directory)
    out_directory_path = Path(out_directory)
    out_directory_path.mkdir(parents=True, exist_ok=True)

    # Create a dictionary to map article types to parsing functions
    parsing_functions = {
        'People': parse_people_page,
        'Places': parse_places_page
    }
    # For all other types, use the default parse_page function
    default_parse = parse_page

    all_article_types = article_types + article_types_special

    for file_path in directory_path.glob('*.html'):
        with file_path.open('r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

            # Check for book pages
            if soup.find('div', class_='book'):
                page_data = parse_books_page(file_path)
                if page_data:
                    output_file = file_path.stem + '.json'
                    output_path = out_directory_path / 'Books' / output_file
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    with output_path.open('w', encoding='utf-8') as outfile:
                        json.dump(page_data, outfile, ensure_ascii=False, indent=4)
                continue

            # For non-book pages, check the content sub
            content_sub = soup.find('div', id='contentSub')
            if content_sub:
                subpages_span = content_sub.find('span', class_='subpages')
                if subpages_span:
                    subpages_html = str(subpages_span)
                    matched_type = next((article_type for article_type in all_article_types
                                         if f'<a href="/wiki/Lore:{article_type}"' in subpages_html), None)

                    if matched_type:
                        parse_function = parsing_functions.get(matched_type, default_parse)
                        page_data = parse_function(file_path)

                        if page_data:
                            output_file = file_path.stem + '.json'
                            output_path = out_directory_path / matched_type / output_file
                            output_path.parent.mkdir(parents=True, exist_ok=True)
                            with output_path.open('w', encoding='utf-8') as outfile:
                                json.dump(page_data, outfile, ensure_ascii=False, indent=4)


def main():
    in_dir = 'LORE_DUMP'
    process_html_files(in_dir, 'CLEANED_OUTPUT', article_types, article_types_special)


if __name__ == "__main__":
    main()