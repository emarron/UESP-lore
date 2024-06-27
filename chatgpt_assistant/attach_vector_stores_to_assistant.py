import os

import dotenv
from openai import OpenAI

dotenv.load_dotenv()
key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")
client = OpenAI(api_key=key)

assistant = client.beta.assistants

# Create Vector Store

vector_store = client.beta.vector_stores.create(name="Library")
print(f"Vector Store ID - {vector_store.id}")

from pathlib import Path
text = "/"
# Define the directory path
directory_path = Path("data/imperial_library_cleaned_books/MASTER_JSONS")

# Initialize the list to store file paths as strings
file_paths = []

# Iterate through the files in the directory and add their paths as strings to the list
for file in directory_path.iterdir():
    if file.is_file():
        file_paths.append(str(file))

# Print the file paths to verify
for file_path in file_paths:
    print(file_path)

file_streams = [open(path, "rb") for path in file_paths]

file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id,
    files=file_streams
)

print(f'File Status {file_batch.status}')

assistant = client.beta.assistants.update(
    assistant_id=assistant_id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)
