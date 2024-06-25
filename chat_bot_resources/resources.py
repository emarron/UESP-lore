from pathlib import Path
import json
from llama_index.core import Document, VectorStoreIndex, StorageContext, load_index_from_storage


def create_or_load_index(persist_dir, article_directory):
    persist_path = Path(persist_dir)
    article_path = Path(article_directory)

    if not persist_path.exists():
        # Load the documents and create the index
        documents = []

        for filepath in article_path.rglob('*.json'):
            with filepath.open('r', encoding='utf-8') as f:
                article = json.load(f)
                content = article.get('Contents', '').strip()
                if content:
                    title = article.get('Title', '')
                    tags = article.get('tags', [])
                    document = Document(text=content, meta={"title": title, "tags": tags})
                    documents.append(document)

        if documents:
            index = VectorStoreIndex.from_documents(documents)
            index.storage_context.persist(persist_dir=str(persist_path))
        else:
            print("No documents to index.")
    else:
        storage_context = StorageContext.from_defaults(persist_dir=str(persist_path))
        index = load_index_from_storage(storage_context)

    return index


def completion_to_prompt_phi(completion):
    return f"<|system|>You are a librarian that helps summarize elder scrolls lore.<|end|>\n<|user|>\n{completion}<|end|>\n<|assistant|>\n"


# Transform a list of chat messages into zephyr-specific input
def messages_to_prompt_phi(messages):
    prompt = ""
    for message in messages:
        if message.role == "system":
            prompt += f"<|system|>\n{message.content}<|end|>\n"
        elif message.role == "user":
            prompt += f"<|user|>\n{message.content}<|end|>\n"
        elif message.role == "assistant":
            prompt += f"<|assistant|>\n{message.content}<|end|>\n"

    # ensure we start with a system prompt, insert blank if needed
    if not prompt.startswith("<|system|>\n"):
        prompt = "<|system|>\n<|end|>\n" + prompt

    # add final assistant prompt
    prompt = prompt + "<|assistant|>\n"

    return prompt


def completion_to_prompt_llama3(completion):
    return f"### System\nYou are a librarian that helps summarize Elder Scrolls lore.\n\n### Assistant\n{completion}\n"


# Transform a list of chat messages into Llama3-specific input
def messages_to_prompt_llama3(messages):
    prompt = ""
    for message in messages:
        if message['role'] == "system":
            prompt += f"### System\n{message['content']}\n"
        elif message['role'] == "user":
            prompt += f"### User\n{message['content']}\n"
        elif message['role'] == "assistant":
            prompt += f"### Assistant\n{message['content']}\n"

    # Ensure we start with a system prompt, insert blank if needed
    if not prompt.startswith("### System"):
        prompt = "### System\n\n" + prompt

    # Add final assistant prompt
    prompt += "### Assistant\n"

    return prompt
