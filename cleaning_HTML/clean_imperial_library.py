import os
import json
import chardet
from bs4 import BeautifulSoup

def detect_encoding(file_path):
    with open(file_path, "rb") as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def extract_content_from_html(file_path):
    encoding = detect_encoding(file_path)
    with open(file_path, "r", encoding=encoding, errors="ignore") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    main_content = soup.find("main", id="main", class_="site-main")

    if main_content:
        text_content = main_content.get_text(separator="\n", strip=True)
    else:
        text_content = "Main content not found."

    return text_content

def save_to_json(output_path, title, content):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data = {
        "Title": title,
        "Contents": content
    }
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def process_files(root_dir, output_root):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(subdir, file)
                relative_path = os.path.relpath(file_path, root_dir)
                output_path = os.path.join(output_root, relative_path).replace(".html", ".json")

                title = os.path.splitext(file)[0]
                content = extract_content_from_html(file_path)

                save_to_json(output_path, title, content)
                print(f"Processed and saved: {output_path}")

root_directory = "DUMPS/imperial_library"  # Change to the root directory containing your HTML files
output_directory = "imperial_libary_cleaned"  # Change to the desired output directory

process_files(root_directory, output_directory)


# pay special attention to game books as it has a synopsis for each book. this may prove valuable.
