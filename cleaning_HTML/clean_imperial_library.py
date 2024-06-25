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
        return str(main_content), None
    else:
        return None, file_path

def save_to_json(output_path, title, content):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data = {
        "Title": title,
        "Contents": content
    }
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def process_files(root_dir, output_root):
    not_found_list = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(subdir, file)
                relative_path = os.path.relpath(file_path, root_dir)
                output_path = os.path.join(output_root, relative_path).replace(".html", ".json")

                title = os.path.splitext(file)[0]
                content, not_found_path = extract_content_from_html(file_path)

                if content:
                    save_to_json(output_path, title, content)
                    print(f"Processed and saved: {output_path}")
                else:
                    not_found_list.append(not_found_path)
                    print(f"Main content not found in: {file_path}")

    return not_found_list

root_directory = "DUMPS/imperial_library"  # Change to the root directory containing your HTML files
output_directory = "imperial_library_cleaned"  # Change to the desired output directory

not_found_files = process_files(root_directory, output_directory)
print("Files with no main content found:")
print(not_found_files)
