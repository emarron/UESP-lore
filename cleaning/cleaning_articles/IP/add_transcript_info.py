import json
from pathlib import Path
from bs4 import BeautifulSoup

# Directory containing your JSON files
json_directory = Path("data/transcript")
# Directory where the processed JSON files will be saved
output_directory = Path("data/imperial_library_sorted/transcript")
# Path to the failure log file
failure_log_path = output_directory / "failure.txt"


def load_json_files(directory):
    json_files = {}
    for filepath in directory.rglob("*.json"):
        with filepath.open('r', encoding='utf-8') as file:
            json_files[filepath] = json.load(file)
    return json_files


def extract_transcript_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    transcript_info = {}

    # Extract the true title
    true_title_tag = soup.find('h1', class_='entry-title', itemprop='headline')
    if true_title_tag:
        transcript_info['True_Title'] = true_title_tag.get_text(strip=True)

    # Extract the dialogues
    dialogues = []
    headings = soup.find_all('h6', class_='wp-block-heading')
    for heading in headings:
        speaker = heading.get_text(strip=True)
        dialogue = heading.find_next_sibling('p')
        if dialogue:
            dialogues.append(f'{speaker}: "{dialogue.get_text(strip=True)}"')

    if dialogues:
        transcript_info['Dialogue'] = "\n".join(dialogues)
    else:
        # Extract and format all content from the entry-content clear class
        entry_content = soup.find('div', class_='entry-content clear')
        if entry_content:
            formatted_content = entry_content.get_text(separator="\n", strip=True)
            transcript_info['Formatted_Contents'] = formatted_content
            transcript_info['Tags'] = ["Unformatted Transcript"]

    return transcript_info


def update_json_with_transcript_info(json_files):
    updated_files = {}
    failed_files = []

    for filepath, content in json_files.items():
        html_content = content.get("Contents", "")
        transcript_info = extract_transcript_info(html_content)
        if transcript_info:  # Only update if it's a transcript
            content.update(transcript_info)
            relative_path = filepath.relative_to(json_directory)
            category = relative_path.parent
            if category not in updated_files:
                updated_files[category] = {}
            updated_files[category][filepath.name] = content
        else:
            failed_files.append(filepath)

    return updated_files, failed_files


def save_json_files(output_directory, updated_files):
    for category, files in updated_files.items():
        category_dir = output_directory / category
        category_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            output_path = category_dir / filename
            with output_path.open('w', encoding='utf-8') as file:
                json.dump(content, file, ensure_ascii=False, indent=4)


def log_failed_files(failure_log_path, failed_files):
    failure_log_path.parent.mkdir(parents=True, exist_ok=True)
    with failure_log_path.open('w', encoding='utf-8') as file:
        for filepath in failed_files:
            file.write(f"{filepath}\n")


# Main script
json_files = load_json_files(json_directory)

# Update all JSON files with transcript information
updated_files, failed_files = update_json_with_transcript_info(json_files)

# Save the updated JSON files to the new directory structure
save_json_files(output_directory, updated_files)

# Log the files that failed to trigger formatted_contents
log_failed_files(failure_log_path, failed_files)
