import spacy
import os
import json
import subprocess
import re
from nltk.corpus import stopwords
import string

from chat_bot_resources.config import DATA_DIRECTORY


# Function to download SpaCy model if not already present
def download_spacy_model():
    try:
        spacy.load('en_core_web_sm')
    except OSError:
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])


# Function to download NLTK stopwords if not already present
def download_nltk_stopwords():
    try:
        stopwords.words('english')
    except LookupError:
        import nltk
        nltk.download('stopwords')


# Download the SpaCy model if necessary
download_spacy_model()
# Download NLTK stopwords if necessary
download_nltk_stopwords()

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

# Get NLTK stopwords list
nltk_stopwords = set(stopwords.words('english'))

# Custom stopwords and filter criteria
custom_stopwords = set()
with open('cleaning_articles/stopwords-en.txt', 'r', encoding='utf-8') as file:
    for line in file:
        custom_stopwords.add(line.strip().lower())


all_stopwords = nltk_stopwords.union(custom_stopwords)


def generate_tags(text):
    doc = nlp(text)
    tags = set()
    for ent in doc.ents:
        # Filter out stopwords, single characters, and numerical values
        if (ent.text.lower() not in all_stopwords and
                len(ent.text) > 1 and
                not ent.text.isdigit() and
                not all(char in string.punctuation for char in ent.text)):
            tags.add(ent.text)
    return list(tags)


def add_folder_tags(filepath):
    # Split the filepath to get folder names and filename
    parts = filepath.split(os.sep)  # Use os.sep for cross-platform compatibility
    folder_tags = parts[1:-1]  # Get all parts except the root folder and filename
    return folder_tags


def extract_references(content, references):
    # Find all reference markers in the content
    ref_markers = re.findall(r'\[\d+\]', content)

    # Map markers to references
    ref_map = {}
    for marker in set(ref_markers):
        ref_index = int(marker.strip('[]')) - 1
        if ref_index < len(references):
            ref_map[marker] = references[ref_index]

    return ref_map


def extract_additional_info(article):
    additional_tags = set()

    # Check for and extract information from specific sections
    provenance = article.get('Provenance', {})
    if provenance:
        for key, value in provenance.items():
            if value:
                additional_tags.add(f"{key}: {value}")

    synopsis = article.get('Synopsis', '')
    if synopsis:
        additional_tags.add(f" {synopsis}")

    person_info = article.get('Person_Info', {})
    if person_info:
        for key, value in person_info.items():
            if value:
                additional_tags.add(f"{key}: {value}")

    place_info = article.get('Place_Info', {})
    if place_info:
        for key, value in place_info.items():
            if value:
                additional_tags.add(f"{key}: {value}")

    return list(additional_tags)


def extract_dates(content):
    date_tags = set()
    # Patterns for eras and dates
    era_patterns = [
        r'\b1st era\b', r'\b2nd era\b', r'\b3rd era\b', r'\b4th era\b',
        r'\b1E \d+\b', r'\b2E \d+\b', r'\b3E \d+\b', r'\b4E \d+\b'
    ]
    for pattern in era_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        date_tags.update(matches)

    return list(date_tags)


# Walk through the directory structure and process JSON files
root_dir = DATA_DIRECTORY
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.json'):
            filepath = os.path.join(subdir, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    article = json.load(f)

                # Remove existing tags
                if 'tags' in article:
                    del article['tags']

                # Generate tags from content
                content_tags = generate_tags(article.get('Contents', ''))

                # Add folder tags
                folder_tags = add_folder_tags(filepath)

                # Extract references
                references = article.get('References', [])
                ref_map = extract_references(article.get('Contents', ''), references)

                # Extract additional info
                additional_info_tags = extract_additional_info(article)

                # Extract date tags
                date_tags = extract_dates(article.get('Contents', ''))

                # Combine all tags
                ref_tags = list(ref_map.values())
                all_tags = list(set(content_tags + folder_tags + ref_tags + additional_info_tags + date_tags))

                # Update the article with tags
                article['tags'] = all_tags

                # Save the updated article back to the file
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(article, f, indent=4)
            except UnicodeDecodeError as e:
                print(f"Error decoding file {filepath}: {e}")

print("Tagging completed.")
