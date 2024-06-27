import json5
import csv
from pathlib import Path


def read_json(file_path):
    with file_path.open('r', encoding='utf-8') as file:
        return json5.load(file)


def get_all_json_files(directory):
    return list(directory.rglob('*.json'))


def normalize_title(title):
    return title.strip().lower()


def collect_titles_and_paths(directory, key):
    titles_and_paths = []
    json_files = get_all_json_files(directory)

    for file in json_files:
        json_data = read_json(file)
        if key in json_data:
            normalized_title = normalize_title(json_data[key])
            relative_path = file.relative_to(directory)
            titles_and_paths.append((normalized_title, str(file)))

    return titles_and_paths


def write_to_csv(titles_and_paths, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Path"])
        writer.writerows(titles_and_paths)


# Example usage
dir_a = Path('imperial_library_sorted')
dir_b = Path('cleaned_articles/Books')

titles_and_paths_a = collect_titles_and_paths(dir_a, 'True_Title')
titles_and_paths_b = collect_titles_and_paths(dir_b, 'Title')

write_to_csv(titles_and_paths_a, 'imperial_library_sorted.csv')
write_to_csv(titles_and_paths_b, 'cleaned_articles_Books.csv')

print("Titles and paths from Directory A written to imperial_library_sorted.csv")
print("Titles and paths from Directory B written to cleaned_articles_Books.csv")
