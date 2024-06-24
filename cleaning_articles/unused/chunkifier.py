import json
from pathlib import Path
from datasets import load_dataset, Dataset, DatasetDict
from transformers import AutoTokenizer


def chunk_text(text, tokenizer, max_length=512):
    """Chunks text into pieces that fit within the max_length limit."""
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunks = [tokens[i:i + max_length] for i in range(0, len(tokens), max_length)]
    return [tokenizer.decode(chunk, skip_special_tokens=True) for chunk in chunks]


def chunk_responses(dataset, tokenizer, max_length=512):
    new_data = []
    for entry in dataset:
        prompt = entry['prompt']
        response = entry['response']
        response_chunks = chunk_text(response, tokenizer, max_length)

        for i, chunk in enumerate(response_chunks):
            chunk_prompt = prompt + f" (Part {i + 1})" if len(response_chunks) > 1 else prompt
            new_data.append({"prompt": chunk_prompt, "response": chunk})

    return new_data


def main():
    # Load existing dataset
    dataset_path = Path('dataset.jsonl')
    dataset = load_dataset('json', data_files=str(dataset_path))['train']

    # Initialize the tokenizer
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")

    # Chunk the responses
    chunked_data = chunk_responses(dataset, tokenizer, max_length=512)

    # Save the new dataset to JSONL file
    chunked_dataset_path = Path('chunked_dataset.jsonl')
    with chunked_dataset_path.open('w', encoding='utf-8') as f:
        for entry in chunked_data:
            f.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    main()
