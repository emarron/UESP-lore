import os
import json
from bs4 import BeautifulSoup

# Directory containing your JSON files
json_directory = "books"
# Directory where the processed JSON files will be saved
output_directory = "imperial_library_sorted/book"
# Path to the failure log file
failure_log_path = os.path.join(output_directory, "failure.txt")


def load_json_files(directory):
    json_files = {}
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                json_files[filename] = json.load(file)
    return json_files


def extract_book_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    book_info = {}

    # Check if the book-info box exists
    book_info_tag = soup.find('p', class_='book-info')
    if not book_info_tag:
        return None  # Not a book

    # Extract the true title
    true_title_tag = soup.find('h1', class_='entry-title', itemprop='headline')
    if true_title_tag:
        book_info['True_Title'] = true_title_tag.get_text(strip=True)

    # Extract "Released in" information
    released_in = [a.get_text(strip=True) for a in
                   book_info_tag.find_all('a', href=lambda href: 'game-category' in href)]
    book_info['Released in'] = ', '.join(released_in) if released_in else ''

    # Extract "Category" information
    category_tag = book_info_tag.find('a', href=lambda href: 'book-type' in href)
    book_info['Category'] = category_tag.get_text(strip=True).lower() if category_tag else ''

    # Extract "Author" information
    author_text = book_info_tag.get_text(strip=True)
    if 'Author (in-game):' in author_text:
        author = author_text.split('Author (in-game):')[-1].strip()
        book_info['Author'] = author
    else:
        book_info['Author'] = ''

    # Extract librarian comment
    librarian_comment_tag = soup.find('div', class_='librarian-comment')
    if librarian_comment_tag:
        librarian_comment_p_tag = librarian_comment_tag.find('p')
        if librarian_comment_p_tag:
            librarian_comment = librarian_comment_p_tag.get_text(strip=True)
            book_info['Librarian_Comment'] = librarian_comment

    # Extract and format the content within <div class="news-post"></div>
    formatted_books = []
    news_post_tags = soup.find_all('div', class_='news-post')
    for news_post in news_post_tags:
        for listing_item in news_post.find_all('div', class_='listing-item'):
            title_tag = listing_item.find('a', class_='title')
            content_tag = listing_item.find('div', class_='content')
            if title_tag and content_tag:
                formatted_books.append({
                    "Title": title_tag.get_text(strip=True),
                    "Contents": content_tag.get_text(strip=True)
                })

    if formatted_books:
        book_info['Formatted_Books'] = formatted_books

    # Extract and format the content within <div class="entry-content clear"></div> if no news-post is found
    if not formatted_books:
        entry_content_tag = soup.find('div', class_='entry-content clear')
        if entry_content_tag:
            # Remove librarian comment from the entry-content
            if librarian_comment_tag:
                librarian_comment_tag.extract()
            formatted_content = entry_content_tag.get_text(strip=True)
            book_info['Formatted_Content'] = {
                "Title": book_info.get('True_Title', ''),
                "Contents": formatted_content.strip()
            }

    return book_info


def update_json_with_book_info(json_files):
    updated_files = {}
    failed_files = []

    for filename, content in json_files.items():
        html_content = content.get("Contents", "")
        book_info = extract_book_info(html_content)
        if book_info:  # Only update if it's a book
            json_files[filename].update(book_info)
            # Add "Book" tag if it doesn't already exist
            if 'Tags' not in json_files[filename]:
                json_files[filename]['Tags'] = []
            if "Book" not in json_files[filename]['Tags']:
                json_files[filename]['Tags'].append("Book")

            # Prepare for saving to new directory
            category = book_info.get('Category', 'unknown')
            if category not in updated_files:
                updated_files[category] = []
            updated_files[category].append((filename, json_files[filename]))
        else:
            failed_files.append(filename)

    return updated_files, failed_files


def save_json_files(output_directory, updated_files):
    for category, files in updated_files.items():
        category_dir = os.path.join(output_directory, category)
        os.makedirs(category_dir, exist_ok=True)
        for filename, content in files:
            output_path = os.path.join(category_dir, filename)
            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(content, file, ensure_ascii=False, indent=4)


def log_failed_files(failure_log_path, failed_files):
    with open(failure_log_path, 'w', encoding='utf-8') as file:
        for filename in failed_files:
            file.write(f"{filename}\n")


# Main script
json_files = load_json_files(json_directory)

# Update all JSON files with book information
updated_files, failed_files = update_json_with_book_info(json_files)

# Save the updated JSON files to the new directory structure
save_json_files(output_directory, updated_files)

# Log the files that failed to trigger formatted_contents
log_failed_files(failure_log_path, failed_files)
