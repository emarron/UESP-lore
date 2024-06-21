import os.path
from pathlib import Path
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage, Settings,
)
from llama_index.llms.ollama import Ollama

# Path to your local corpus directory
PERSIST_DIR = 'storage2'
corpus_directory = 'articles'

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

Settings.llm = Ollama(model="llama3", request_timeout=360.0)

load_dotenv()
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader(corpus_directory).load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()


def chat():
    print("Chatbot is ready. Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Ending the chat. Goodbye!")
            break
        response = query_engine.query(user_input)
        print(f"Chatbot: {response}")


# Start the chat
chat()