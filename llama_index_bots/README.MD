# llama_index_bots

This subdirectory uses `llamaindex` to enable users to query Elder Scrolls lore.
The main recommendations are `Ollama` or a `huggingfaces` type (advanced). If you were to be doing a chatGPT type I recommend
using the `chatgpt_assistant` type.

See `storage` for the different indexes you can use. You want the index to match the specific model and embedding type.
If you want to train, check the `data` directory.
## Tools
- **llama_index_bots**: Tools for running or creating llamaindex vector stores.

## Demo
- **Hugging Faces Demo**: [Meta-Llama-3-8B-Instruct + BGE embeddings](https://huggingface.co/spaces/emarron/elderscrolls_lore_bot)

## Tier List
1. **ChatGPT version**: Best performance and speed. Not recommended because The assistant is superior.
2. **Local Ollama**: Comparable to Hugging Faces but can be slow without a GPU.
3. **Hugging Faces**: Easiest to use, no hardware requirements.
4. **Alternative Models**: Use only if space is limited or experimenting.

## Getting Started
### Prerequisites
- ChatGPT API key for the ChatGPT version.
- Ollama installed for the local version.
- HuggingFaces API key for certain HuggingFaces models.
- Python 3.10

### Installation


1. **Download Storage Folder**
Please review the Storage section for this.
In general you will want the index that fulfills:
* Matches the specific LLM model you are using
* Matches the specific embeddings you are using (this will almost always be BGE-Large)

[llamaindexes](https://app.mediafire.com/83516vc48hz8v)
You most likely want storage_bge-large-en-v1-5_local_ollama_llama3.7z

Place this file in the `storage` directory in the root or create it if it doesn't exist.

If you are trying to train your own indexes you would want the cleaned data. Information can be found about that in the `data` subdirectory.

Most likely you want

2. **Highly Recommended Installs**

These consist of requirements that are HIGHLY recommended. Please read this file thoroughly.

**CUDA Installation**

If you have an NVIDIA device, download CUDA from the following link:
[CUDA Downloads](https://developer.nvidia.com/cuda-downloads)

**PyTorch Installation**

Select the correct PyTorch version for your system from the following link:
[PyTorch Get Started](https://pytorch.org/get-started/locally/)

For this example, I will use Preview (Nightly), Windows, Pip, Python, CUDA 12.4 since this most closely matches my CUDA version of 12.5. The command for my setup would be:

```sh
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124
```

3. **Download Requirements:
```sh
pip install -r llama_index_bots/requirements.txt

```


4. **Download Ollama (local_ollama ONLY)**
- [Ollama download](https://ollama.com/download)

5. **Set Up Environment Variables (Only for ChatGPT version or certain HuggingFaces)**

Create a `.env` file in the project root with your API keys:
```env
CHATGPT_API_KEY=your_api_key_here
HF_KEY=your_huggingfaces_api_key_here
```

6. Very Optional Improvements:

The following packages are also recommended:

- `bitsandbytes`
- `requests`
- `einops`

You can install these packages using:

```sh
pip install bitsandbytes requests einops
```


`triton` and `flashattn` are good to have but can fail to install at times. Make sure you have the latest Pip before attempting to install them.

- `triton`
- `flashattn`

You can try installing them using:

```sh
pip install triton flashattn
```

### Usage
1. **Run the Llama Indexer**
```bash
python llama_indexer_bots\llama_indexer_chatgpt.py
```
or
```bash
python llama_indexer_bots\llama_indexer_local_ollama.py
```

or 
```bash
python llama_indexer_bots\llama_indexer_local_hf_type.py
```

2. **Ask Questions**
Interact with the chatbot via the local URL provided in the terminal.


### License
This project is licensed under the MIT License.

---

Feel free to adapt this description to fit your needs and project updates.