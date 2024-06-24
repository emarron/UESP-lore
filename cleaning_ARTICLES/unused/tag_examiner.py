import json
from pathlib import Path
from collections import Counter
from thefuzz import process

# Function to normalize and group similar tags
def normalize_tags(tag_counter):
    threshold = 80  # Similarity threshold
    normalized_tags = Counter()
    for tag in tag_counter:
        match = None
        if normalized_tags:
            result = process.extractOne(tag, list(normalized_tags.keys()))
            if result and result[1] >= threshold:
                match = result[0]
        if match:
            normalized_tags[match] += tag_counter[tag]
        else:
            normalized_tags[tag] = tag_counter[tag]
    return normalized_tags

# Function to traverse directories and collect tags
def collect_tags(directory):
    tag_counter = Counter()
    json_files = []
    for json_file in Path(directory).rglob('*.json'):
        json_files.append(json_file)
        with open(json_file, 'r') as f:
            data = json.load(f)
            if 'tags' in data:
                normalized_tags = [tag.lower() for tag in data['tags']]
                tag_counter.update(normalized_tags)
    return tag_counter, json_files

# Function to remove irrelevant tags
def remove_irrelevant_tags(json_files, irrelevant_tags):
    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)
        if 'tags' in data:
            data['tags'] = [tag for tag in data['tags'] if tag.lower() not in irrelevant_tags]
            with open(json_file, 'w') as f:
                json.dump(data, f, indent=4)

# Main script
directory = '../cleaned_articles'  # Update this with the path to your directory
tag_counter, json_files = collect_tags(directory)
normalized_tag_counter = normalize_tags(tag_counter)

# Display and dump the most common tags
most_common_tags = normalized_tag_counter.most_common(100)  # Adjust the number to show more/less common tags
with open('most_common_tags.txt', 'w') as f:
    f.write("Most common tags:\n")
    for tag, count in most_common_tags:
        f.write(f"{tag}: {count}\n")

print("Most common tags have been saved to 'most_common_tags.txt'.")

# Ask user if they want to proceed with removing the common tags
response = input("Do you want to remove these common tags? (yes/no): ").strip().lower()
if response == 'yes':
    irrelevant_tags = {tag for tag, _ in most_common_tags}
    remove_irrelevant_tags(json_files, irrelevant_tags)
    print("Irrelevant tags removed.")
else:
    print("No tags were removed.")
