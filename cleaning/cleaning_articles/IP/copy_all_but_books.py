from pathlib import Path
import shutil

# Define the paths to the directories
cleaned_dir = Path('imperial_library_cleaned')
sorted_dir = Path('imperial_library_sorted')
review_dir = Path('imperial_library_cleaned_review')

# Ensure the review directory exists
review_dir.mkdir(parents=True, exist_ok=True)

# Create a set of all file names in the sorted directory
sorted_files = {file.name for file in sorted_dir.rglob('*') if file.is_file()}

# Walk through the cleaned directory
for cleaned_file in cleaned_dir.rglob('*'):
    if cleaned_file.is_file():
        # Check if the file exists in the sorted files set
        if cleaned_file.name not in sorted_files:
            # Determine the target path in the review directory
            rel_path = cleaned_file.relative_to(cleaned_dir)
            target_file = review_dir / rel_path
            target_file.parent.mkdir(parents=True, exist_ok=True)

            # Copy the file to the review directory
            shutil.copy(cleaned_file, target_file)

print("Files copied successfully.")
