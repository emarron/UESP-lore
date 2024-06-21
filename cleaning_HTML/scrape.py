# scrape.py

import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
import time

base_url = "https://en.uesp.net"
all_pages_url = f"{base_url}/wiki/Special:AllPages?from=&to=&namespace=130&hideredirects=1"
lore_dump_dir = Path('LORE_DUMP')

# Create the LORE_DUMP directory if it doesn't exist
lore_dump_dir.mkdir(exist_ok=True)

# Function to check if a title matches the "Lore:%ANYTHING%" pattern
def is_lore_page(title):
    return re.match(r"^Lore:[^ ]", title)

# Function to get all lore article URLs from the provided all pages URL
def get_lore_article_urls():
    url_list = []
    next_page_url = all_pages_url

    while next_page_url:
        response = requests.get(next_page_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            if link['href'].startswith('/wiki/Lore:'):
                url_list.append(base_url + link['href'])

        # Find the next page link
        next_page_link = soup.find('a', text=re.compile(r'Next page'))
        if next_page_link:
            next_page_url = base_url + next_page_link['href']
        else:
            next_page_url = None

    return url_list

# Function to sanitize filenames by removing invalid characters
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Function to save the content of a lore page to a file
def save_lore_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text
    filename = title.replace(":", "_").replace(" - The Unofficial Elder Scrolls Pages (UESP)", "") + '.html'
    filename = sanitize_filename(filename)

    filepath = lore_dump_dir / filename
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(response.text)

    print(f"Saved: {filename}")

# Main function to execute the scraping
def main():
    lore_article_urls = get_lore_article_urls()

    # Save each lore page to the LORE_DUMP directory
    for lore_page in lore_article_urls:
        save_lore_page(lore_page)
        time.sleep(1)  # Adding delay to avoid overwhelming the server

if __name__ == "__main__":
    main()
