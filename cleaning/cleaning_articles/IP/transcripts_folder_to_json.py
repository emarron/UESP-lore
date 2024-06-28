import json
from pathlib import Path


def merge_json_files(true_final_path, master_transcripts_path):
    true_final_dir = Path(true_final_path)
    master_transcripts_dir = Path(master_transcripts_path)

    for subdir in true_final_dir.iterdir():
        if subdir.is_dir():
            master_json_content = []
            master_transcript_file = master_transcripts_dir / f"{subdir.name}.json"

            # Add the content of the associated master transcript file as the first entry
            if master_transcript_file.exists():
                with open(master_transcript_file, 'r', encoding='utf-8') as mt_file:
                    master_transcript_data = json.load(mt_file)
                    master_json_content.append(master_transcript_data)

            # Add all JSON files from the current subdirectory
            for json_file in subdir.glob("*.json"):
                with open(json_file, 'r', encoding='utf-8') as jf:
                    json_data = json.load(jf)
                    master_json_content.append(json_data)

            # Write the combined content to the master JSON file
            master_output_file = true_final_dir / f"{subdir.name}.json"
            with open(master_output_file, 'w', encoding='utf-8') as mo_file:
                json.dump(master_json_content, mo_file, indent=4)
            print(f"Created {master_output_file}")


# Usage
true_final_path = 'data/final/true_final'
master_transcripts_path = 'data/final/master_transcripts'
merge_json_files(true_final_path, master_transcripts_path)
