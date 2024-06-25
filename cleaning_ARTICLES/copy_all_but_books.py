import os
import shutil

# Define the paths to the directories
cleaned_dir = 'imperial_library_cleaned'
sorted_dir = 'imperial_library_sorted'
review_dir = 'imperial_library_cleaned_review'

# Ensure the review directory exists
os.makedirs(review_dir, exist_ok=True)

# Walk through the cleaned directory
for root, dirs, files in os.walk(cleaned_dir):
    # Determine the relative path from the cleaned directory
    rel_path = os.path.relpath(root, cleaned_dir)

    for file in files:
        # Full path to the file in the cleaned directory
        cleaned_file = os.path.join(root, file)

        # Corresponding path in the sorted directory
        sorted_file = os.path.join(sorted_dir, rel_path, file)

        # Check if the file exists in the sorted directory
        if not os.path.exists(sorted_file):
            # Determine the target path in the review directory
            target_dir = os.path.join(review_dir, rel_path)
            os.makedirs(target_dir, exist_ok=True)

            # Copy the file to the review directory
            shutil.copy(cleaned_file, target_dir)

print("Files copied successfully.")
