import shutil
from pathlib import Path

from data_directory_set.config import DATA_DIRECTORY


def copy_directory_structure(src, dest):
    src_path = Path(src)
    dest_path = Path(dest)

    for src_dir in src_path.rglob('*'):
        if src_dir.is_dir():
            rel_path = src_dir.relative_to(src_path)
            dest_dir = dest_path / rel_path
            if not dest_dir.exists():
                dest_dir.mkdir(parents=True)
                print(f"Created directory: {dest_dir}")


def move_files_to_structure(src, dest, result):
    dest_path = Path(dest)
    result_path = Path(result)

    for json_file in dest_path.rglob('*.json'):
        rel_path = json_file.relative_to(dest_path)
        src_file_name = json_file.name

        # Find the corresponding directory in src that matches the file name
        for src_dir in Path(src).rglob('*'):
            if src_dir.is_dir() and (src_dir / src_file_name).exists():
                dest_file_path = result_path / src_dir.relative_to(src) / src_file_name
                if not dest_file_path.parent.exists():
                    dest_file_path.parent.mkdir(parents=True)
                if not dest_file_path.exists():
                    shutil.move(str(json_file), str(dest_file_path))
                    print(f"Moved file: {json_file} to {dest_file_path}")
                else:
                    print(f"File already exists: {dest_file_path}")
                break


def process_unknown_files(result, src_structure, dest_structure):
    result_path = Path(result)
    unknown_dir = result_path / 'unknown'

    for json_file in Path(dest_structure).rglob('*.json'):
        rel_path = json_file.relative_to(dest_structure)
        src_expected_path = Path(src_structure) / rel_path

        if not src_expected_path.exists():
            if not unknown_dir.exists():
                unknown_dir.mkdir(parents=True)
                print(f"Created unknown directory: {unknown_dir}")

            dest_file_path = unknown_dir / json_file.name

            if not dest_file_path.exists():
                shutil.move(str(json_file), str(dest_file_path))
                print(f"Moved unknown file: {json_file} to {dest_file_path}")
            else:
                print(f"Unknown file already exists: {dest_file_path}")


src_dir = DATA_DIRECTORY
dest_dir = 'CLEANED_OUTPUT'
result_dir = 'paralleled_struct'

# Copy directory structure from src_dir to result_dir
copy_directory_structure(src_dir, result_dir)

# Move files from dest_dir into the structure in result_dir
move_files_to_structure(src_dir, dest_dir, result_dir)

# Process unknown files
process_unknown_files(result_dir, src_dir, dest_dir)
